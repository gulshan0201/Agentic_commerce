import json
import re
import time

from google import genai

from app.config import settings
from app.schemas.intent import ShoppingIntent


client = genai.Client(
    api_key=settings.gemini_api_key
)


SYSTEM_PROMPT = """
You are an intent extraction system for an electronics commerce application.

Convert the user's shopping request into JSON.

Allowed fields:

category
budget_max
use_case
minimum_ram
gpu_required
minimum_rating
in_stock_only

Rules:

1. category examples:
   laptop, smartphone, headphones, keyboard, mouse, accessories

2. Convert shorthand money:
   80k = 80000
   1 lakh = 100000
   1.2 lakh = 120000

3. Machine learning, AI, deep learning, gaming and video editing
   usually require a dedicated GPU.

4. If RAM is not mentioned:
   minimum_ram = null

5. If rating is not mentioned:
   minimum_rating = null

6. in_stock_only defaults to true.

7. Never invent a budget.

Return JSON only.
"""


def local_intent_parser(
    message: str
) -> ShoppingIntent:

    text = message.lower()

    # --------------------
    # Category
    # --------------------

    category = None

    if "laptop" in text:
        category = "laptop"

    elif any(
        word in text
        for word in [
            "smartphone",
            "phone",
            "mobile"
        ]
    ):
        category = "smartphone"

    elif "headphone" in text:
        category = "headphones"

    elif "keyboard" in text:
        category = "keyboard"

    elif "mouse" in text:
        category = "mouse"

    elif "accessor" in text:
        category = "accessories"

    # --------------------
    # Budget
    # --------------------

    budget = None

    lakh_match = re.search(
        r"(\d+(?:\.\d+)?)\s*lakh",
        text
    )

    if lakh_match:

        budget = (
            float(lakh_match.group(1))
            * 100000
        )

    else:

        k_match = re.search(
            r"(\d+(?:\.\d+)?)\s*k\b",
            text
        )

        if k_match:

            budget = (
                float(k_match.group(1))
                * 1000
            )

        else:

            amount_match = re.search(
                r"(?:under|below|upto|up to|max(?:imum)?(?: budget)?(?: of)?)\s*₹?\s*([\d,]+)",
                text
            )

            if amount_match:

                budget = float(
                    amount_match
                    .group(1)
                    .replace(",", "")
                )

    # --------------------
    # RAM
    # --------------------

    minimum_ram = None

    ram_match = re.search(
        r"(\d+)\s*gb\s*ram",
        text
    )

    if ram_match:

        minimum_ram = int(
            ram_match.group(1)
        )

    # --------------------
    # Use case
    # --------------------

    use_case = None

    use_cases = [
        "machine learning",
        "deep learning",
        "data science",
        "gaming",
        "video editing",
        "programming",
        "coding",
        "development",
        "office",
        "student"
    ]

    for case in use_cases:

        if case in text:
            use_case = case
            break

    # --------------------
    # GPU
    # --------------------

    gpu_required = False

    gpu_use_cases = [
        "machine learning",
        "deep learning",
        "ai",
        "gaming",
        "video editing",
        "data science"
    ]

    if any(
        term in text
        for term in gpu_use_cases
    ):
        gpu_required = True

    # --------------------
    # Rating
    # --------------------

    minimum_rating = None

    rating_match = re.search(
        r"(\d(?:\.\d)?)\s*(?:star|rating)",
        text
    )

    if rating_match:

        minimum_rating = float(
            rating_match.group(1)
        )

    return ShoppingIntent(
        category=category,
        budget_max=budget,
        use_case=use_case,
        minimum_ram=minimum_ram,
        gpu_required=gpu_required,
        minimum_rating=minimum_rating,
        in_stock_only=True
    )


def extract_shopping_intent(
    message: str
) -> ShoppingIntent:

    prompt = f"""
{SYSTEM_PROMPT}

User message:
{message}
"""

    models = [
        settings.gemini_model,
        settings.gemini_fallback_model
    ]

    last_error = None

    for model_name in models:

        for attempt in range(2):

            try:

                response = (
                    client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                )

                raw_text = (
                    response.text
                    .strip()
                    .replace(
                        "```json",
                        ""
                    )
                    .replace(
                        "```",
                        ""
                    )
                    .strip()
                )

                data = json.loads(
                    raw_text
                )

                return ShoppingIntent(
                    **data
                )

            except Exception as exc:

                last_error = exc

                if attempt < 1:

                    time.sleep(
                        1
                    )

    print(
        "Gemini unavailable. "
        "Using local intent parser."
    )

    return local_intent_parser(
        message
    )
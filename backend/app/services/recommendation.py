from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.recommendation import RecommendationRequest


def extract_ram_gb(
    specifications: dict | None
) -> int | None:

    if not specifications:
        return None

    ram_value = specifications.get("ram")

    if not ram_value:
        return None

    if isinstance(ram_value, int):
        return ram_value

    text = str(ram_value).lower()

    digits = "".join(
        character
        for character in text
        if character.isdigit()
    )

    if not digits:
        return None

    return int(digits)


def has_gpu(
    specifications: dict | None
) -> bool:

    if not specifications:
        return False

    gpu = specifications.get("gpu")

    if not gpu:
        return False

    gpu_text = str(gpu).lower()

    integrated_terms = [
        "integrated",
        "intel uhd",
        "intel iris",
        "radeon graphics"
    ]

    return not any(
        term in gpu_text
        for term in integrated_terms
    )
    
def calculate_use_case_score(
    product: Product,
    use_case: str | None
) -> tuple[float, list[str]]:

    if not use_case:
        return 0, []

    use_case_text = use_case.lower()

    specifications = (
        product.specifications or {}
    )

    description = (
        product.description or ""
    ).lower()

    gpu_available = has_gpu(
        specifications
    )

    ram = extract_ram_gb(
        specifications
    )

    score = 0.0
    reasons = []

    if any(
        term in use_case_text
        for term in [
            "machine learning",
            "ai",
            "deep learning",
            "data science"
        ]
    ):

        if gpu_available:
            score += 8

            reasons.append(
                "Dedicated GPU is useful for AI/ML workloads"
            )

        if ram is not None and ram >= 16:
            score += 7

            reasons.append(
                "16GB or more RAM is suitable for AI/data workloads"
            )

    elif "gaming" in use_case_text:

        if gpu_available:
            score += 10

            reasons.append(
                "Dedicated GPU is suitable for gaming"
            )

        if ram is not None and ram >= 16:
            score += 5

            reasons.append(
                "Adequate RAM for gaming"
            )

    elif any(
        term in use_case_text
        for term in [
            "programming",
            "coding",
            "development"
        ]
    ):

        if ram is not None and ram >= 16:

            score += 10

            reasons.append(
                "RAM capacity is suitable for development workloads"
            )

        score += 5

        reasons.append(
            "Product is suitable for general development workloads"
        )

    elif any(
        term in use_case_text
        for term in [
            "office",
            "student",
            "browsing"
        ]
    ):

        score += 10

        reasons.append(
            "Suitable for everyday productivity"
        )

    elif any(
        term in use_case_text
        for term in [
            "video editing",
            "editing",
            "content creation"
        ]
    ):

        if gpu_available:

            score += 8

            reasons.append(
                "Dedicated GPU supports editing workloads"
            )

        if ram is not None and ram >= 16:

            score += 7

            reasons.append(
                "RAM capacity supports content creation"
            )

    return score, reasons
    
def calculate_product_score(
    product: Product,
    request: RecommendationRequest
) -> tuple[float, list[str]]:

    score = 0.0

    reasons = []

    # -------------------------
    # 1. Budget score
    # -------------------------

    product_price = Decimal(product.price)

    if product_price <= request.budget_max:

        score += 30

        reasons.append(
            "Fits within the requested budget"
        )

        budget_ratio = (
            product_price
            / request.budget_max
        )

        if budget_ratio >= Decimal("0.75"):

            score += 5

            reasons.append(
                "Uses the available budget efficiently"
            )

    else:
        return 0, [
            "Product exceeds the requested budget"
        ]

    # -------------------------
    # 2. Stock score
    # -------------------------

    if product.stock > 0:

        score += 10

        reasons.append(
            "Currently in stock"
        )

    elif request.in_stock_only:

        return 0, [
            "Product is out of stock"
        ]

    # -------------------------
    # 3. Rating score
    # -------------------------

    if product.rating is not None:

        rating_score = (
            float(product.rating) / 5
        ) * 15

        score += rating_score

        reasons.append(
            f"Customer rating: {product.rating}/5"
        )

    # -------------------------
    # 4. RAM score
    # -------------------------

    product_ram = extract_ram_gb(
        product.specifications
    )

    if request.minimum_ram is not None:

        if (
            product_ram is not None
            and product_ram >= request.minimum_ram
        ):

            score += 20

            reasons.append(
                f"Meets RAM requirement: {product_ram}GB"
            )

        else:

            reasons.append(
                "Does not meet the requested RAM requirement"
            )

    # -------------------------
    # 5. GPU score
    # -------------------------

    if request.gpu_required:

        if has_gpu(product.specifications):

            score += 15

            reasons.append(
                "Has a dedicated GPU"
            )

        else:

            reasons.append(
                "Dedicated GPU requirement not satisfied"
            )

    # -------------------------
    # 6. Minimum rating rule
    # -------------------------

    if request.minimum_rating is not None:

        if (
            product.rating is None
            or product.rating
            < request.minimum_rating
        ):

            return 0, [
                "Product does not meet minimum rating requirement"
            ]
            
            
            
    use_case_score, use_case_reasons = (
        calculate_use_case_score(
            product,
            request.use_case
        )
    )

    score += use_case_score
    reasons.extend(
        use_case_reasons
    )

    final_score = min(
    score,
    100
    )

    return round(
        final_score,
        2
    ), reasons
    
def recommend_products(
    db: Session,
    request: RecommendationRequest
):

    query = db.query(Product).filter(
        Product.category_id
        == request.category_id
    )

    query = query.filter(
        Product.is_active.is_(True)
    )

    query = query.filter(
        Product.price
        <= request.budget_max
    )

    if request.in_stock_only:

        query = query.filter(
            Product.stock > 0
        )

    products = query.all()

    scored_products = []

    for product in products:

        score, reasons = (
            calculate_product_score(
                product,
                request
            )
        )

        if score <= 0:
            continue

        scored_products.append(
            {
                "product_id": product.id,
                "name": product.name,
                "brand": product.brand,
                "price": product.price,
                "match_score": score,
                "reasons": reasons,
                "specifications": (
                    product.specifications
                )
            }
        )

    scored_products.sort(
        key=lambda item: item[
            "match_score"
        ],
        reverse=True
    )

    return scored_products    
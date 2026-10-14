from pydantic import BaseModel, Field, field_validator


class ShoppingIntent(BaseModel):
    category: str | None = None

    budget_max: float | None = Field(
        default=None,
        gt=0
    )

    use_case: str | None = None

    minimum_ram: int | None = Field(
        default=None,
        ge=1
    )
    
    @field_validator(
        "budget_max",
        mode="before"
    )
    @classmethod
    def parse_budget(cls, value):
        if value is None:
            return None

        if isinstance(value, (int, float)):
            return value

        text = str(value).lower().strip()

        text = text.replace(
            "₹",
            ""
        ).replace(
            ",",
            ""
        )

        if "lakh" in text:
            number = float(
                text.replace(
                    "lakh",
                    ""
                ).strip()
            )

            return number * 100000

        if text.endswith("k"):
            number = float(
                text[:-1]
            )

            return number * 1000

        return float(text)

    gpu_required: bool = False

    minimum_rating: float | None = Field(
        default=None,
        ge=0,
        le=5
    )

    in_stock_only: bool = True

    @field_validator(
        "minimum_ram",
        mode="before"
    )
    @classmethod
    def parse_ram(cls, value):
        if value is None:
            return None

        if isinstance(value, int):
            return value

        text = str(value).lower()

        digits = "".join(
            char for char in text
            if char.isdigit()
        )

        if not digits:
            return None

        return int(digits)


class IntentRequest(BaseModel):
    message: str = Field(
        min_length=2,
        max_length=1000
    )

# from pydantic import BaseModel, Field


# class ShoppingIntent(BaseModel):
#     category: str | None = None

#     budget_max: float | None = Field(
#         default=None,
#         gt=0
#     )

#     use_case: str | None = None

#     minimum_ram: int | None = Field(
#         default=None,
#         ge=1
#     )

#     gpu_required: bool = False

#     minimum_rating: float | None = Field(
#         default=None,
#         ge=0,
#         le=5
#     )

#     in_stock_only: bool = True
    
# class IntentRequest(BaseModel):
#     message: str = Field(
#         min_length=2,
#         max_length=1000
#     )    
from fastapi import APIRouter

from app.routes.categories import router as categories_router
from app.routes.database_test import router as database_test_router
from app.routes.health import router as health_router
from app.routes.merchants import router as merchants_router
from app.routes.products import router as products_router
from app.routes.test import router as test_router

from app.routes.recommendations import (
    router as recommendations_router
)


api_router = APIRouter(
    prefix="/api/v1"
)

api_router.include_router(health_router)
api_router.include_router(test_router)
api_router.include_router(database_test_router)

api_router.include_router(merchants_router)
api_router.include_router(categories_router)
api_router.include_router(products_router)
api_router.include_router(
    recommendations_router
)

# from fastapi import APIRouter

# from app.routes.health import router as health_router


# api_router = APIRouter(
#     prefix="/api/v1"
# )

# api_router.include_router(health_router)

# from fastapi import APIRouter

# from app.routes.health import router as health_router
# from app.routes.test import router as test_router


# api_router = APIRouter(
#     prefix="/api/v1"
# )

# api_router.include_router(health_router)
# api_router.include_router(test_router)






# from fastapi import APIRouter

# from app.routes.health import router as health_router
# from app.routes.test import router as test_router
# from app.routes.database_test import router as database_test_router


# api_router = APIRouter(
#     prefix="/api/v1"
# )

# api_router.include_router(health_router)
# api_router.include_router(test_router)
# api_router.include_router(database_test_router)
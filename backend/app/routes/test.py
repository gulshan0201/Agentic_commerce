from fastapi import APIRouter

router = APIRouter(
    prefix="/test",
    tags=["Testing"]
)


@router.get("")
def test_api():
    return {
        "success": True,
        "message": "Stage 2 API architecture is working"
    }
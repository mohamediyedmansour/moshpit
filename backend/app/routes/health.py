from fastapi import APIRouter, Response, status

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
@router.head("/health", status_code=status.HTTP_200_OK)
@router.options("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok"}

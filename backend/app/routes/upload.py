from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.status import HTTP_201_CREATED

router = APIRouter()


@router.post("/upload_video", status_code=HTTP_201_CREATED)
async def upload_video(file: UploadFile = File(...)):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Invalid video file")

    # intentionally do nothing for now
    return {
        "filename": file.filename,
        "content_type": file.content_type,
    }


@router.post("/upload_picture", status_code=HTTP_201_CREATED)
async def upload_picture(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")

    # intentionally do nothing for now
    return {
        "filename": file.filename,
        "content_type": file.content_type,
    }

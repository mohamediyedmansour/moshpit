from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.status import HTTP_201_CREATED
from fastapi.responses import Response

from app.mosh.video import mosh_video
from app.mosh.image import mosh_image

router = APIRouter()


@router.post("/upload_video", status_code=HTTP_201_CREATED)
async def upload_video(file: UploadFile = File(...)):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Invalid video file")

    original = await file.read()
    moshed = mosh_video(original)

    return Response(
        content=moshed,
        media_type=file.content_type,
        headers={
            "Content-Disposition": f'attachment; filename="moshed_{file.filename}"'
        },
    )


@router.post("/upload_picture", status_code=HTTP_201_CREATED)
async def upload_picture(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")

    original = await file.read()
    moshed = mosh_image(original)

    return Response(
        content=moshed,
        media_type=file.content_type,
        headers={
            "Content-Disposition": f'attachment; filename="moshed_{file.filename}"'
        },
    )

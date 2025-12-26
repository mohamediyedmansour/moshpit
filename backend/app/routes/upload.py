from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import Response
from starlette.status import HTTP_201_CREATED

from app.mosh.video import mosh_video
from app.mosh.image import mosh_image
from app.mosh.audio import mosh_audio

router = APIRouter()


@router.post("/upload_video", status_code=HTTP_201_CREATED)
async def upload_video(
    file: UploadFile = File(...),
    intensity: int = Query(5, ge=1, le=10),
):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Invalid video file")

    data = await file.read()
    moshed = mosh_video(data, intensity)

    return Response(
        content=moshed,
        media_type=file.content_type,
        headers={
            "Content-Disposition": f'attachment; filename="moshed_{file.filename}"'
        },
    )


@router.post("/upload_picture", status_code=HTTP_201_CREATED)
async def upload_picture(
    file: UploadFile = File(...),
    intensity: int = Query(5, ge=1, le=10),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")

    data = await file.read()
    moshed = mosh_image(data, intensity)

    return Response(
        content=moshed,
        media_type=file.content_type,
        headers={
            "Content-Disposition": f'attachment; filename="moshed_{file.filename}"'
        },
    )


@router.post("/upload_audio", status_code=HTTP_201_CREATED)
async def upload_audio(
    file: UploadFile = File(...),
    intensity: int = Query(5, ge=1, le=10),
):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Invalid audio file")

    data = await file.read()
    moshed = mosh_audio(data, intensity)

    return Response(
        content=moshed,
        media_type=file.content_type,
        headers={
            "Content-Disposition": f'attachment; filename="moshed_{file.filename}"'
        },
    )

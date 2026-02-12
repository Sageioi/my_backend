from datetime import datetime
from fastapi import FastAPI, APIRouter, File, UploadFile, Form, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import PostCreate, PostResponse
from app.models import Post,get_async_session
from app.images import imagekit
import shutil
import os
import uuid
import tempfile

routes = APIRouter()

@routes.post("/create_post")
async def create_post(file: UploadFile = File(...),caption: str = Form(""), session: AsyncSession = Depends(get_async_session)):
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)
        with open(temp_file_path, 'rb') as upload_file:
            upload_result = imagekit.files.upload(
                file=upload_file,
                file_name=file.filename,
                tags = ["backend_upload"],

            )


        if upload_result and hasattr(upload_result, 'url'):
            post = Post(
                caption=caption,
                url=upload_result.url,
                file_type="video" if "video" in file.content_type else "image",
                file_name=upload_result.name,
                created_at=datetime.now(),
            )
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post
        else:
            pass

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Upload Error: {str(error)}")

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()
@routes.get("/get_feed")
async def get_feed(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    post =  [row[0] for row in result.all()]
    post_data = []
    for post in post:
        post_data.append({
            "id": post.id,
            "caption": post.caption,
            "url": post.url,
            "file_name": post.file_name,
            "file_type": post.file_type,
            "created_at": post.created_at.isoformat(),
        })
    return post_data

@routes.delete("/delete_images")
async def delete_images(post_id ,session: AsyncSession = Depends(get_async_session)):
    try:
        post_id = uuid.UUID(post_id)
        result = await session.execute(select(Post).where(Post.id == post_id))
        post = result.scalars().first()
        await session.delete(post)
        await session.commit()

        return {"message":"Post Deleted Successfully"}
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Encountered an error when deleting : {str(error)}")



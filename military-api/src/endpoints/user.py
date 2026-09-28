from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException,Query,Response
from fastapi.responses import HTMLResponse
from fastapi import Query
from src.models.user import User_Base, User_Controller as user_controller   
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from io import BytesIO


router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}})


@router.get("/query_user")
async def query_user(keyword: str = Query(...)):
    try:
        user_ctrl = user_controller()
        result = await user_ctrl.query_user(keyword)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/set_user_position")
async def set_user_position(user_id: int = Query(...), position: str = Query(...)):
    try:
        user_ctrl = user_controller()
        result = user_ctrl.set_user_position(user_id, position)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add")
async def add_user(user: User_Base):
    try:
        user_ctrl = user_controller()
        result = user_ctrl.create_user(user)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.post("/login")
async def login_user(user_name: str = Query(...), password: str = Query(...)):
    try:
        user_ctrl = user_controller()
        result = await user_ctrl.login_system(user_name, password)
        if result:
            return {"status": "success", "data": result}
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/change_password")
async def change_password(
    user_name: str = Query(...),
    current_password: str = Query(...),
    new_password: str = Query(...),
):
    try:
        user_ctrl = user_controller()
        result = user_ctrl.change_password(user_name, current_password, new_password)
        if result.get("status") != "success":
            raise HTTPException(status_code=401, detail=result.get("message"))
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
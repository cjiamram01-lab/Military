from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException,Query,Response
from fastapi.responses import HTMLResponse
from fastapi import Query
from src.models.database_management import  DatabaseManagement_Controller
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from io import BytesIO


router = APIRouter(
    prefix="/database_management",
    tags=["database_management"],
    responses={404: {"description": "Not found"}})

@router.get("/get_column_names/{database_name}/{table_name}")
def get_column_names(database_name,table_name):
    db_control=DatabaseManagement_Controller()
    results=db_control.get_column_names(database_name,table_name)
    return results


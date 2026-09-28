from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException,Query,Response
from fastapi.responses import HTMLResponse
from fastapi import Query
from src.models.register import  Student_Base,Student_Controller as register_Controller
from src.models.militaryrequest import MilitaryRequest_Controller
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from io import BytesIO


router = APIRouter(
    prefix="/register",
    tags=["student_register"],
    responses={404: {"description": "Not found"}})


@router.post("/add")
async def add_student(student: Student_Base):
    try:
        register = register_Controller()
        result = register.add(student.dict())
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/update/{id}")
async def update_student(id: int, student: Student_Base):
    try:
        register = register_Controller()
        result = register.update(student.dict(), id)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/get_data/{id}")
async def get_student_data(id: int):
    try:
        register = register_Controller()
        result = register.get_data(id)
        if result:
            return {"status": "success", "data": result}
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/get_province")    
async def get_provinces():
    try:
        register = register_Controller()
        result = register.get_province()
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/get_district/{province_code}")
async def get_districts(province_code: str):
    try:
        register = register_Controller()
        result = register.get_district(province_code)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_department")
async def get_departments():
    try:
        register = register_Controller()
        result = register.get_department()
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_edulevel")
async def get_edulevels():
    try:
        register = register_Controller()
        result = register.get_edulevel()
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_studenttype")
async def get_studenttypes():
    try:
        register = register_Controller()
        result = register.get_studenttype()
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_ref_id_by_student_code/{studentCode}")
async def get_ref_id_by_student_code(studentCode: str):
    try:
        register = register_Controller()
        result = register.get_ref_id_by_student_code(studentCode)
        if result:
            return {"status": "success", "data": result}
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_data_by_student_code/{studentCode}")
async def get_student_data_by_code(studentCode: str):
    try:
        register = register_Controller()
        result = register.get_data_by_student_code(studentCode)
        if result:
            return {"status": "success", "data": result}
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    
@router.get("/get_register_by_id/{id}")
async def get_register_by_id(id: int):  
    try:
            register = register_Controller()
            result = register.get_register_by_id(id)
            if result:
                return {"status": "success", "data": result}
            else:
                raise HTTPException(status_code=404, detail="Register not found")
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
@router.get("/get_student_by_district/{province_code}/{district_code}/{birth_year}")
@router.get("/get_student_by_district/{province_code}/{birth_year}")
async def get_student_by_district(province_code: str, birth_year: str, district_code: str = ""):
    try:
        register = register_Controller()
        result = register.get_student_by_district(province_code, district_code, birth_year)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/is_exist/{studentCode}")
async def check_student_existence(studentCode: str):
    try:
        register = register_Controller()
        is_exist = register.is_exist(studentCode)
        return is_exist
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/migrate_student_soldier_from_nrru/{org_year}/{active_year}")
async def migrate_student_soldier_from_nrru(org_year: str, active_year: str):
    try:
        register = register_Controller()
        date_range = register.build_soldier_date_range(org_year=int(org_year), active_year=int(active_year))
        result = register.get_student_soldier_from_nrru(date_range["sDate"], date_range["fDate"], "M")

        military_request = MilitaryRequest_Controller()
        sync_result = military_request.sync_from_nrru_result(result, date_range["activeYear"])

        return {"status": "success", "data": sync_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
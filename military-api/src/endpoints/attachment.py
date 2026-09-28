from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, RedirectResponse

from src.models.attachment import Attachment_Controller


router = APIRouter(
    prefix="/attachment",
    tags=["attachment"],
    responses={404: {"description": "Not found"}},
)

@router.post("/upload")
async def upload_attachment(
    file: UploadFile = File(...),
    doc_type: str = Form(...),
    register_id: int = Form(...),
):
    try:
        return await Attachment_Controller().upload(file, doc_type, register_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.get("/get_document_types")
async def get_document_types():
    try:
        result = Attachment_Controller().get_document_types()
        return {"status": "success", "data": result}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.get("/get_attachments_by_register_id/{register_id}")
async def get_attachments_by_register_id(register_id: int):
    try:
        result = Attachment_Controller().get_attachments_by_register_id(register_id)
        return {"status": "success", "data": result}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.delete("/delete_by_id/{id}")
async def delete_by_id(id: int):
    try:
        result = Attachment_Controller().delete_by_id(id)
        return {"status": "success", "data": result}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.get("/get_file/{register_id}/{doc_type}")
async def get_file(register_id: int, doc_type: str):
    try:
        result = Attachment_Controller().get_file(register_id, doc_type)
        if not result:
            raise HTTPException(status_code=404, detail="Attachment not found")

        if result["is_url"]:
            return RedirectResponse(result["location"])

        file_path = result["location"]
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(file_path)
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

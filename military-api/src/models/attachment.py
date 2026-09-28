from datetime import date
import glob
import json
from pathlib import Path
import re
from typing import Optional

from pydantic import BaseModel

from src.util.dbcontroller import DBController as DB

MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB


def _route_storage():
	# Base URL of the attachment/get_file endpoint, e.g. ".../attachment/get_file/"
	with open('././config/config.json') as file:
		return json.load(file)["route_storage"]


def _local_file(file_name):
	"""Disk path for a stored fileName, or None when it points at an external URL.

	fileName is either a path under uploads/ or a route_storage URL
	(<route_storage><register_id>/<doc_type>) which has no extension, so the
	uploaded file is found by matching "<register_id>-<doc_type>.*" (current naming)
	or "<doc_type>.*" (older uploads) in uploads/<register_id>/.
	"""
	base = _route_storage()
	if file_name.startswith(base):
		register_id, _, doc_type = file_name[len(base):].partition("/")
		folder = Path("uploads") / register_id
		for stem in (f"{register_id}-{doc_type}", doc_type):
			matches = sorted(glob.glob(glob.escape(str(folder / stem)) + ".*"))
			if matches:
				return Path(matches[0])
		return None
	if file_name.startswith("http://") or file_name.startswith("https://"):
		return None
	return Path("uploads") / file_name


class Attachment_Base(BaseModel):
	id: Optional[int] = None
	fileName: Optional[str] = None
	docType: Optional[str] = None
	registerId: Optional[int] = None


class Attachment_Controller:
	__tablename__ = "t_attachment"

	def __init__(self):
		self.__tableName__ = "t_attachment"

	async def add(self, attachment):
		db = DB(self.__tableName__)
		result = db.create(attachment)
		del db
		return result

	async def delete_id(self, register_id, doc_type):
		db = DB(self.__tableName__)
		sql = f"SELECT id, fileName FROM {self.__tableName__} WHERE registerId = %s AND docType = %s"
		rows = db.get_specific_sql(sql, ["id", "fileName"], (register_id, doc_type))
		for row in rows:
			file_path = _local_file(row["fileName"])
			if file_path and file_path.exists():
				file_path.unlink()
			db.delete(row["id"])
		del db
		return {"deleted": len(rows)}

	async def upload(self, file, doc_type, register_id):
		current_date = date.today().isoformat()
		safe_doc_type = re.sub(r"[^A-Za-z0-9_-]", "_", doc_type).strip("_")
		if not safe_doc_type:
			raise ValueError("doc_type is required")

		extension = Path(file.filename or "").suffix
		file_name = f"{register_id}-{safe_doc_type}{extension}"
		upload_directory = Path("uploads") / str(register_id)
	
		upload_directory.mkdir(parents=True, exist_ok=True)
		file_location = f"{_route_storage()}{register_id}/{safe_doc_type}"
		file_path = upload_directory/ file_name
  


		try:
			content = await file.read()
			if len(content) > MAX_UPLOAD_SIZE:
				raise ValueError("File size must not exceed 5 MB")

			await self.delete_id(register_id, doc_type)
			file_path.write_bytes(content)
			attachment = {
				"fileName": f"""{register_id}/{file_name}""",
				"docType": doc_type,
				"registerId": register_id,
			}
			result = await self.add(attachment)
		except Exception:
			if file_path.exists():
				file_path.unlink()
			raise
		finally:
			await file.close()

		return {
			"status": "success",
			"fileName": f"""{register_id}/{file_name}""",
			"docType": doc_type,
			"registerId": register_id,
			"current_date": current_date,
			"data": result,
		}

	def delete_by_id(self, id):
		db = DB(self.__tableName__)
		sql = f"SELECT id, fileName FROM {self.__tableName__} WHERE id = %s"
		rows = db.get_specific_sql(sql, None, (id,))
		for row in rows:
			file_path = _local_file(row["fileName"])
			if file_path and file_path.exists():
				file_path.unlink()
			db.delete(row["id"])
		del db
		return {"deleted": len(rows)}

	def update(self, attachment, id):
		db = DB(self.__tableName__)
		result = db.update(attachment, id)
		del db
		return result

	def delete(self, id):
		db = DB(self.__tableName__)
		result = db.delete(id)
		del db
		return result

	def get_data(self, id):
		db = DB(self.__tableName__)
		fields = ["id", "fileName", "docType", "registerId"]
		result = db.get_data(fields, id)
		del db
		return result

	def get_document_types(self):
		db = DB()
		sql = "SELECT code AS code, description AS name FROM t_documenttype ORDER BY id"
		result = db.get_specific_sql(sql, ["code", "name"])
		del db
		return result

	def get_attachments_by_register_id(self, register_id):
		db = DB(self.__tableName__)
		sql = "SELECT * FROM t_attachment WHERE registerId = %s"
		results = db.get_specific_sql(sql, None, (register_id,))
		del db
		return results

	def get_file(self, register_id, doc_type):
		db = DB(self.__tableName__)
		sql = f"SELECT fileName FROM {self.__tableName__} WHERE registerId = %s AND docType = %s"
		result = db.get_specific_sql(sql, ["fileName"], (register_id, doc_type))
		del db
		if not result:
			return None

		file_name = result[0]["fileName"]
		file_path = _local_file(file_name)
		print(file_path)
		if file_path is None:
			# route_storage URLs whose file is gone, and external URLs. Redirecting the
			# former would loop back into this endpoint, so only real external URLs redirect.
			if file_name.startswith(_route_storage()):
				return None
			return {"is_url": True, "location": file_name}

		return {"is_url": False, "location": file_path}

	def get_attachment(self, id, register_id):
		db = DB(self.__tableName__)
		sql = "SELECT * FROM t_attachment WHERE id = %s AND registerId = %s"
		results = db.get_specific_sql(sql, None, (id, register_id))
		del db
		if results:
			return results[0]
		else:
			return None
		

from pydantic import BaseModel
from datetime import  datetime
from src.util.dbcontroller import DBController as DB
from src.util.utility import Util
from typing import List, Optional
import json
from urllib.parse import quote
import requests
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

NRRU_STUDENT_SOLDIER_ENDPOINT = "https://entrance.nrru.ac.th/nrruwebservice/nrruWebService_studentSoldier.php"
NRRU_STUDENT_SOLDIER_NAMESPACE = "http://entrance.nrru.ac.th/soap/studentSoldier"
NRRU_STUDENT_SOLDIER_SOAP_ACTION = f"{NRRU_STUDENT_SOLDIER_ENDPOINT}/studentSoldier"




class Student_Base(BaseModel):
    id: int
    studentCode: str
    studentName: str
    personalId: str
    birthYear: int
    age: int
    street: Optional[str] = None
    homeNo: Optional[str] = None
    mooNo: Optional[str] = None
    subDistrict: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    postalCode: Optional[str] = None
    fatherName: Optional[str] = None
    motherName: Optional[str] = None
    description: Optional[str] = None
    fatherTel: Optional[str] = None
    motherTel: Optional[str] = None
    birthDate: datetime = datetime.now()
    departmentCode: Optional[str] = None
    telNo: Optional[str] = None
    eduLevel: Optional[str] = None
    eduProgram: Optional[str] = None
    registYear: Optional[str] = None
    eduType: Optional[str] = None
    everRequest: Optional[bool] = None
    everSchool: Optional[bool] = None
    isAprove: Optional[bool] = None

class Student_Controller():
    __tablename__ = 't_register'

    def __init__(self):
        self.__tableName__ = 't_register'

    def add(self, student):
        db = DB(self.__tableName__)
        result = db.create(student)
        del db
        return result

    def update(self, student, id):
        db = DB(self.__tableName__)
        result = db.update(student, id)
        del db
        return result

    def delete(self, id):
        db = DB(self.__tableName__)
        result = db.delete(id)
        del db
        return result
    
    def is_exist(self, studentCode):
        db = DB()
        sql="SELECT id FROM t_register WHERE studentCode = %s"
        result = db.get_specific_sql(sql, None,(studentCode,))
        del db
        return {"status": len(result) > 0}
    
    def get_province(self):
        db = DB()
        sql = "SELECT DISTINCT code AS code, prvName_Th AS name FROM province ORDER BY prvName_Th"
        result = db.get_specific_sql(sql, ["code", "name"])
        del db
        return result
    
    @staticmethod
    def _route_storage():
        # Base URL of the attachment/get_file endpoint, e.g. ".../attachment/get_file/"
        with open('././config/config.json') as file:
            return json.load(file)["route_storage"]

    def get_file_attachment(self,register_id,db=None):
        # Pass an open `db` to reuse its connection when calling this in a loop.
        own_db = db is None
        if own_db:
            db=DB()
        sql=f"""SELECT 
            A.fileName AS file_name,
            C.`description` AS document_type,
            A.docType AS doc_type
        FROM t_attachment A INNER JOIN `t_register` B 
        ON A.`registerId`=B.id INNER JOIN 
        `t_documenttype` C ON A.`docType`=C.`code` WHERE A.registerId=%s  """
        results=db.get_specific_sql(sql,None,(register_id,))
        if own_db:
            del db
        # Serve every file through the storage route; get_file redirects legacy full-URL rows.
        base = self._route_storage()
        for item in results:
            item["file_name"] = f"{base}{register_id}/{quote(str(item.pop('doc_type')), safe='')}"
        return results

    def get_student_by_district(self, province_code, district_code, birth_year):
        db = DB()
        sql = f"""SELECT 
					A.studentCode,
					A.id AS registerId,
					D.personalId,
					A.studentName,
					A.`birthYear`,
					A.`street`,
					A.`homeNo`,
					A.`mooNo`,
					A.`subDistrict`,
					A.`postalCode`,
					A.`fatherName`,
					A.`motherName`,
					B.`disName_Th` AS districtName,
					B.`code` AS districtCode,
					C.prvName_Th AS provinceName,
					C.`code` AS provinceCode,
					A.`postalCode`

			 FROM  t_register A INNER JOIN `district` B 
			 ON A.`district` =B.`code` INNER JOIN `province` C
			 ON A.`province` =C.`code` INNER JOIN t_register D 
			 ON A.studentCode=D.studentCode 
			 WHERE C.code =%s 
			 AND B.code LIKE %s
			 AND A.birthYear=%s
			 AND A.isAprove=0
        """
        district_code = district_code or "%"
        results = db.get_specific_sql(sql, None, (province_code, district_code, birth_year))
        for row in results:
            row["attachments"] = self.get_file_attachment(row["registerId"], db)
        del db
        
        
        return results

    def get_district(self, province_code):
        db = DB()
        sql = "SELECT code AS code, disName_Th AS name FROM district WHERE prv_Code = %s ORDER BY disName_Th"
        result = db.get_specific_sql(sql, ["code", "name"], (province_code,))
        del db
        return result

    def get_department(self):
        db = DB()
        sql = "SELECT departmentcode AS code, departmentName AS name FROM t_department WHERE isFaculty = 1 ORDER BY departmentName"
        result = db.get_specific_sql(sql, ["code", "name"])
        del db
        return result

    def get_edulevel(self):
        db = DB()
        sql = "SELECT code AS code, eduLevel AS name FROM t_edulevel ORDER BY id"
        result = db.get_specific_sql(sql, ["code", "name"])
        del db
        return result

    def get_studenttype(self):
        db = DB()
        sql = "SELECT code AS code, studentType AS name FROM t_studenttype ORDER BY id"
        result = db.get_specific_sql(sql, ["code", "name"])
        del db
        return result
    
    def get_data_by_student_code(self, studentCode):
        db = DB(self.__tableName__)
        sql="SELECT * FROM t_register WHERE studentCode = %s"
        result = db.get_specific_sql(sql, None,(studentCode,))
        del db
        return result[0] if result else None
    
    def get_ref_id_by_student_code(self, studentCode):
        db = DB(self.__tableName__)
        sql="SELECT id FROM t_register WHERE studentCode = %s"
        result = db.get_specific_sql(sql, None,(studentCode,))
        del db
        return result[0]["id"] if result else None
    
    def get_register_by_id(self, id):
        db = DB(self.__tableName__)
        sql=f"""SELECT  A.id,
			A.studentCode,
			A.studentName,
			A.personalId,
			A.birthDate,
			A.age,
			A.street,
			A.homeNo,
			A.mooNo,
			A.subDistrict,
			B.disName_TH AS district,
			C.prvName_TH AS province,
			A.postalCode,
			A.fatherName,
			A.motherName,
			A.fatherTel,
			A.motherTel,
			A.eduLevel,
			A.eduProgram,
			A.registYear,
			A.eduType,
			A.departmentCode,
			A.everRequest,
			A.everSchool,
			A.telNo,
			A.registYear
		FROM t_register A  LEFT OUTER JOIN district B 
		ON A.district=B.code LEFT OUTER JOIN province C 
		ON A.province=C.code 
		 WHERE A.id=%s"""
        result = db.get_specific_sql(sql, None,(id,))
        del db
        return result[0] if result else None

    def get_data(self, id):
        db = DB(self.__tableName__)
        fields = [
            "id",
            "studentCode",
            "studentName",
            "personalId",
            "birthYear",
            "age",
            "street",
            "homeNo",
            "mooNo",
            "subDistrict",
            "district",
            "province",
            "postalCode",
            "fatherName",
            "motherName",
            "description",
            "fatherTel",
            "motherTel",
            "birthDate",
            "departmentCode",
            "telNo",
            "eduLevel",
            "eduProgram",
            "registYear",
            "eduType"
        ]
        result = db.get_data(fields, id)
        del db
        return result
    
    def build_soldier_date_range(self, org_year: Optional[str] = None, active_year: Optional[str] = None) -> dict:
        """Mirror of the PHP orgYear/activeYear/sDate/fDate derivation."""
        current_year = datetime.now().year

        org_year = (int(org_year) - 543) if org_year is not None else (current_year - 543)
        active_year = int(active_year) if active_year is not None else (current_year + 543)

        s_date = f"{org_year}/01/01"
        f_date = f"{org_year}/12/31"

        return {
            "orgYear": org_year,
            "activeYear": active_year,
            "sDate": s_date,
            "fDate": f_date,
        }


    def get_student_soldier_from_nrru(self, birthdatefrom: str, birthdateto: str, studentsex: str = "M") -> list:
        """Call the NRRU studentSoldier SOAP (rpc/encoded) service and return the decoded student list.

        The service's nusoap-generated WSDL declares its soap:body with an empty
        namespace attribute, which trips up zeep's strict binding parser
        ("Empty tag name"). The envelope is built by hand instead, bypassing
        WSDL parsing entirely for this single, simple operation.
        """
        envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/">
  <SOAP-ENV:Body>
    <tns:studentSoldier xmlns:tns="{NRRU_STUDENT_SOLDIER_NAMESPACE}" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
      <birthdatefrom xsi:type="xsd:string">{escape(birthdatefrom)}</birthdatefrom>
      <birthdateto xsi:type="xsd:string">{escape(birthdateto)}</birthdateto>
      <studentsex xsi:type="xsd:string">{escape(studentsex)}</studentsex>
    </tns:studentSoldier>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

        response = requests.post(
            NRRU_STUDENT_SOLDIER_ENDPOINT,
            data=envelope.encode("utf-8"),
            headers={
                "Content-Type": "text/xml; charset=UTF-8",
                "SOAPAction": NRRU_STUDENT_SOLDIER_SOAP_ACTION,
            },
            timeout=30,
        )
        response.raise_for_status()

        root = ET.fromstring(response.content)
        return_el = root.find(".//return")
        if return_el is None or not return_el.text:
            return []

        return json.loads(return_el.text)



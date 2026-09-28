from pydantic import BaseModel
from datetime import datetime
from src.util.dbcontroller import DBController as DB
from typing import Optional


class MilitaryRequest_Base(BaseModel):
    id: Optional[int] = None
    studentCode: Optional[str] = None
    birthDate: Optional[datetime] = None
    activeYear: Optional[int] = None
    fullName: Optional[str] = None
    divisionCode: Optional[str] = None
    divisioncodename: Optional[str] = None
    levelcode: Optional[str] = None
    levelcodename: Optional[str] = None
    facultyid: Optional[int] = None
    facultyname: Optional[str] = None
    programid: Optional[int] = None
    programname: Optional[str] = None
    admitacadyear: Optional[str] = None


class MilitaryRequest_Controller():
    __tablename__ = 't_militaryrequest'

    def __init__(self):
        self.__tableName__ = 't_militaryrequest'

    def create(self, record):
        db = DB(self.__tableName__)
        result = db.create(record)
        del db
        return result

    def update(self, record, id):
        db = DB(self.__tableName__)
        result = db.update(record, id)
        del db
        return result

    def is_exist(self, studentCode, activeYear):
        db = DB()
        sql = "SELECT id FROM t_militaryrequest WHERE studentCode = %s AND activeYear = %s"
        result = db.get_specific_sql(sql, None, (studentCode, activeYear))
        del db
        return len(result) > 0

    def get_id(self, studentCode, activeYear):
        db = DB()
        sql = "SELECT id FROM t_militaryrequest WHERE studentCode = %s AND activeYear = %s"
        result = db.get_specific_sql(sql, None, (studentCode, activeYear))
        del db
        return result[0]["id"] if result else None

    @staticmethod
    def _map_nrru_row(row: dict, active_year: int) -> dict:
        """Map one row from get_student_soldier_from_nrru() to t_militaryrequest columns."""
        full_name = " ".join(
            part for part in (
                row.get("prefixname"),
                row.get("studentname"),
                row.get("studentsurname"),
            ) if part
        )

        return {
            "studentCode": row.get("studentcode"),
            "birthDate": row.get("birthdate"),
            "activeYear": active_year,
            "fullName": full_name,
            "divisionCode": row.get("divisioncode"),
            "divisioncodename": row.get("divisioncodename"),
            "levelcode": row.get("levelcode"),
            "levelcodename": row.get("levelcodename"),
            "facultyid": row.get("facultyid"),
            "facultyname": row.get("facultyname"),
            "programid": row.get("programid"),
            "programname": row.get("programname"),
            "admitacadyear": row.get("admitacadyear"),
        }

    def sync_from_nrru_result(self, result: list, active_year: int) -> dict:
        """Upsert each NRRU studentSoldier row into t_militaryrequest.

        Mirrors the create/update loop in getStudentFromMIS.php: a row is
        inserted if no record exists yet for (studentCode, activeYear),
        otherwise the existing record is updated.
        """
        history = []

        for row in result:
            student_code = row.get("studentcode")
            record = self._map_nrru_row(row, active_year)

            existing_id = self.get_id(student_code, active_year)
            if existing_id is None:
                outcome = self.create(record)
                history.append({
                    "studentCode": student_code,
                    "activeYear": active_year,
                    "action": "create",
                    "result": outcome,
                })
            else:
                outcome = self.update(record, existing_id)
                history.append({
                    "studentCode": student_code,
                    "activeYear": active_year,
                    "action": "update",
                    "result": outcome,
                })

        return {"history": history, "message": True}

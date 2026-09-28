from pydantic import BaseModel
from datetime import  datetime
from src.util.dbcontroller import DBController as DB
from src.util.utility import Util
from typing import List, Optional

class DatabaseManagement_Controller():
    def get_column_names(self,database_name,table_name):
        db = DB()
        sql = f"""SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = '{table_name}'
            AND TABLE_SCHEMA = '{database_name}'
            ORDER BY ORDINAL_POSITION;"""
        results = db.get_specific_sql(sql)

        column_names = []
        for item in results:
            column_name = item["COLUMN_NAME"]
            if column_name not in column_names:
                column_names.append(column_name)

        # Format as a string with curly braces
        formatted_output = "{" + ",".join(f'"{name}"' for name in column_names) + "}"

        del db
        return column_names
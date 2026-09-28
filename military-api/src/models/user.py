from ast import keyword
import hashlib
import os
import tempfile
from typing import Optional
from urllib.parse import quote

import certifi
import requests
from pydantic import BaseModel

from src.util.dbcontroller import DBController as DB

NRRU_CREDENTIAL_URL = "https://cos.nrru.ac.th/NRRUCredential/NRRUCredential1.php"

# cos.nrru.ac.th's web server does not send its intermediate certificate
# (Sectigo Public Server Authentication CA DV R36), so plain certifi/OpenSSL
# cannot build a trust chain to it ("unable to get local issuer certificate").
# We supply the missing intermediate ourselves rather than disabling TLS
# verification, since this endpoint receives the password in the URL.
_NRRU_INTERMEDIATE_CERT = """-----BEGIN CERTIFICATE-----
MIIGTDCCBDSgAwIBAgIQOXpmzCdWNi4NqofKbqvjsTANBgkqhkiG9w0BAQwFADBf
MQswCQYDVQQGEwJHQjEYMBYGA1UEChMPU2VjdGlnbyBMaW1pdGVkMTYwNAYDVQQD
Ey1TZWN0aWdvIFB1YmxpYyBTZXJ2ZXIgQXV0aGVudGljYXRpb24gUm9vdCBSNDYw
HhcNMjEwMzIyMDAwMDAwWhcNMzYwMzIxMjM1OTU5WjBgMQswCQYDVQQGEwJHQjEY
MBYGA1UEChMPU2VjdGlnbyBMaW1pdGVkMTcwNQYDVQQDEy5TZWN0aWdvIFB1Ymxp
YyBTZXJ2ZXIgQXV0aGVudGljYXRpb24gQ0EgRFYgUjM2MIIBojANBgkqhkiG9w0B
AQEFAAOCAY8AMIIBigKCAYEAljZf2HIz7+SPUPQCQObZYcrxLTHYdf1ZtMRe7Yeq
RPSwygz16qJ9cAWtWNTcuICc++p8Dct7zNGxCpqmEtqifO7NvuB5dEVexXn9RFFH
12Hm+NtPRQgXIFjx6MSJcNWuVO3XGE57L1mHlcQYj+g4hny90aFh2SCZCDEVkAja
EMMfYPKuCjHuuF+bzHFb/9gV8P9+ekcHENF2nR1efGWSKwnfG5RawlkaQDpRtZTm
M64TIsv/r7cyFO4nSjs1jLdXYdz5q3a4L0NoabZfbdxVb+CUEHfB0bpulZQtH1Rv
38e/lIdP7OTTIlZh6OYL6NhxP8So0/sht/4J9mqIGxRFc0/pC8suja+wcIUna0HB
pXKfXTKpzgis+zmXDL06ASJf5E4A2/m+Hp6b84sfPAwQ766rI65mh50S0Di9E3Pn
2WcaJc+PILsBmYpgtmgWTR9eV9otfKRUBfzHUHcVgarub/XluEpRlTtZudU5xbFN
xx/DgMrXLUAPaI60fZ6wA+PTAgMBAAGjggGBMIIBfTAfBgNVHSMEGDAWgBRWc1hk
lfmSGrASKgRieaFAFYghSTAdBgNVHQ4EFgQUaMASFhgOr872h6YyV6NGUV3LBycw
DgYDVR0PAQH/BAQDAgGGMBIGA1UdEwEB/wQIMAYBAf8CAQAwHQYDVR0lBBYwFAYI
KwYBBQUHAwEGCCsGAQUFBwMCMBsGA1UdIAQUMBIwBgYEVR0gADAIBgZngQwBAgEw
VAYDVR0fBE0wSzBJoEegRYZDaHR0cDovL2NybC5zZWN0aWdvLmNvbS9TZWN0aWdv
UHVibGljU2VydmVyQXV0aGVudGljYXRpb25Sb290UjQ2LmNybDCBhAYIKwYBBQUH
AQEEeDB2ME8GCCsGAQUFBzAChkNodHRwOi8vY3J0LnNlY3RpZ28uY29tL1NlY3Rp
Z29QdWJsaWNTZXJ2ZXJBdXRoZW50aWNhdGlvblJvb3RSNDYucDdjMCMGCCsGAQUF
BzABhhdodHRwOi8vb2NzcC5zZWN0aWdvLmNvbTANBgkqhkiG9w0BAQwFAAOCAgEA
YtOC9Fy+TqECFw40IospI92kLGgoSZGPOSQXMBqmsGWZUQ7rux7cj1du6d9rD6C8
ze1B2eQjkrGkIL/OF1s7vSmgYVafsRoZd/IHUrkoQvX8FZwUsmPu7amgBfaY3g+d
q1x0jNGKb6I6Bzdl6LgMD9qxp+3i7GQOnd9J8LFSietY6Z4jUBzVoOoz8iAU84OF
h2HhAuiPw1ai0VnY38RTI+8kepGWVfGxfBWzwH9uIjeooIeaosVFvE8cmYUB4TSH
5dUyD0jHct2+8ceKEtIoFU/FfHq/mDaVnvcDCZXtIgitdMFQdMZaVehmObyhRdDD
4NQCs0gaI9AAgFj4L9QtkARzhQLNyRf87Kln+YU0lgCGr9HLg3rGO8q+Y4ppLsOd
unQZ6ZxPNGIfOApbPVf5hCe58EZwiWdHIMn9lPP6+F404y8NNugbQixBber+x536
WrZhFZLjEkhp7fFXf9r32rNPfb74X/U90Bdy4lzp3+X1ukh1BuMxA/EEhDoTOS3l
7ABvc7BYSQubQ2490OcdkIzUh3ZwDrakMVrbaTxUM2p24N6dB+ns2zptWCva6jzW
r8IWKIMxzxLPv5Kt3ePKcUdvkBU/smqujSczTzzSjIoR5QqQA6lN1ZRSnuHIWCvh
JEltkYnTAH41QJ6SAWO66GrrUESwN/cgZzL4JLEqz1Y=
-----END CERTIFICATE-----
"""


def _nrru_ca_bundle():
	bundle_path = os.path.join(tempfile.gettempdir(), "nrru_ca_bundle.pem")
	if not os.path.exists(bundle_path):
		with open(certifi.where(), "r", encoding="utf-8") as f:
			bundle = f.read()
		with open(bundle_path, "w", encoding="utf-8") as f:
			f.write(bundle)
			f.write("\n")
			f.write(_NRRU_INTERMEDIATE_CERT)
	return bundle_path


class User_Base(BaseModel):
	id: Optional[int] = None
	UserName: Optional[str] = None
	Password: Optional[str] = None
	FullName: Optional[str] = None
	Picture: Optional[str] = None
	UserCode: Optional[str] = None
	DepartmentId: Optional[str] = None
	position: Optional[str] = None
	telNo: Optional[str] = None
	email: Optional[str] = None
	lineNo: Optional[str] = None
	facebook: Optional[str] = None
 
class User_Login(BaseModel):
    UserName: str
    Password: str


class User_Controller:
	__tablename__ = "t_user"

	def __init__(self):
		self.__tableName__ = "t_user"

	def add(self, user:User_Login):
		db = DB(self.__tableName__)
		user_data = user.dict()
		user_data["Password"] = hashlib.md5(
			user_data["Password"].encode("utf-8")
		).hexdigest()
		result = db.create(user_data)
		del db
		return result

	def create_user(self, user_login):
		db = DB(self.__tableName__)
		user_data = user_login.dict() if isinstance(user_login, BaseModel) else dict(user_login)
		user_data["Password"] = hashlib.md5(
			user_data["Password"].encode("utf-8")
		).hexdigest()
		result = db.create(user_data)
		del db
		return result


	async def query_user(self, keyword):
		db = DB(self.__tableName__)
		sql = f"""SELECT 
			id,
			UserName AS username,
			FullName AS fullname,
			picture AS picture,
			'' AS description,
			position
		FROM t_user WHERE UserName LIKE %s OR FullName LIKE %s"""
		result = db.get_specific_sql(
			sql, None, (f"%{keyword}%", f"%{keyword}%")
		)
		del db
		return result


	async def login_system(self, username, password):
		db = DB()
		sql = f"""SELECT 
			UserName AS username,
			FullName AS fullname,
			picture AS picture,
			'' AS description,
			position,
			role
  		FROM t_user WHERE UserName = %s AND password = %s"""
		params=(username, hashlib.md5(password.encode("utf-8")).hexdigest())
		print(params)
		result = db.get_specific_sql(
			sql,
			None,
			params,
		)
		del db
		if not result:
			result = await self.login_mis(username, password)
			if result is None:
				return {"status": "error", "message": "Invalid username or password"}
		return result


	def _is_valid_user(self, username):
		db = DB()
		sql = f"SELECT id FROM {self.__tableName__} WHERE UserName = %s"
		result = db.get_specific_sql(sql, ["id"], (username,))
		del db
		return bool(result)

	def _set_password(self, username, password):
		db = DB()
		sql = f"UPDATE {self.__tableName__} SET Password = %s WHERE UserName = %s"
		result = db.set_specific_sql(sql, (hashlib.md5(password.encode("utf-8")).hexdigest(), username))
		del db
		return result

	async def login_mis(self, username, password):
		url = (
			f"{NRRU_CREDENTIAL_URL}"
			f"?userName={quote(str(username), safe='')}"
			f"&password={quote(str(password), safe='')}"
		)
		
		try:
			response = requests.get(url, timeout=10, verify=_nrru_ca_bundle())

			data = response.json()
		except (requests.RequestException, ValueError) as e:
			print(f"login_mis error: {e}")
			return None

		if not isinstance(data, list) or not data:
			return None

		o = data[0]
		if self._to_int(o.get("status")) <= 0:
			return None

		self._sync_nrru_user(o, password)

		return {
			"id": self._to_int(o.get("staffid")),
			"username": o.get("username") or username,
			"fullname": self._build_name(o),
			"picture": o.get("picture") or "",
			"description": o.get("departmentname") or "",
			"position": "user",
		}

	@staticmethod
	def _to_int(value, default=0):
		try:
			return int(value)
		except (TypeError, ValueError):
			return default

	@staticmethod
	def _build_name(o):
		# Matches the FullName built by the existing PHP NRRU flows
		# (credentialReceive.php / callbackAuthen.php): firstname + lastname.
		return f"{o.get('firstname') or ''} {o.get('lastname') or ''}".strip()

	
 
	def _sync_nrru_user(self, o, password):
		db = DB(self.__tableName__)
		user_name = o.get("username") or ""
		existing = db.get_specific_sql(
			"SELECT * FROM t_user WHERE UserName = %s",
			None,
			(user_name,),
		)

		if self._is_valid_user(user_name):
			self._set_password(user_name, password)
			user_record = existing[0] if existing else None
			if user_record:
				user_record.pop("Password", None)
			del db
			return user_record
		else:
			fields = {
				"UserName": user_name,
				"UserCode": user_name,
				"FullName": self._build_name(o),
				"Picture": o.get("picture") or "",
				"DepartmentId": o.get("departmentcode1") or o.get("departmentcode2") or ""
			}
			if existing:
				fields["Password"] = hashlib.md5(password.encode("utf-8")).hexdigest()
				result = db.update(fields, existing[0]["id"])
			else:
				fields["Password"] = hashlib.md5(password.encode("utf-8")).hexdigest()
				result = self.create_user(fields)
			del db
			return result

	def change_password(self, username, current_password, new_password):
		db = DB(self.__tableName__)
		sql = f"SELECT id FROM {self.__tableName__} WHERE UserName = %s AND Password = %s"
		current_hash = hashlib.md5(current_password.encode("utf-8")).hexdigest()
		result = db.get_specific_sql(sql, ["id"], (username, current_hash))
		if not result:
			del db
			return {"status": "error", "message": "Current password is incorrect"}

		new_hash = hashlib.md5(new_password.encode("utf-8")).hexdigest()
		db.update({"Password": new_hash}, result[0]["id"])
		del db
		return {"status": "success"}

	def update(self, user, id):
		db = DB(self.__tableName__)
		result = db.update(user, id)
		del db
		return result

	def set_user_position(self, user_id, position):
		db = DB(self.__tableName__)
		result = db.update({"position": position}, user_id)
		del db
		return result

	def delete(self, id):
		db = DB(self.__tableName__)
		result = db.delete(id)
		del db
		return result

	def get_data(self, id):
		db = DB(self.__tableName__)
		fields = [
			"id",
			"UserName",
			"Password",
			"FullName",
			"Picture",
			"UserCode",
			"DepartmentId",
			"position",
			"telNo",
			"email",
			"lineNo",
			"facebook",
		]
		result = db.get_data(fields, id)
		del db
		return result


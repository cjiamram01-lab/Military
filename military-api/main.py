import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes.api import router as api_router

app = FastAPI()

origins = ["https://cos.nrru.ac.th","http://localhost:5173","http://0.0.0.0:5173"]

# CLIENT_ID = os.getenv('25133f28f9e842998a662eb4b935cf2a')
# TENANT_ID = os.getenv('8b060fcf-29fd-4b25-a613-c4712345cfd9')
# AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
# SCOPE = ['User.Read']

app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"],
     allow_credentials=True,
     allow_methods=["*"],  # HTTP methods to allow
     allow_headers=["*"]
)

app.include_router(api_router)
if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, log_level="info",reload=True)#Developer code
    # command: uvicorn app.main:app --host 0.0.0.0
    #**********Production********************************
    #uvicorn.run(app, host="0.0.0.0", port=8000)  make for production code
    #bash uvicorn main:app --reload
    # Security SSL isAuthen
    #uvicorn.run("main:app", host='0.0.0.0', port=4000, log_level="info", ssl_keyfile="/certs/apache.key", ssl_certfile="/certs/fullchain.crt",   reload=False)
    print("running")

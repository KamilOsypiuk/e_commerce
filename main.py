from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from auth.router import router as auth_router
from user.routes import router as utils_router
from data.routes import router as data_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(utils_router)
app.include_router(data_router)


@app.exception_handler(IntegrityError)
async def validation_exception_handler(request, exc):
    return JSONResponse(str(exc), status_code=status.HTTP_400_BAD_REQUEST)

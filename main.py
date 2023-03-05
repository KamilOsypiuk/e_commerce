from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from auth.router import router as auth_router
from data.routes import router as data_router
from user.routes import router as utils_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(utils_router)
app.include_router(data_router)


@app.exception_handler(IntegrityError)
def validation_exception_handler(request, exc) -> JSONResponse:
    return JSONResponse(str(exc.args[0]), status_code=status.HTTP_400_BAD_REQUEST)

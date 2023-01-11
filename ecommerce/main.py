from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import create_engine
from sqlmodel import SQLModel
from sqlmodel import Session
from sqlmodel import select

from ecommerce.Data.model import Data
from ecommerce.User.model import Users

from ecommerce.auth.router import router as auth_router


engine = create_engine("postgresql://postgres:postgres@localhost/postgres")

SQLModel.metadata.create_all(engine)


async def get_db():
    with engine.connect() as db:
        try:
            yield db
        finally:
            db.close()


app = FastAPI()

app.include_router(auth_router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.get("/User/")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return {"token": token}


with Session(engine) as session:
    @app.post("/Data/create/", tags=['Data'], status_code=201,
              response_description="Item have been created successfully")
    async def create_data(first_name, last_name):
        session.add(Data(first_name=first_name, last_name=last_name))
        session.commit()


    async def create_user(data: dict):
        session.add(Users(username=data, email=data, password=data))
        session.commit()


    @app.get(f"/Data/read_one/", tags=['Data'])
    async def read(id):
        statement = select(Data).where(Data.id == id).limit(1)
        data = session.scalar(statement)
        if data is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return data


    @app.get(f"/User/read_one/", tags=['User'])
    async def read(id):
        statement = select(Users).where(Users.id == id).limit(1)
        data = session.scalar(statement)
        if data is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return data

    @app.get("/Data/read_many/", tags=['Data'])
    async def read_many(limit=None, offset=None):
        statement = select(Data).order_by(Data.id).limit(limit).offset(offset)
        data = session.scalars(statement)
        results = data.all()
        return results


    @app.get("/User/read_many/", tags=['User'])
    async def read_many(limit=None, offset=None):
        statement = select(Users).order_by(Users.id).limit(limit).offset(offset)
        data = session.scalars(statement)
        results = data.all()
        return results


    @app.put("/Data/update/", tags=['Data'])
    async def update(id, first_name, last_name):
        statement = select(Data).where(Data.id == id).limit(1)
        data = session.scalar(statement)
        data.first_name = first_name
        data.last_name = last_name
        if data is None:
            raise HTTPException(status_code=404, detail="Item not found")
        session.commit()


    @app.delete("/Data/delete/", tags=['Data'])
    async def delete(id):
        statement = select(Data).where(Data.id == id).limit(1)
        data = session.scalar(statement)
        if data is None:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(data)
        session.commit()

    @app.delete("/User/delete/", tags=['User'])
    async def delete(id):
        statement = select(Users).where(Users.id == id).limit(1)
        data = session.scalar(statement)
        if data is None:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(data)
        session.commit()
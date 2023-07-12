import uvicorn
from fastapi import FastAPI

from api import router
from config.db_config import database

app = FastAPI(title="some peace of sh...  test", redoc_url="/redoc")
app.include_router(router)


# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

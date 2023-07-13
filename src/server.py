import uvicorn
from fastapi import FastAPI

from api import router

app = FastAPI(title="some peace of sh...  test", redoc_url="/redoc")
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

import uvicorn
from fastapi import FastAPI

from imageRouter import router

app = FastAPI(docs_url="/docs")

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)

import uvicorn
from fastapi import FastAPI
from fastapi_router_controller import Controller, ControllersTags
from controller.user_controller import UserController, router
from utils.connection import conn
from utils.config import Config


app = FastAPI(
    title = Config.read('app', 'name'),
    version = "0.0.1",
    docs_url = Config.read('app', 'api-docs.path'),
    openapi_tags = ControllersTags
)


@app.get("/")
def home() -> str:
    return "Home"


def main():
    app.include_router(router)
    
    conn()
    
    uvicorn.run(
        app = "main:app",
        host = "127.0.0.1",
        port = 8000,
        workers = 1,
        reload = True
    )
    
    
if __name__ == "__main__":
    main()
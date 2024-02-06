import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from const import APP, HOST, PORT, WORKERS
from database.connection import conn
from routers.patch import patch_router
from routers.patch_detail import patch_detail_router
from routers.product import product_router
from routers.user import user_router


# 라우터 등록
app = FastAPI()
app.include_router(router=patch_router, prefix="/patch")
app.include_router(router=patch_detail_router, prefix="/patch_detail")
app.include_router(router=product_router, prefix="/product")
app.include_router(router=user_router, prefix="/user")


# 출처 등록
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


@app.on_event("startup")
def on_startup():
    conn()


if __name__ == "__main__":
    uvicorn.run(
        app = APP,
        host = HOST,
        port = PORT,
        workers = WORKERS,
        reload = True
    )
    

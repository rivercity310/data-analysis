import uvicorn
from fastapi import FastAPI
from const import APP, HOST, PORT, WORKERS
from database.connection import conn
from routers.patch import patch_router
from routers.patch_detail import patch_detail_router
from routers.product import product_router
from routers.user import user_router


app = FastAPI()
app.include_router(router=patch_router, prefix="/patch")
app.include_router(router=patch_detail_router, prefix="/patch_detail")
app.include_router(router=product_router, prefix="/product")
app.include_router(router=user_router, prefix="/user")


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
    

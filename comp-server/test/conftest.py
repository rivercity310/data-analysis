# [ conftest.py ]
# - 테스트 시작점 역할을 하는 모듈
# - 테스트 파일이 필요로 하는 애플리케이션 인스턴스를 만든다.
import asyncio      # 테스트가 단일 스레드로 실행되도록 하는 역할 (활성 루프 세션)
import httpx        # 비동기 클라이언트 역할 
import pytest
from main import app 
from typing import Generator, Any
from sqlmodel import Session
from database.connection import Settings, conn, get_session
from models.user import User
from models.product import Product


# [ 루프 세션 픽스쳐 ]
# scope
# - session: 전체 테스트 세션동안 픽스쳐 함수가 유효
# - module: 특정 함수에서만 유효
@pytest.fixture(scope = "session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
    

async def init_db():
    conn()
    

@pytest.fixture(scope = "session")
async def default_client():
    await init_db()
    async with httpx.AsyncClient(app = app, base_url = "http://app") as client:
        yield client

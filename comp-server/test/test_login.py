import httpx
import pytest


@pytest.mark.asyncio
async def test_sign_new_user(default_client: httpx.AsyncClient) -> None:
    payload = {
        "user_email": "h970126@naver.com",
        "user_password": "12345"
    }
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    response = await default_client.post(url = "/user/signup", json = payload, headers = headers)
    
    assert response.status_code == 404
    
    
@pytest.mark.asyncio
async def test_sign_user_in(default_client: httpx.AsyncClient) -> None:
    payload = {
        "user_email": "h970123126@naver.com", 
        "user_password": "12345"
    }
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = await default_client.post(url = "/user/signin", json = payload, headers = headers)
    
    print(response.status_code)
    print(response.json())
    assert response.status_code == 200
    assert response.json()['token_type'] == 'Bearer'
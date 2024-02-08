from fastapi import Depends, APIRouter
from fastapi_router_controller import Controller
from service.user_service import UserService
from model.user import User


router = APIRouter()
controller = Controller(router, openapi_tag={'name': 'user-controller'})


@controller.use()
@controller.resource()
class UserController:
    def __init__(self, service: UserService = Depends()):
        self.service = service
           
    
    @controller.route.get(
        path = "/{id}",
        tags = ['sample-controller'],
        summary = 'Get Object from DB',
        response_model = User
    )
    def get_by_id(self, id: int) -> User:
        return self.service.get_by_id(id)
    
    
    @controller.route.get("/all")
    def get_by(self) -> list[User]:
        return self.service.get_by()
    

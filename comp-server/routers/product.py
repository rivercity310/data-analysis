from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, Session
from database.connection import get_session
from models.product import Product, ProductUpdate
from auth.authenticate import authenticate


product_router = APIRouter(tags=["product_router"])


@product_router.get("/")
async def get_all_product(session: Session = Depends(get_session)) -> list[Product]:
    stat = select(Product)
    return session.exec(stat).all()    


@product_router.get("/{id}")
async def get_product(
    id: int, 
    session: Session = Depends(get_session)
) -> Product:
    product = session.get(Product, id)
    
    if not product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"CAN'T FIND PRODUCT ID {id}"
        )
    
    return product


@product_router.post("/")
async def add_product(
    product: Product, 
    user: str = Depends(authenticate),
    session: Session = Depends(get_session)
) -> Product:
    
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@product_router.put("/{id}")
async def update_product(
    id: int, 
    product_update: ProductUpdate, 
    session: Session = Depends(get_session)
) -> Product:
    product = session.get(Product, id) 
    product_data = product_update.model_dump()
   
    if not product:
       raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"CAN'T FIND PRODUCT ID {id}")
    
    for key, value in product_data.items():
        if type(value) == str and not value.strip():
            continue
        
        setattr(product, key, value)    
    
    session.add(product)
    session.commit()
    session.refresh(product)
    
    return product
    
    
@product_router.delete("/{id}")
async def delete_product(
    id: int, 
    session: Session = Depends(get_session)
) -> Product:
    product = session.get(Product, id)
    
    if not product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"CAN'T NOT FIND PRODUCT ID {id}"
        )
        
    session.delete(product)
    session.commit()
    
    return product
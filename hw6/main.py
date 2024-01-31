from datetime import datetime
from fastapi import FastAPI, HTTPException, Path
from typing import List
from random import randint
from hashlib import sha3_384
from .models import db, products, users, orders
from .models import Product, User,  Order#, OrderStatus


app = FastAPI()


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/")
async def root():
    return {"mess": "hello!!!"}


@app.get("/users/", response_model=List[User])
async def get_all_users():
    query = users.select()
    return await db.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int = Path(..., gt=0)):
    query = users.select().where(users.c.id == user_id)
    result = await db.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="user not found")
    return result


@app.post("/users/", response_model=User)
async def create_user(user: User):
    _user = dict(user)
    del _user['id']
    _user['password'] = get_hex_digest(_user['password'])
    query = users.insert().values(**_user)
    new_id = await db.execute(query)
    return {**_user, 'id': new_id}


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    _user = dict(user)
    del _user['id']
    _user['password'] = get_hex_digest(_user['password'])
    query = users.update().where(users.c.id == user_id).values(**_user)
    await db.execute(query)
    return {**_user, 'id': user_id}


@app.delete("/users/{user_id}")
async def del_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await db.execute(query)
    return {"mess": "user deleted"}


@app.get("/products/", response_model=List[Product])
async def get_all_products():
    query = products.select()
    return await db.fetch_all(query)


@app.get("/products/{product_name}", response_model=List[Product])
async def get_product(product_name: str = Path(..., title='product_name')):
    query = products.select().where(products.c.product_name == product_name)
    result = await db.fetch_all(query)
    if not result:
        raise HTTPException(status_code=404, detail="product not found")
    return result


@app.post("/products/", response_model=Product)
async def create_product(product: Product):
    _product = dict(product)
    del _product['id']
    query = products.insert().values(**_product)
    new_id = await db.execute(query)
    return {**_product, 'id': new_id}


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: Product):
    _product = dict(product)
    del _product['id']
    query = products.update().where(products.c.id == product_id).values(**_product)
    await db.execute(query)
    return {**_product, 'id': product_id}


@app.delete("/products/{product_id}")
async def del_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await db.execute(query)
    return {"mess": "product deleted"}


@app.get("/orders/", response_model=List[Order])
async def get_all_orders():
    query = orders.select()
    return await db.fetch_all(query)


@app.get("/orders/{user_id}", response_model=List[Order])
async def get_order(user_id: str = Path(..., title='user_id')):
    query = orders.select().where(orders.c.user_id == user_id)
    result = await db.fetch_all(query)
    if not result:
        raise HTTPException(status_code=404, detail="orders not found")
    return result


@app.post("/orders/", response_model=Order)
async def create_order(order: Order):
    _order = dict(order)
    del _order['id']
    query = orders.insert().values(**_order)
    new_id = await db.execute(query)
    return {**_order, 'id': new_id}


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order: Order):
    _order = dict(order)
    del _order['id']
    query = orders.update().where(orders.c.id == order_id).values(**_order)
    await db.execute(query)
    return {**_order, 'id': order_id}


@app.delete("/orders/{order_id}")
async def del_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await db.execute(query)
    return {"mess": "order deleted"}


###
def get_hex_digest(password):
    return sha3_384(password.encode('utf-8')).hexdigest()


@app.get("/create_fake/{count}")
async def create_fake(count: int):
    for i in range(1, count+1):
        query = users.insert().values(firstname=f"user_{i}",
                                      lastname="lastname",
                                      email=f"mail_{i}@mail.ru",
                                      password=f"pass_{i}")
        await db.execute(query)
    for i in range(1, count+1):
        query = products.insert().values(product_name=f"product_name_{i}",
                                         description=f"description_{i}",
                                         price=randint(1, 1000))
        await db.execute(query)
    for i in range(1, count+1):
        query = orders.insert().values(user_id=randint(1, count),
                                       product_id=randint(1, count),
                                       date_at=datetime.now(),
                                       status=randint(1, 7)
                                       )
        await db.execute(query)
    return {'mess': f"{count} fake data create"}


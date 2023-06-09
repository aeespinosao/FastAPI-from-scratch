from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
import requests
from fastapi.background import BackgroundTasks
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host='redis-13726.c16.us-east-1-3.ec2.cloud.redislabs.com',
    port=13726,
    password='',
    decode_responses=True
)

class ProductOrder(HashModel):
    product_id: str
    quantity: int
    
    class Meta:
        database = redis
      
class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int  
    status: str
    
    class Meta:
        database = redis

@app.get("/order")
def all():
    return [get(pk) for pk in Order.all_pks()]


@app.post("/order")
def create(product_order: ProductOrder, background_task: BackgroundTasks):
    req = requests.get("http://localhost:8000/product/{product_order.product_id}")
    product = req.json()
    fee = product.get('price', 0)*0.2
    order = Order(
        product_id=product_order.product_id,
        price = product.get('price', 0),
        fee = fee,
        total = product.get('price', 0) + fee,
        quantity = product_order.quantity,
        status = 'pending'
    )
    order.save()    
    background_task.add_task(order_complete, order)
    return order

@app.get("/order/{pk}")
def get(pk: str):
    return Order.get(pk)

@app.delete("/order/{pk}")
def delete(pk: str):
    return Order.delete(pk)

def order_complete(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd(name='order-completed', fields=order.dict())
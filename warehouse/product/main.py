from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

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
    password='yRk9oGN6bXOhYh0ewKe7onxxxq9MnXKM',
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int
    
    class Meta:
        database = redis
        

@app.get("/product")
def all():
    return [get(pk) for pk in Product.all_pks()]


@app.post("/product")
def create(product: Product):
    return product.save()

@app.get("/product/{pk}")
def get(pk: str):
    return Product.get(pk)

@app.delete("/product/{pk}")
def delete(pk: str):
    return Product.delete(pk)
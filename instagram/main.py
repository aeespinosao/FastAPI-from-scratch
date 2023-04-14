from fastapi import FastAPI
from database.database import engine, Base
from routers import user, post
from fastapi.staticfiles import StaticFiles

app = FastAPI() 

app.include_router(user.router) 
app.include_router(post.router)
Base.metadata.create_all(engine)

app.mount("/images", StaticFiles(directory="images"), name="images")
from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    username: str
    email: str
    password: str
    
    class Config:
        orm_mode = True
        
class PostBase(BaseModel):
    image_url: str
    image_url_type: str
    caption: str
    user_id: int

class User(BaseModel):
    username: str
    
    class Config:
        orm_mode = True
    
class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    user: User
    
    class Config:
        orm_mode = True
        
class UserAuth(BaseModel):
    id: int
    username: str
    email: str
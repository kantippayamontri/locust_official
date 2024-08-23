from fastapi import FastAPI
from pydantic import BaseModel  # standard python types
from typing import Union
import time
import random

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_office: Union[bool, None] = None

class Login(BaseModel):
    username: str
    password: str

@app.get("/")
def index():
    return "index api"

@app.get("/about")
def about():
    return "about api"

@app.get("/hello")
def hello():
    return "Hello"


@app.get("/world")
def world():
    return "world"


@app.get("/items/{item_id}")
def read_items(item_id: int, q: Union[str, None]=None):
    return {"item_id": item_id, "q": q}
    # return {
    #     "item_id": item_id,
    #     "item_name": item.name,
    #     "item_price": item.price,
    #     "is_office": item.is_office,
    # }

@app.post(f"/login")
def login(login: Login):

    #TODO: for testing error in waiting too long
    # random_value =random.random() 
    # if  random_value > 0.8:
    #     print(f"random value: {random_value}")
    #     time.sleep(2)

    return {
        "status" : "success",
        "username": login.username,
        "password": login.password,
    }

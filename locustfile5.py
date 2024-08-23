from locust import HttpUser, tag, task, between, constant
from locust.exception import RescheduleTask
from typing import Union
from pydantic import BaseModel
import random
from icecream import ic
import json


class LoginUser(BaseModel):
    username: str
    password: Union[str, None] = (
        None  # add to make some request error for error checking
    )

# HttpUser -> most have 'client' to make http requests.
class MyUser(HttpUser):
    wait_time = constant(3)

    @tag("get")
    @tag("basic")
    @task(1)
    def index(
        self,
    ):
        self.client.get("/")

    @tag("get")
    @tag("basic")
    @task(1)
    def about(
        self,
    ):
        self.client.get("/about")

    """ 
    client = instance of HttpSession 
    HttpSession = subclass of requests.Session
    requests.Session = it preserves cookies between requests -> can use to log in
    """

    @tag("post")
    @tag("login")
    @task(1)
    def login(
        self,
    ):
        userList = [
            LoginUser(username="Kan", password="1234"),
            LoginUser(username="First", password="5555"),
            LoginUser(
                username="test fail",
                password=None,
            ), # this will get error -> password can not be None -> string only. 
        ]

        random_index_user = random.randint(0, len(userList) - 1)

        with self.client.post(
            "/login",
            json=json.loads(userList[random_index_user].model_dump_json()),
            catch_response=True,
        ) as response:
            if response.elapsed.total_seconds() > 0.5:
                print("Got wrong response -> too long to wait.")
                print()
                response.failure("Got wrong response -> too long to wait.")
                # response.success() #TODO: we if use this line in stead of above line -> we will tell locust that this request too long is sucess not failure
                # raise RescheduleTask() #TODO: avoid logging a request
            elif response.status_code == 200:
                print(f"request success ////////")
                # ic(json.loads(response.text))
                ic(response.json())
                print()
                response.success()
                # raise RescheduleTask()
            else:
                print(f"request fail status code: {response.status_code} <---")
                print()
                response.failure("Got wrong response -> code wrong.")
                # raise RescheduleTask()
    
    #TODO: we can set not found api to success -> using response.success()
    @tag("get")
    @tag("not_found")
    @task(1)
    def not_found(self,):
        with self.client.get("/not_found", catch_response=True) as response:
            if response.status_code == 404:
                ic(f"request not found.")
                print()
                response.success()
    
    #TODO: grouping a request
    @task
    def group_request(self,):
        for i in range(10):
            self.client.get('/items?item_id=')
        ...

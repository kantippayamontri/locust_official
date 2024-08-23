from locust import HttpUser, task, between, constant_throughput  # type: ignore
import time
# from typing import Union,

class HelloWorldUser(HttpUser):
    # create client from HttpUser -> create session for each client
    # each session use to make a request to host
    wait_time = constant_throughput(10) # type: ignore # 10 task per second -> wait_time is apply to tasks not requests.
    # •	Constant Throughput ensures a specific number of requests per second across all users, dynamically adjusting the wait time to maintain this rate.
	# •	Constant Pacing ensures that each individual user starts their tasks at consistent intervals, regardless of the time taken by the tasks themselves.

    @task  # with task decorator -> locust create micro-thread -> code with task will executed sequently ex. /world will call after /hello is executed
    def hello_world(
        self,
    ):
        self.client.get("/hello", name="helloworld_user/hello") # call first 
        self.client.get("/world", name="helloworld_user/world") # called after /hello already executed (cuz task decorator)

class QuickstartUser(HttpUser):
    # delayed after each task executed
    # wait_time is an attribute to tell locust how long to wait after every request execution
    # if we not set wait_time -> new set of request will execution as soon as possible

    #TODO: about wait_time
    # wait_time = between(1, 5)  # type: ignore # (random wait) stimulated users wait 1-5 seconds after each task is executed
    # wait_time = 1 # wait 1 seconds when each request execution

    # we can write wait_time in terms of function
    last_wait_time=0
    def wait_time(self,):
        self.last_wait_time += 0.5
        return self.last_wait_time

    @task  # with task decorator -> locust create micro-thread -> code with task will executed sequently ex. /world will call after /hello is executed
    def hello_world(
        self,
    ):
        self.client.get("/hello", name="quickstart_user") # call first 
        self.client.get("/world", name="quickstart_user") # called after /hello already executed (cuz task decorator)

    @task(3) # when running each task will random pick -> view_items have weight=3 -> have a chance to pick 3 time than task without weight declare 
    def view_items(
        self,
    ):
        for item_id in range(10):  # type: ignore
            self.client.get(f"/items/{item_id}?q=haha", name="items") # we use name paramter to group requests -> items will show instead of /items in name tab
            time.sleep(1)
    
    def on_start(self,): # this function will be run only when each client start the process
        print(f"client start")
        self.client.post("/login", json={"username": "foo", "password": "bar"})

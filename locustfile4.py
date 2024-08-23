# events -> when we need to add some code when the event start and stop
from locust import  events,task, User, constant
from locust.runners import MasterRunner

# run when the test is starting (after click run)
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("A new test is starting")

# run when the test is stopping (after the test is finish ex. by time_out)
@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("A new test is stopping")

# run when we run locust in terminal
@events.init.add_listener
def on_locust_init(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        print(f"I'm on Master node.")
    else:
        print(f"I'm on a worker or standalone node")

class UserClass(User):

    wait_time = constant(2)

    @task
    def hello(self,):
        print(f"hello")
from locust import HttpUser, User, task, between, constant, constant_throughput  # type: ignore


# we can use User class instead of HttpUser class when we want to mock user with other protocals like websocket
class MobileUser(User):
    weight = 3  # set weight of this user class

    # last_wait_time = 0
    # def wait_time(self,):
    #     self.last_wait_time+=0.5
    #     return self.last_wait_time

    wait_time = between(1, 5)  # type: ignore

    def on_start(
        self,
    ):  # call when start executing the task
        print(f"--> mobile user on start")

    def on_stop(self):  # call when stop executing the task
        # stop when 1. set runtime by --run-time
        print(f"xxx---> mobile user on stop")

    @task
    def my_task(self):
        print("User instance (%r) executing my_task" % self)

    @task
    def mobile_task(
        self,
    ):
        print(f"mobile task")


class WebUser(User):
    weight = 1  # set weight of this user class

    def on_start(self):
        print(f"---> web user on start")

    def on_stop(self):
        print(f"xxx---> web user on stop")

    @task
    def my_task(self):
        print("User instance (%r) executing my_task" % self)

    @task
    def helloworld(
        self,
    ):
        print(f"web user task")

    wait_time = constant(1)  # type: ignore
    # wait_time = constant_throughput(50) # type: ignore


class AdminUser(User):
    # TODO: fixed_count will have higher prority than weight
    fixed_count = 1  # we can set fixed_count -> to make sure that we have the system will create Admin user 1 user surely (in this case we set fixed_count=1)
    wait_time = constant(1)  # type: ignore
    weight = 1

    def on_start(self):
        print(f"---> Admin user start")

    def on_stop(self):
        print(f"xxx---> Admin user on stop")

    @task
    def my_task(self):
        print("User instance (%r) executing my_task" % self)

    @task
    def admin_task(
        self,
    ):
        print(f"admin task")
        # TODO: environment variable -> environment that user run on
        # self.environment.runner.quit() # if we quit on stanalone locust instance -> stop the entire run. if run on worker node -> stop that particular node.


def mytask1(user: User): # fix input type to be User
    print(f"task 1")


def mytask2(user: User):
    print(f"task 2")


def mytask3(user: User):
    print(f"task 3")


class ClassListUser(User):
    # TODO: we can assign task via list of function -> the function in list will randomly execute.
    tasks = [mytask1, mytask2, mytask3]  # type: ignore
    wait_time = constant(1)  # type: ignore


class ClassDictUser(User):
    # TODO: we can assign task via dict ->  key=function,value=weight,
    tasks = {  # type: ignore
        mytask1: 1,
        mytask2: 3,
        mytask3: 1,
    }  # type: ignore

    #TODO: or we can implement this dict into list
    # tasks = [mytask1, mytask2,mytask2,mytask2,mytask3]

    wait_time = constant(1)  # type: ignore

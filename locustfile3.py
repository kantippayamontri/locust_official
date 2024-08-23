from locust import User, constant, tag, task #type: ignore

#TODO: we can use tag decorator to run the tag with has only tag by use --tags task1 task2
class TagClass(User):

    wait_time = constant(1) #type: ignore

    def on_start(self):
        print(f"Tag class start...")
    
    def on_stop(self):
        print(f"Tag class stop...")
    
    @tag("tag1")
    @task
    def mytask1(user:User):
        print(F"mytask1 tag: 1")

    @tag("tag2")
    @task
    def mytask2(user:User):
        print(F"mytask2 tag: 2")

    @tag("tag3")
    @task
    def mytask3(user:User):
        print(F"mytask3 tag: 3")
    
    @task
    def mytask4(self):
        print(f"mytask4: no tag")

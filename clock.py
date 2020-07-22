from apscheduler.schedulers.blocking import BlockingScheduler
from SendMeMsg import SendMeMsg

def todo():
    SendMeMsg()
    print("MSG sent")

sched=BlockingScheduler()
sched.add_job(todo,'interval',minutes=2)
sched.start()
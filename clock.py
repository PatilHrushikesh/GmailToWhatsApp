from SendMeMsg import SendMeMsg
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    SendMeMsg()
    print('This job is run every three minutes.')

sched.start()

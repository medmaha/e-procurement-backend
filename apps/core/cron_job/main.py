import time
import schedule


counter = 0


def task():
    global counter
    counter += 1
    print("task running")


schedule.every(30).seconds.do(task)


while counter < 3:
    time.sleep(5)
    schedule.run_pending()

import webbrowser
from time import sleep
from time import ctime

NUM_BREAKS = 3
WORK_TIME_SEC = 10
VIDEO_URL = 'http://www.youtube.com/watch?v=kOmGsEFSBc8'

print "Start at " + ctime()
for _ in range(NUM_BREAKS):
    sleep(WORK_TIME_SEC)
    webbrowser.open(VIDEO_URL)

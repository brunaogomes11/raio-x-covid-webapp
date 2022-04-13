import time 
import os

def countdown():
    t = 18000
    while t:
        time.sleep(1)
        t -= 1
        if t == 0:
            dir = os.listdir("./static/uploads/")
            for i in range(0, len(dir)):
                os.unlink('./static/uploads/'+dir[i])

def delete_files():
    dir = os.listdir("./static/uploads/")
    for i in range(0, len(dir)):
        os.unlink('./static/uploads/'+dir[i])
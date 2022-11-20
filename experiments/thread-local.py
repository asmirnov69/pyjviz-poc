import threading, time

def thread_body(idx):
    mydata = threading.local()
    mydata.x = idx

    while 1:
        print(f"thread {threading.get_native_id()}, local x is {mydata.x}")
        time.sleep(5)        

if __name__ == "__main__":
    mydata = threading.local()
    mydata.x = 1

    ts = [threading.Thread(target = thread_body, args=(i,)) for i in range(3)]
    for t in ts:
        t.start()

    print(f"main run on thread {threading.get_native_id()}, local x is {mydata.x}")

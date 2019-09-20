from queue import Queue

def main():

    page_queue = Queue(100)
    for i in range(1,101):
        page_queue.put(i)

    data_queue = Queue()

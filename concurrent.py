# Cook book: Chapter 12: Concurrency
# recepe 12.1: Starting Threads
import time
from threading import Thread


class CountDownTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def countdown(self, n):
        while n > 0 and self._running:
            print("T-Minus %d" % n)
            n -= 1
            time.sleep(5)

def run_12_1():
    countdown = CountDownTask()
    t = Thread(target=countdown.countdown, args=(3,))
    t.start()

    time.sleep(10)
    countdown.terminate()
    t.join()

# Recepe 12.2 : Determining if an event has started
from threading import Thread, Event, Condition

def countdown(n, event):
    print("Starting Countdown")
    time.sleep(1)
    print("GO!!")
    event.set()
    while n > 0:
        print("T-MINUS ", n)
        n -= 1
        time.sleep(2)

def run_12_2():
    e = Event()
    t = Thread(target=countdown, args=(5,e))
    t.start()
    
    e.wait()
    print("Countdown started")


class PeriodicTimer:
    def __init__(self, interval):
        self.interval = interval
        self._cv = Condition()
        
    def start(self):
        self.t = Thread(target=self.run)
        self.t.start()

    def run(self):
        while True:
            print("Periodic Timer Tick!")
            with self._cv:
                time.sleep(self.interval)
                print("Periodic Timer Notify all!")
                self._cv.notify_all()

    def wait_for_tick(self):
        with self._cv:
            print("Periodic Timer wait")
            self._cv.wait()
            print("Periodic Timer stopped waiting")


def count_down(n, timer):
    while n > 0:
        print("T-MINUS ", n)
        n -= 1
        timer.wait_for_tick()

def count_up(n, timer):
    i = 0
    while i < n:
        print("T_PLUS ", i)
        i += 1
        timer.wait_for_tick()

def run_12_2_b():
    pt = PeriodicTimer(2)
    pt.start()
    
    t1 = Thread(target=count_down, args=(10, pt))
    t2 = Thread(target=count_up, args=(5, pt))

    t1.start()
    t2.start()



# Recepe 12.3: Communicating between threads
import random
import queue
def producer(queue):
    while True:
        time.sleep(1)
        print("Queue size: %d" % queue.qsize())
        print("Put Widget")
        widget = random.choice(('drum', 'stick', 'trombone', 'swordfish'))
        queue.put(widget, block=False)

def consumer(queue, name):
    def _print(string):
        print("%s: %s" % (name, string))
        
    while True:
        widget = queue.get()
       
        _print("will crank widget: %s" % widget)
        time.sleep(random.choice((1,3,5,3,6,7)))
        _print("Cranket!")
    
def run12_3():
    q = queue.Queue(15)

    Thread(target=producer, args=(q,)).start()
    
    # Thread(target=consumer, args=(q, 'Tamara')).start()
    Thread(target=consumer, args=(q, 'Johny')) .start()

    
    
if __name__ == '__main__':
    run12_3()

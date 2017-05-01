#!/usr/bin/python3
from threading import Thread, Lock, Condition, get_ident
from random import randint

# errors might occure if more than threads_count threads use the same BRLock
class BRLock:
    def __init__(self, threads_count):
        self.threads_count = threads_count
        self.locks = [Lock() for i in range(threads_count)]
        self.state = 0
        # -1 means a writer is writing,
        # 0 means no one is using the resource atm,
        # >0 indicates the number of active readers
        self.state_cond = Condition()
        self.lock_vs_thread = {} #a dictionary identifying locks with threads

    def rd_acquire(self):
        with self.state_cond:
            while self.state == -1:
                self.state_cond.wait()
            lock_id = randint(0, self.threads_count - 1)
            self.locks[lock_id].acquire()
            self.lock_vs_thread[lock_id] = get_ident() #gets the id of the current thread
            self.state += 1

    def rd_release(self):
        with self.state_cond:
            for i in self.lock_vs_thread:
                if self.lock_vs_thread[i] == get_ident():
                    self.locks[i].release()
                    self.state -= 1
                    # ...

    def wr_acquire(self):
        pass

    def wr_release(self):
        pass

brlock = BRLock(8)
thread = Thread(target=brlock.rd_acquire)
thread.start()
thread.join()
print(brlock.lock_vs_thread)

#!/usr/bin/python3
from threading import Thread, Lock, Condition, get_ident
from random import randint
from time import sleep

class BRLock:
    def __init__(self, threads_count):
        self.threads_count = threads_count
        self.locks = [Lock() for i in range(threads_count)]
        #a dictionary identifying locks with threads
        self.lock_vs_thread = {i:0 for i in range(threads_count)}
        self.lock_vs_thread_mutex = Lock()

        self.another_writer_active = False;
        # self.another_writer_mutex = Lock()

        self.another_writer_cond = Condition()


    def rd_acquire(self):
        lock_id = randint(0, self.threads_count - 1)
        self.locks[lock_id].acquire()
        with self.lock_vs_thread_mutex:
            #gets the id of the current thread
            self.lock_vs_thread[lock_id] = "R{}".format(get_ident())
            # print(self.info())

    def rd_release(self):
        with self.lock_vs_thread_mutex:
            for i in self.lock_vs_thread:
                if self.lock_vs_thread[i] == "R{}".format(get_ident()):
                    self.locks[i].release()
                    self.lock_vs_thread[i] = 0
                    return
            print("wtf: there's no such lock-thread combination")
            print("my thread_id: {}".format(get_ident()))
            print(self.lock_vs_thread) #pretty print maybe?

    def wr_acquire(self):
        #sync with mutex and sleep(). a deadlock IS POSSIBLE with this solution!
        # with self.another_writer_mutex:
        #     print("wr_acquire started")
        #     while self.another_writer_active == True:
        #         print("sleeping")
        #         sleep(1)
        #     self.another_writer_active = True;

        #sync with cond
        with self.another_writer_cond:
            while self.another_writer_active == True:
                self.another_writer_cond.wait()
            self.another_writer_active = True;

        for i in range(len(self.locks)):
            self.locks[i].acquire()
            with self.lock_vs_thread_mutex:
                self.lock_vs_thread[i] = "W{}".format(get_ident())
                # print(self.info())

    def wr_release(self):
        for i in range(len(self.locks)):
            self.locks[i].release()
            with self.lock_vs_thread_mutex:
                self.lock_vs_thread[i] = 0
                # print(self.info())

        # with self.another_writer_mutex:
        #     self.another_writer_active = False;

        with self.another_writer_cond:
            self.another_writer_active = False;
            self.another_writer_cond.notify()

    def info(self):
        return "lock:thread : {}".format(self.lock_vs_thread)

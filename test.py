#!/usr/bin/python3
from threading import Thread
import brlock
from random import randint

class Reader(Thread):
    def __init__(self, id):
        self.id = id;
        super().__init__()

    def read(self):
        global resource
        print("reader {} reads: {}".format(self.id, resource))

    def run(self):
        brl.rd_acquire()
        self.read()
        brl.rd_release()

class Writer(Thread):
    def __init__(self, id):
        self.id = id;
        super().__init__()
        self.texts = ["happy-elephant", "agile-cat", "friendly-dog", "shady-rat", "dangerous-hornet", "wise-owl"]

    def write(self):
        brl.wr_acquire()
        global resource
        old_res = resource
        resource = self.texts[randint(0,5)]
        print("writer {} modified from \"{}\" to \"{}\"".format(self.id, old_res, resource))
        brl.wr_release()

    def run(self):
        self.write()

threads_count = 8
brl = brlock.BRLock(threads_count)
resource = "sample-text"

readers = [Reader(i) for i in range(threads_count + 10)]
writers = [Writer(i) for i in range(5)]
threads = readers
threads.insert(2,writers[0])
threads.insert(3,writers[1])
threads.insert(4,writers[2])
threads.insert(6,writers[3])
threads.insert(13,writers[4])
print(threads)
print()

for i in range(len(threads)):
    threads[i].start()

for i in range(len(threads)):
    threads[i].join()

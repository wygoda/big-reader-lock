#!/usr/bin/python3
from threading import Thread, Lock, get_ident

def f():
    print(get_ident())

# t = Thread(target=f)
# t.start()
# t.join()

# l = [1,2,3,4]
# print(l[0])

d = {1:"one",5:"five",60:"sixty", 2:"two", 3:"three"}
# print(size(d))
for i in d:
    print(d[i])

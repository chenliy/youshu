#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/8/4 11:25
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

import threading
from time import ctime,sleep

def music(a):
    for i in range(2):
        print('i was listening to music {},{}'.format(a,ctime()))
        sleep(1)
        return i

def movie(b):
    for i in range(2):
        print('i was whatching TV {},{}'.format(b,ctime()))
        sleep(5)

threads = []
t1 = threading.Thread(target=music,args=('music1',))
threads.append(t1)
t2 = threading.Thread(target = movie,args=('movie2',))
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True) #将线程声明为守护线程，必须在start()方法调用之前设置，如果不设置为守护线程，程序将会被无限挂起，子线程执行之后，父线程也继续执行下去
        #当父线程执行完最后一条语句print("all over {}".format(ctime()))后，没有等待子线程，直接就退出了，同时子线程也一同结束
        t.start()
    t.join() #我们只对上面的程序加了个join()方法，用于等待线程终止。join（）的作用是，在子线程完成运行之前，这个子线程的父线程将一直被阻塞。
    #       join()方法的位置是在for循环外的，也就是说必须等待for循环里的两个进程都结束后，才去执行主进程。

    print("all over {}".format(ctime()))
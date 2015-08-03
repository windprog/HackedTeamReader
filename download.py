#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   15/8/3
Desc    :   
"""
import os
import sys
from threading import Thread
import Queue
import random

from hash_check import FILE_DOWNLOAD, FILE_UNDOWNLOAD, FILE_SHA1ERROR, FILE_OTHERERROR

FILE_NOW_DOWNLOAD = os.path.join(os.path.dirname(__file__), 'now_download.txt')

BASE_URLS = [
    "http://hacking.technology/Hacked%20Team"
]

'''
def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename


def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()
'''
class MyThread(Thread):
    def __init__(self, thread_pool, timeout=30, **kwargs):
        super(MyThread, self).__init__(**kwargs)
        assert isinstance(thread_pool, ThreadPool)
        # 线程在结束前等待任务队列多长时间
        self.timeout = timeout
        self.setDaemon(True)
        self.work_queue = thread_pool.work_queue
        self.result_queue = thread_pool.result_queue
        self.start()

    def run(self):
        while True:
            try:
                # 从工作队列中获取一个任务
                callback, args, kwargs = self.work_queue.get(timeout=self.timeout)
                # 我们要执行的任务
                res = callback(args, kwargs)
                # 报任务返回的结果放在结果队列中
                self.result_queue.put(res + " | " + self.getName())
            except Queue.Empty:  # 任务队列空的时候结束此线程
                break
            except:
                print sys.exc_info()
                with file('error_traceback', 'a+') as error:
                    import traceback
                    info = sys.exc_info()
                    traceback.print_exception(*info, file=error)


class DownloadThread(MyThread):
    pass


class ThreadPool(object):
    def __init__(self, num_of_threads=10):
        self.work_queue = Queue.Queue()
        self.result_queue = Queue.Queue()
        self.threads = []
        self.__createThreadPool(num_of_threads)

    def __createThreadPool(self, num_of_threads):
        for i in range(num_of_threads):
            thread = MyThread(self)
            self.threads.append(thread)

    def wait_for_complete(self):
        # 等待所有线程完成。
        while len(self.threads):
            thread = self.threads.pop()
            # 等待线程结束
            if thread.isAlive():  # 判断线程是否还存活来决定是否调用join
                thread.join()

    def add_job(self, callable, *args, **kwargs):
        self.work_queue.put((callable, args, kwargs))


if __name__ == '__main__':
    with file(FILE_NOW_DOWNLOAD, 'a+') as result_f:
        result_f.seek(0)
        ready_lines = set(result_f.read().split('\n'))

        for path in [FILE_UNDOWNLOAD, FILE_SHA1ERROR, FILE_OTHERERROR]:
            with file(path, 'r') as undo:
                while True:
                    line = undo.readline()
                    if line not in ready_lines:
                        # 添加job
                        url = BASE_URLS[random.randint(0, len(BASE_URLS) - 1)] + line
                        pass

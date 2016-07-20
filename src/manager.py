#manager.py
#--coding:utf-8--

import Queue
import threading

import worker
import default
import store

class Manager(object):
    __slots__ = ('_task_queue', '_wait_queue',  '_config', '_stop', '_submit_thread', '_check_thread', '_stop_checking')

    def __init__(self, config=default.manager.config):
        self._task_queue = Queue.Queue()
        self._wait_queue = Queue.Queue()
        self._config = config
        self._stop = False
        self._stop_checking = False
        self.load_backup()

    @property
    def task_queue(self):
        return self._task_queue

    @property
    def wait_queue(self):
        return self._wait_queue

    def add_task(self, task):
        self.task_queue.put(task)

        return self

    def submit_task(self):
        task = self.task_queue.get()
        result = worker.crawler.delay(task.url, downloader_config=task.downloader, parser_config=task.parser)
        self.wait_queue.put(result)

        return self

    def check_task(self):
        if self._stop_checking:
            return None

        task = self.wait_queue.get()
        if task.ready():
            self.complete_task(task)
        else:
            self.wait_queue.put(task)

        return self

    def complete_task(self, task):
        result = task.get()
        store.save_data(result.url, result.data)
        self.add_url(result.url)

        return self

    def add_url(self, urls): # Custom
        for url in urls:
            task = Config(self._config.task)
            task.url = url
            self.add_task(task)

        return self

    def submit_task_loop(self):
        while not self._stop:
            self.submit_task()

    def check_task_loop(self):
        while not self._stop_checking:
            self.check_task()
        self._submit_thread.join()
        while not self.wait_queue.empty():
            self.check_task()

    def start(self):
        self._submit_thread = threading.Thread(target=self.submit_task_loop, name='SubmitThread')
        self._check_thread = threading.Thread(target=self.check_task_loop, name='CheckThread')

    def stop(self):
        self._stop = True
        self._check_thread.join()
        self.backup()

    def shutdown(self):
        self._stop = True
        self._check_stop = True
        self._check_thread.join()
        self.backup()

    def backup(self):
        pass

    def load_backup(self):
        pass

if __name__ == '__main__':
    raise EnvironmentError("Do Not Directly Run This Script")

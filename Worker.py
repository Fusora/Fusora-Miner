from multiprocessing import Process, Queue
class Worker(Process):
    def __init__(self, target, name, args, queue):
        # super().__init__()
        super(Worker, self).__init__()
        self._target = target
        self._name = name
        self._args = args
        self.queue = queue

    def run(self):
        print('{} is running'.format(self._name))
        if (self._target):
            result = self._target(*self._args)
            if result is not None:
                self.queue.put(result)
            return

from market.base.executor import Executor
from market.base.worker import Worker

class DefaultExecutor(Executor):

    def __init__(self, worker: Worker):
        super().__init__()
        self.worker = worker

    def execute(self):
        self.worker.trading()

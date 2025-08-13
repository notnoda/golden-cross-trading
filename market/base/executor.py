import threading
from abc import abstractmethod

class Executor(threading.Thread):
    
    def __init__(self):
        super().__init__()

    def run(self):
        self.execute()

    @abstractmethod
    def execute(self):
        pass

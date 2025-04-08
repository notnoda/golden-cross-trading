import threading
from abc import abstractmethod

# -----------------------------------------------------------------------------
# BaseThread
# -----------------------------------------------------------------------------
class BaseThread(threading.Thread):
    
    def __init__(self):
        super().__init__()

    def run(self):
        self.execute()

    @abstractmethod
    def execute(self):
        pass

# end of class BaseThread
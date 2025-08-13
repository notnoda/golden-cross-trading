from abc import ABC, abstractmethod

class Worker(ABC):

    @abstractmethod
    async def trading(self):
        pass

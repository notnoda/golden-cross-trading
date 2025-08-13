from abc import ABC, abstractmethod

class Rest(ABC):

    @abstractmethod
    async def post(self, path, params, name="Out"):
        pass

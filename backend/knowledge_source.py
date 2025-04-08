from abc import ABC, abstractmethod

class knowledge_source(ABC):

    @abstractmethod
    def execute(self, information):
        pass
    

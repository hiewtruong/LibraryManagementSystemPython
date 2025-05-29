from abc import ABC, abstractmethod

class IBookService(ABC):
    @abstractmethod
    def get_all_book_trans(self):
        pass
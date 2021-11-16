from enum import Enum


class Checker:
    def __init__(self, exceptionFullText, exceptionClass):
        self.exceptionFullText = exceptionFullText
        self.exceptionClass = exceptionClass

    def shout(self):
        print(self.ERROR_CODE)

    

class ERROR_CODE(Enum):
    SUCCESS = 0x000000
    CRITICAL_ERROR = 0xFFFFFF

    # HTTP REQUEST ERROR


    # DB ERROR
    BULK_WRITE_ERROR = 0xE0100
    DOCUMENT_TOO_LARGE = 0xE0101
    DUPLICATE_KEY_ERROR = 0xE0102


class BULK_WRITE_ERROR(Enum):
    print
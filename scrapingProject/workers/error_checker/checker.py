from enum import Enum
from requests.exceptions import *

class ErrorCode(Enum):
    SUCCESS = 0x000000
    CRITICAL_ERROR = 0xFFFFFF

    # HTTP REQUEST ERROR
    CONNECTION_ERROR = 0xA0101

    # DB ERROR
    BULK_WRITE_ERROR = 0xE0101
    DOCUMENT_TOO_LARGE = 0xE0102
    DUPLICATE_KEY_ERROR = 0xE0103

class ErrorChecker:
    def __init__(self):
        self.exceptionFullText = ''
    
    def is_handling(self, exceptionFullText, exceptionClass):
        self.exceptionFullText = exceptionFullText

        if exceptionClass in dir(ErrorCode):
            something = globals()[exceptionClass].say.value
        else :
            something = globals()[UnchecedError].say.value
        return something

class UnchecedError(Enum):
    say = '** Unidentified ERROR : {} **'

class ConnectionError(Enum):
    say = 'Request Connection Error : {}'

class BulkWriteError(Enum):
    say = 'DB Bulk Insert Error : {}'

class DocumentTooLargeError(Enum):
    say = 'DB Document Size Error : {}'

class DuplicateKeyError(Enum):
    say = 'DB Duplicate Key Error : {}'

class ParsingAttributeError(Enum):
    say = 'Parser Attribute Error : {}'
    
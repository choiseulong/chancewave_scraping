from enum import Enum
from requests.exceptions import *

class ERROR_CODE(Enum):
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

        if exceptionClass in dir(ERROR_CODE):
            something = globals()[exceptionClass].say.value
        else :
            something = globals()[UNCHECKED_ERROR].say.value
        return something

class UNCHECKED_ERROR(Enum):
    say = '** Unidentified ERROR : {} **'

class CONNECTION_ERROR(Enum):
    say = 'Request Connection Error : {}'

class BULK_WRITE_ERROR(Enum):
    say = 'DB Bulk Insert Error : {}'

class DOCUMENT_TOO_LARGE(Enum):
    say = 'DB Document Size Error : {}'

class DUPLICATE_KEY_ERROR(Enum):
    say = 'DB Duplicate Key Error : {}'

class PARSINNG_ATTRIBUTE_ERROR(Enum):
    say = 'Parser Attribute Error : {}'
    
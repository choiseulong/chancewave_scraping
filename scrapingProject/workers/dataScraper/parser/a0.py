from ..parserTools.tools import *

def post_list_parsing(text):
    soup = convert_response_text_to_BeautifulSoup(text)
    
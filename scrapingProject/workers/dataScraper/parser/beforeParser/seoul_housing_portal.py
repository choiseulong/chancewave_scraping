
from ..parserTools.tools import *
from ..scraperTools.tools import *

def extract_post_list_from_response_text(text, dateRange, channelCode):
    soup = convert_response_text_to_BeautifulSoup(text)
    tr_items = search_tags_in_soup(soup, 'tr')
    for tr in tr_items:
        checkFixedPost = extract_children_tags_from_parents_tags(tr, 'td', False, {'class' : 'td1'})
    pass

def extract_post_contents_from_response_text(text):
    pass
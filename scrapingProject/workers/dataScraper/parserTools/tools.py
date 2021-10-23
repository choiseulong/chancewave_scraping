from bs4 import BeautifulSoup

def convert_response_text_to_BeautifulSoup(responseText):
    soup = BeautifulSoup(responseText, 'html.parser')
    return soup

# def search_tag_data_in_BeautifulSoup(soup, tagName):
#     if type(tagName) == str :
#         soup

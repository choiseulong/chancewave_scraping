import re
from datetime import datetime

class Parser:
    def __init__(self):
        pass


def text_cutter_using_start_and_end_point(text, startPoint, endPoint, reverse=False):
    try :
        if startPoint and endPoint:
            if not reverse :
                start_idx = text.find(startPoint)
            else :
                start_idx = text.rfind(startPoint)
            end_idx = text[start_idx:].find(endPoint)
            text = text[start_idx:start_idx+end_idx]
            return text
    except ValueError as e :
        print('### text cutter value error ###')
        print(e)
        return None

def extract_number_from_text(text):
    numbers = re.sub(r'[^0-9]', '', text)
    return numbers

def extract_img_src_from_text(text):
    startPoint = '<img'
    imgSrcList = []
    if startPoint in text :
        endPoint = '/>'
        imgCount = text.count(startPoint)
        for _ in range(imgCount):
            startPoint_idx = text.find(startPoint)
            endPoint_idx = text[startPoint_idx:].find(endPoint)
            parsedText = text[startPoint_idx:startPoint_idx+endPoint_idx]
            imgSrc = re.search('src="(.+?)"', parsedText).group(1)
            imgSrcList.append(imgSrc)
            text = text[endPoint_idx:]
        return imgSrcList
    else :
        return None

def clean_html_tag(text):
  cleaner = re.compile('<.*?>')
  cleanedText = re.sub(cleaner, '', text)
  return cleanedText

def clean_text(text):
    text = text.replace('\n',"").replace('\t',"")
    return text

def numText_to_datetime(numList):
    if len(numList) == 5 :
        return datetime(numList[0], numList[1], numList[2], numList[3], numList[4])
    else :
        return None

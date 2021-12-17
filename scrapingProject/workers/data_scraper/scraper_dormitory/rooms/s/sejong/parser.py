from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params): 
    targetKeyInfo = {
        'multipleType' : ['uploader', 'postTitle', 'viewCount', 'postUrl', 'uploadedTime']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    table = extract_children_tag(soup, 'table', {"class" : "board_list"}, childIsNotMultiple)
    trList = extract_children_tag(table, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList[1:] :
        tdList = extract_children_tag(tr, 'td', {"data-cell-header" : True}, childIsMultiple)
        for td in tdList:
            header = extract_attrs(td, 'data-cell-header')
            text = extract_text(td)
            aTag = extract_children_tag(td, 'a', {"href" : True}, childIsNotMultiple)
            if header == '작성자':
                var['uploader'].append(text)
            elif header == '등록일':
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(text)
                )
            elif header == '조회수':
                var['viewCount'].append(extract_numbers_in_text(text))
            elif header == '제목':
                var['postTitle'].append(
                    clean_text(
                        text.replace('새글', '')
                    )
                )
                var['postUrl'].append(
                    var['channelMainUrl'] + \
                    extract_attrs(
                        aTag,
                        'href'
                    )
                )
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result


def postContentParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postImageUrl'],
        'singleType' : ['postText', 'contact']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    contentsBox = extract_children_tag(soup, 'div', {"class" : "bbs--view--cont"}, childIsNotMultiple)
    var['postText'] = clean_text(
            extract_text(
            extract_children_tag(contentsBox, 'div', {'class' : 'bbs--view--content'}, childIsNotMultiple)
        )
    )
    var['contact'] = extract_contact_numbers_from_text(var['postText'])
    imgList = extract_children_tag(contentsBox, 'img', dummyAttrs, childIsMultiple)
    if imgList:
        for img in imgList:
            var['postImageUrl'].append(
                var['channelMainUrl'] + extract_attrs(img, 'src')
            )

    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result
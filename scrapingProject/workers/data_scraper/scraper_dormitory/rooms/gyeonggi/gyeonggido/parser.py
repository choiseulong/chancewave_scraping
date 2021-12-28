from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

POST_URL_FORMAT = '/bbs/boardView.do?bIdx={bIdx}&bsIdx={bsIdx}&bcIdx={bcIdx}&menuId=1590&isManager=false&isCharge=false&page=1'


def postListParsingProcess(**params):
    target_key_info = {
        'multipleType' : ['postUrl', 'postTitle', 'postSubject', 'uploadedTime', 'viewCount']
    }
    var, jsonData, key_list = json_type_default_setting(params, target_key_info)


    # 2021-12-28 json 항목 매핑
    # CATEGORY_NAME : 분류
    # SUBJECT : 제목
    # VIEW_CNT : 조회수
    # WRITE_DATE2 : 작성일
    # CATEGORY_NAME : 민간위탁·대행

    for tmp_obj in jsonData['items']:
        tmp_post_url = POST_URL_FORMAT.format(bIdx=tmp_obj['B_IDX'], bsIdx=tmp_obj['BS_IDX'], bcIdx=tmp_obj['BC_IDX'])
        var['postUrl'].append(var['channelMainUrl'][:-1] + tmp_post_url)
        var['postTitle'].append(tmp_obj['SUBJECT'])
        var['postSubject'].append(tmp_obj['CATEGORY_NAME'])
        var['viewCount'].append(tmp_obj['VIEW_CNT'])
        var['uploadedTime'].append(convert_datetime_string_to_isoformat_datetime(tmp_obj['WRITE_DATE2']))

    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    # print(result)
    return result


def parse_onclick(text):
    return re.findall("'(.+?)'", text)[1]


def postContentParsingProcess(**params):
    target_key_info = {
        'singleType': ['postText', 'uploader'],
        'multipleType': ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, target_key_info)
    content_area = extract_children_tag(soup, 'div', {'class' : 's-v-board-default'}, childIsNotMultiple)
    content_info_header_area = extract_children_tag(content_area, 'div', {'class' : 'header'}, childIsNotMultiple)

    content_info_header_list = extract_children_tag(content_info_header_area, 'dl', childIsMultiple=childIsNotMultiple)
    content_info_header_list = extract_children_tag(content_info_header_list, 'dd', childIsMultiple=childIsMultiple)

    for tmp_info_header in content_info_header_list:
        tmp_column = tmp_info_header.strong
        tmp_column_value = tmp_column.nextSibling.text.strip()
        if tmp_column.text.strip() == '작성자':
            var['uploader'] = tmp_column_value

    content_post_area = extract_children_tag(content_area, 'div', {'class': 'content'})

    var['postText'] = clean_text(extract_text(content_post_area))
    var['postImageUrl'] = search_img_list_in_contents(content_post_area, var['channelMainUrl'])

    value_list = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, value_list)
    # print(result)
    return result

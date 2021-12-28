from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['is_going_on', 'view_count', 'uploaded_time', 'post_title', 'post_url', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', DataStatus.empty_attrs, DataStatus.not_multiple)
    contentsList = extract_children_tag(tbody, 'tr', DataStatus.empty_attrs, DataStatus.multiple)

    for contents in contentsList:
        ongoingCheck = extract_children_tag(contents, 'span', {"class": ['tag color01']}, DataStatus.not_multiple)
        if var['channel_code'] == 'gyeonggi_content_agency_0':
            if not ongoingCheck :
                var['is_going_on'].append(False)
                # continue
            else :
                var['is_going_on'].append(True)
        else :
            var['is_going_on'].append(None)
        view_count = extract_children_tag(contents, 'td', {"class": "hit"}, DataStatus.not_multiple)
        var['view_count'].append(extract_numbers_in_text(extract_text(view_count)))
        uploaded_time = extract_children_tag(contents, 'td', {"class": "date"}, DataStatus.not_multiple)
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(uploaded_time).strip()
            )
        )
        post_title = extract_children_tag(contents, 'a', {"title": True}, DataStatus.not_multiple)
        var['post_title'].append(
            extract_text(post_title)
        )
        var['post_url'].append(
            var['channel_main_url'] + extract_attrs(post_title, 'href')
        )
        uploader = extract_children_tag(contents, 'td', {"class": "name"}, DataStatus.not_multiple)
        var['uploader'].append(extract_text(uploader))
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['extra_info'],
        'single_type' : ['post_text_type', 'post_thumbnail']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_text_type'] = 'only_extra_info'
    commBoxList = extract_children_tag(soup, 'div', {"class" : "commBox"}, DataStatus.multiple)
    extraDict = {'info_title' : '사업 상세'}
    for commBox in commBoxList:
        ul = extract_children_tag(commBox, 'ul', DataStatus.empty_attrs, DataStatus.not_multiple)
        if type(ul) == type(None):
            continue
        sTlt = extract_children_tag(ul, 'div', {"class" : "sTlt"}, DataStatus.not_multiple)
        sTltText = extract_text(sTlt)
        sTltContentsText = extract_text(find_next_tag(sTlt))
        lenExtraDict = len(extraDict)
        extraDict.update({f'info_{lenExtraDict}' : [sTltText, sTltContentsText]})
    var['extra_info'].append(extraDict)
    imgDiv = extract_children_tag(soup, 'div', {"class" : "img"}, DataStatus.not_multiple)
    if imgDiv:
        var['post_thumbnail'] = var['channel_main_url'] + extract_attrs(
            extract_children_tag(imgDiv, 'img', DataStatus.empty_attrs, DataStatus.not_multiple),
            'src'
        )
    else :
        var['post_thumbnail'] = None

    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result


def postContentParsingProcess_other(**params):
    target_key_info = {
        'single_type' : ['post_text', 'linked_post_url'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    view_content = extract_children_tag(soup, 'div', {"class" : "view-content"}, DataStatus.not_multiple)
    var['post_text'] = clean_text(extract_text(view_content))
    aTagList = extract_children_tag(view_content, 'a', {'target' : True}, DataStatus.multiple)
    if aTagList:
        for a_tag in aTagList:
            print(a_tag)
            href = extract_attrs(a_tag, 'href')
            if href :
                var['linked_post_url'] += href
    var['post_image_url'] = search_img_list_in_contents(view_content, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result

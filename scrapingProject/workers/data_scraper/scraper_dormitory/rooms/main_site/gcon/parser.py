from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['is_going_on', 'view_count', 'uploaded_time', 'post_title', 'post_url', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    contentsList = extract_children_tag(tbody, 'tr', is_child_multiple=True)

    for contents in contentsList:
        ongoingCheck = extract_children_tag(contents, 'span', child_tag_attrs={"class": ['tag color01']})
        if var['channel_code'] == 'gyeonggi_content_agency_0':
            if not ongoingCheck :
                var['is_going_on'].append(False)
                # continue
            else :
                var['is_going_on'].append(True)
        else :
            var['is_going_on'].append(None)
        view_count = extract_children_tag(contents, 'td', child_tag_attrs={"class": "hit"})
        var['view_count'].append(extract_numbers_in_text(extract_text(view_count)))
        uploaded_time = extract_children_tag(contents, 'td', child_tag_attrs={"class": "date"})
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(uploaded_time).strip()
            )
        )
        post_title = extract_children_tag(contents, 'a', child_tag_attrs={"title": True})
        var['post_title'].append(
            extract_text(post_title)
        )
        var['post_url'].append(
            var['channel_main_url'] + extract_attrs(post_title, 'href')
        )
        uploader = extract_children_tag(contents, 'td', child_tag_attrs={"class": "name"})
        var['uploader'].append(extract_text(uploader))
    
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['extra_info'],
        'single_type' : ['post_text_type', 'post_thumbnail']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_text_type'] = 'only_extra_info'
    commBoxList = extract_children_tag(soup, 'div', child_tag_attrs={"class" : "commBox"}, is_child_multiple=True)
    extraDict = {'info_title' : '사업 상세'}
    for commBox in commBoxList:
        ul = extract_children_tag(commBox, 'ul')
        if type(ul) == type(None):
            continue
        sTlt = extract_children_tag(ul, 'div', child_tag_attrs={"class" : "sTlt"})
        sTltText = extract_text(sTlt)
        sTltContentsText = extract_text(find_next_tag(sTlt))
        lenExtraDict = len(extraDict)
        extraDict.update({f'info_{lenExtraDict}' : [sTltText, sTltContentsText]})
    var['extra_info'].append(extraDict)
    imgDiv = extract_children_tag(soup, 'div', child_tag_attrs={"class" : "img"})
    if imgDiv:
        var['post_thumbnail'] = var['channel_main_url'] + extract_attrs(
            extract_children_tag(imgDiv, 'img'),
            'src'
        )
    else :
        var['post_thumbnail'] = None
    result = convert_merged_list_to_dict(key_list, var)
    return result


def postContentParsingProcess_other(**params):
    target_key_info = {
        'single_type' : ['post_text', 'linked_post_url'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    view_content = extract_children_tag(soup, 'div', child_tag_attrs={"class" : "view-content"})
    var['post_text'] = clean_text(extract_text(view_content))
    aTagList = extract_children_tag(view_content, 'a', {'target' : True}, is_child_multiple=True)
    if aTagList:
        for a_tag in aTagList:
            if 'href' in a_tag.attrs.keys():
                href = extract_attrs(a_tag, 'href')
                var['linked_post_url'] += href
    var['post_image_url'] = search_img_list_in_contents(view_content, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    return result

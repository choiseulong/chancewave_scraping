from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import re

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    isEmpty = extract_children_tag(soup, 'li', child_tag_attrs={'class' : 'empty'})
    if isEmpty:
        return 

    contentsBox = extract_children_tag(soup, 'ul', child_tag_attrs={'class' : 'boardType3'})
    liList = extract_children_tag(contentsBox, 'li', is_child_multiple=True)
    if not liList :
        return
    for li in liList:
        var['post_title'].append(
            extract_text(extract_children_tag(li, 'a'))
        )
        a_tag = extract_children_tag(li, 'a')
        if not a_tag:
            continue
        MOSF, MOSFBBS = parse_href(
            extract_attrs(
                a_tag,
                'href'
            )
        )
        var['post_url'].append(
            var['post_url_frame'].format(MOSFBBS, MOSF)
        )
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    extract_children_tag(li, 'span', child_tag_attrs={'class' : 'date'})
                )[:-1]
            )
        )
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    return result

def parse_href(text):
    data = re.findall("'(.+?)'", text)
    MOSF, MOSFBBS = data[0], data[1]
    return MOSF, MOSFBBS
    
def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['view_count', 'uploader', 'contact', 'post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    container = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'subContainer'})
    view_count_box = extract_children_tag(container, 'span', child_tag_attrs={'class' : 'view'})
    var['view_count'] = extract_numbers_in_text(
        extract_text(
            view_count_box
        )
    )
    departInfo = extract_children_tag(container, 'ul', child_tag_attrs={'class' : 'departInfo'})
    departLi = extract_children_tag(departInfo, 'li', is_child_multiple=True)
    for liIdx, li in enumerate(departLi):
        liText = extract_text(li)
        if liIdx in [1, 3]:
            var['contact'] += liText + ' '
        elif liIdx in [0, 2] :
            var['uploader'] += liText + ' '
    
    editorCont = extract_children_tag(container, 'div', child_tag_attrs={'class' : 'editorCont'})
    var['post_text'] = extract_text(editorCont)
    var['post_image_url'] = search_img_list_in_contents(editorCont, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result

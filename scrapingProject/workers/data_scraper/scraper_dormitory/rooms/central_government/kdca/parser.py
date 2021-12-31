from typing_extensions import Literal
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    dbody = extract_children_tag(soup, 'div', {'class' : 'dbody'}, is_child_multiple=False)
    ulList = extract_children_tag(dbody, 'ul', child_tag_attrs={}, is_child_multiple=True)
    for ul in ulList:
        liList = extract_children_tag(ul, 'li', child_tag_attrs={}, is_child_multiple=True)
        for liIdx, li in enumerate(liList):
            liText = extract_text(li)
            if '공지' in liText :
                if var['page_count'] == 1 :
                    pass
                else :
                    break
            if liIdx == 1:
                a_tag = extract_children_tag(li, 'a', child_tag_attrs={}, is_child_multiple=False)
                onclick = extract_attrs(a_tag, 'onclick')
                postId = extract_text_between_prefix_and_suffix("('", "')", onclick)
                var['post_url'].append(
                    var['post_url_frame'].format(postId)
                )
                var['post_title'].append(liText)
            elif liIdx == 3 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(liText)
                )
            elif liIdx == 4 :
                var['view_count'].append(
                    extract_numbers_in_text(liText)
                )

    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    # print(result)
    return result

def parse_href(text):
    return text[text.find('&seq=') + len('&seq='):]

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text', 'uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    headInfo = extract_children_tag(soup, 'ul', {'class': ['head', 'info']}, is_child_multiple=False)
    spanList = extract_children_tag(headInfo, 'span', child_tag_attrs={}, is_child_multiple=True)
    for span in spanList:
        spanText = extract_text(span)
        if '담당부서' in spanText:
            var['uploader'] = extract_text(find_next_tag(span))
        elif '연락처' in spanText:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(find_next_tag(span))
            )

    tb_contents = extract_children_tag(soup, 'div', {'class' : 'tb_contents'}, is_child_multiple=False)
    var['post_text'] = clean_text(extract_text(tb_contents))
    var['post_image_url'] = search_img_list_in_contents(tb_contents, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    # print(result)
    return result

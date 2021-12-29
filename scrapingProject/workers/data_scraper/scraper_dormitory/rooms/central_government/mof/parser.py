from typing_extensions import Literal
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'view_count', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    for tr in tr_list:
        td_list = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if '공지' in td_text :
                if var['page_count'] == 1 :
                    pass
                else :
                    continue

            if td_idx == 1 : 
                var['post_title'].append(td_text)
                a_tag = extract_children_tag(td, 'a', child_tag_attrs={}, is_child_multiple=False)
                href = extract_attrs(a_tag, 'href')
                postId = extract_text_between_prefix_and_suffix('articleKey=', '&boardKey', href)
                var['post_url'].append(
                    var['post_url_frame'].format(postId)
                )
            elif td_idx == 2 :
                var['uploader'].append(td_text)
            elif td_idx == 4 :
                if td_text:
                    var['uploaded_time'].append(
                        convert_datetime_string_to_isoformat_datetime(td_text[:-1])
                    )
                else :
                    var['uploaded_time'].append(None)
            elif td_idx == 5 :
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )

    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    # print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', {'class' : 'view'}, is_child_multiple=False)
    thList = extract_children_tag(tbody, 'th', child_tag_attrs={}, is_child_multiple=True)
    for th in thList:
        thText = extract_text(th)
        if '전화번호' in thText:
            var['contact'] = extract_text(find_next_tag(th))
            break
    boardCont = extract_children_tag(soup, 'div', {'class' : 'boardCont'}, is_child_multiple=False)
    var['post_text'] = clean_text(extract_text(boardCont))
    var['post_image_url'] = search_img_list_in_contents(boardCont, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    # print(result)
    return result

from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from datetime import datetime
from pytz import timezone

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'uploaded_time', 'view_count', 'uploader', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    for tr in tr_list :
        td_list = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True)
        uploader = ''
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1 :
                a_tag = extract_children_tag(td, 'a', child_tag_attrs={}, is_child_multiple=False)
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
                var['post_title'].append(
                    td_text
                )
            elif td_idx in [3] :
                uploader += td_text + ' '
            elif td_idx == 5:
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
            elif td_idx == 4:
                if ':' in td_text: 
                    now = datetime.now(timezone('Asia/Seoul'))
                    td_text = now.isoformat()
                else :
                    td_text = convert_datetime_string_to_isoformat_datetime(td_text)
                var['uploaded_time'].append(td_text)
        var['uploader'].append(uploader)
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    cont = extract_children_tag(soup, 'div', {'class' : 'board_cont'}, is_child_multiple=False)
    if cont:
        var['post_text'] = extract_text(cont)
        var['contact'] = extract_contact_numbers_from_text(extract_text(cont))
        var['post_image_url'] = search_img_list_in_contents(cont, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result



from pickle import NONE
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'view_count', 'post_url', 'post_title', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    board_basic_list = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board_basic_list'})
    con_list = extract_children_tag(board_basic_list, 'ul', is_child_multiple=True)
    for con in con_list:
        li_list = extract_children_tag(con, 'li', is_child_multiple=True)
        for li_idx, li in enumerate(li_list):
            li_text = extract_text(li)
            if li_idx == 1:
                form = extract_children_tag(li, 'form')
                input_list = extract_children_tag(form, 'input', is_child_multiple=True)
                post_params = ''
                for input in input_list:
                    input_name = extract_attrs(input, 'name')
                    input_value = extract_attrs(input, 'value')
                    post_params += input_name + '=' + input_value + '&'
                var['post_url'].append(
                    var['post_url_frame'] + post_params
                )
                var['post_title'].append(li_text)
            elif li_idx == 2:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(li_text)
                )
            elif li_idx == 3:
                var['uploader'].append(li_text)
            elif li_idx == 4 :
                var['view_count'].append(
                    extract_numbers_in_text(li_text)
                )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'smartOutput'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] =  extract_contact_numbers_from_text(extract_text(tmp_contents))
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


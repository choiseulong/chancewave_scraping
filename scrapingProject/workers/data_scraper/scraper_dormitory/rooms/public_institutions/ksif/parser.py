from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import re

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'view_count', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    post_list = extract_children_tag(soup, 'div', child_tag_attrs={'class':'list_box'}, is_child_multiple=True)
    for post in post_list:
        var['view_count'].append(
            extract_numbers_in_text(
                extract_text_from_single_tag(post, 'div', {'class':'read'})
            )
        )
        a_tag = extract_children_tag(post, 'a', child_tag_attrs={'class':'title'})
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        var['post_title'].append(
            extract_text(a_tag)
        )
        cont_txt_tag = extract_children_tag(post, 'p', child_tag_attrs={'class':'cont_txt'})
        cont_txt = extract_text(cont_txt_tag).split('│')
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(cont_txt[1].strip())
        )
        var['uploader'].append(cont_txt[0].strip())
    
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'con_box'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    return result
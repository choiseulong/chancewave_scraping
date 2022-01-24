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
            if td_idx == 1 :
                a_tag = extract_children_tag(td, 'a', child_tag_attrs={}, is_child_multiple=False)
                onclick = extract_attrs(a_tag, 'onclick')
                postId = parse_post_id(onclick)
                var['post_url'].append(
                    var['post_url_frame'].format(postId)
                )
                var['post_title'].append(
                    td_text
                )
            elif td_idx == 3 :
                var['uploader'].append(td_text)
            elif td_idx == 4 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 5 :
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
    
    result = merge_var_to_dict(key_list, var)
    
    return result

def parse_post_id(text):
    return re.findall("'(.+?)'", text)[1]

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    view_write = extract_children_tag(soup, 'li', {'class' : 'view_write'}, is_child_multiple=False)
    var['contact'] = extract_contact_numbers_from_text(
        extract_text(view_write)
    )
    view_cont = extract_children_tag(soup, 'div', {'class' : 'view_cont'}, is_child_multiple=False)
    var['post_text'] = clean_text(extract_text(view_cont))
    var['post_image_url'] = search_img_list_in_contents(view_cont, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    
    return result

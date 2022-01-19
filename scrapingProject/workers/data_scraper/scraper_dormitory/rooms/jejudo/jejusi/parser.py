from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploader', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    for tr in tr_list:
        var['post_url'].append(
            var['post_url_frame'].format(
                parse_href(
                    extract_attrs(
                        extract_children_tag(tr, 'a', child_tag_attrs={}, is_child_multiple=False), 'href')
                )
            )
        )
        var['post_title'].append(
            extract_text(
                extract_children_tag(tr, 'td', {'class' : 'title'}, is_child_multiple=False)
            )
        )
        var['uploader'].append(
            extract_text(
                extract_children_tag(tr, 'td', {'class' : 'writer'}, is_child_multiple=False)
            )
        )
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    extract_children_tag(tr, 'td', {'class' : 'date'}, is_child_multiple=False)
                )
            )
        )
        var['view_count'].append(
            extract_numbers_in_text(
                extract_text(
                    extract_children_tag(tr, 'td', {'class' : 'hits'}, is_child_multiple=False)
                )
            )
        )
    
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    dtList = extract_children_tag(soup, 'dt', child_tag_attrs={}, is_child_multiple=True)
    for dt in dtList :
        if extract_text(dt) == '연락처':
            var['contact'] = extract_text(find_next_tag(dt))
    
    viewContent = extract_children_tag(soup, 'div', {'class' : 'view-content'}, is_child_multiple=False)
    var['post_text'] = extract_text(viewContent)
    var['post_image_url'] = search_img_list_in_contents(viewContent, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    return result

def parse_href(text):
    prefix = 'ice_id='
    suffix = '¤'
    result = text[text.find(prefix) + len(prefix) : text.find(suffix)]
    return result
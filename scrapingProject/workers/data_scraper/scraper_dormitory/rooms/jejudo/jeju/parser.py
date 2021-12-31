from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

# jeju_1 ~ jeju_5
def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploader', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', {"class" : True}, is_child_multiple=True)
    for tr in tr_list:
        td_list = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            if len(td_list) != 6 :
                break
            if td_idx == 1 :
                var['post_title'].append(extract_text(td))
                var['post_url'].append(
                    var['channel_main_url'] + \
                        extract_attrs(
                            extract_children_tag(td, 'a', child_tag_attrs={}, is_child_multiple=False),
                            'href'
                        )
                )
            elif td_idx == 3:
                var['uploader'].append(
                    clean_text(extract_text(td))
                )
            elif td_idx == 4: 
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(extract_text(td))
                )
            elif td_idx == 5: 
                var['view_count'].append(
                    extract_numbers_in_text(extract_text(td))
                )
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    article = extract_children_tag(soup, 'td', {"class" : "article-contents"}, is_child_multiple=False)
    var['post_image_url'] = search_img_list_in_contents(article, var['channel_main_url'])
    var['post_text'] = clean_text(
        extract_text(article)
    )
    thList = extract_children_tag(soup, 'th', child_tag_attrs={}, is_child_multiple=True)
    for th in thList :
        if extract_text(th) == '연락처':
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(
                    find_next_tag(th)
                )
            )
            if len(var['contact']) == 1 :
                var['contact'] = var['contact'][0]
            break

    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result

# jeju_6
def postListParsingProcess_other(**params):
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
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    return result

def postContentParsingProcess_other(**params):
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
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result

def parse_href(text):
    prefix = 'ice_id='
    suffix = '¤'
    result = text[text.find(prefix) + len(prefix) : text.find(suffix)]
    return result
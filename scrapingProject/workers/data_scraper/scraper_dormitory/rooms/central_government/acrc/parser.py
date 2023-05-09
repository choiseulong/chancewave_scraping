from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['view_count', 'post_title', 'uploader', 'uploaded_time', 'post_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    # contentsBox = extract_children_tag(soup, 'table', {'class' : 'boardList'}, is_child_multiple=False)
    contentsBox = extract_children_tag(soup, 'table', {'class' : 'tstyle_list'}, is_child_multiple=False)
    tbody = extract_children_tag(contentsBox, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    for tr in tr_list:
        td_list = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True)
        uploader_text = ''
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1 :
                var['post_title'].append(td_text)
                href = extract_attrs(
                    extract_children_tag(td, 'a', {'href' : True}, is_child_multiple=False),
                    'href'
                )
                if 'http' not in href :
                    href = var['channel_main_url'] + href
                var['post_url'].append(href)
            elif td_idx == 2 or td_idx == 3 :
                uploader_text += td_text + ' '
            elif td_idx == 4 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 5 :
                var['view_count'].append(extract_numbers_in_text(td_text))
        var['uploader'].append(uploader_text.strip())
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    # viewContent = extract_children_tag(soup, 'div', {'class' : 'viewContent'}, is_child_multiple=False)
    viewContent = extract_children_tag(soup, 'div', {'class' : 'contents'}, is_child_multiple=False)
    post_text = extract_text(viewContent)
    if post_text:
        var['post_text'] = clean_text(post_text)
    var['post_image_url'] = search_img_list_in_contents(viewContent, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

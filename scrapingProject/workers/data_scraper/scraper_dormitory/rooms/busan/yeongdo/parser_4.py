from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    post_list = extract_children_tag(soup, 'li', child_tag_attrs={'class':'li1'}, is_child_multiple=True)
    if type(post_list) == None:
        return
    for post in post_list:
        var['post_title'].append(
            extract_text_from_single_tag(post, 'strong')
        )
        a_tag = extract_children_tag(post, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['post_url_frame'] + href
        )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'uploaded_time', 'uploader', 'view_count'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_meta_data_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'info1'})
    tmp_meta_data = extract_children_tag(tmp_meta_data_box, 'dt', is_child_multiple=True)
    uploader = ''
    for meta_data in tmp_meta_data:
        meta_data_name = extract_text(meta_data)
        meta_data_value = extract_text(find_next_tag(meta_data))
        if '작성일' in meta_data_name:
            var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(meta_data_value)
        elif '작성자' in meta_data_name:
            uploader += meta_data_value
        elif '연락처' in meta_data_name:
            var['contact'] = meta_data_value
        elif '조회수' in meta_data_name:
            var['view_count'] = meta_data_value
    var['uploader'] = uploader
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'substance'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result
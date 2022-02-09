from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_thumbnail']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_post_list_box = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'gall_thumb'})
    post_list = extract_children_tag(tmp_post_list_box, 'li', is_child_multiple=True, is_recursive=False)
    if not post_list :
        return
    
    for post in post_list:
        a_tag = extract_children_tag(post, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url']+href
        )

        post_thumbnail = extract_children_tag(post, 'div', child_tag_attrs={'class':'thumb'})
        style = extract_attrs(post_thumbnail, 'style')
        src = extract_values_list_in_both_sides_bracket_text(style)[0]
        var['post_thumbnail'].append(
            var['channel_main_url'] + src
        )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title', 'uploaded_time', 'view_count'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_title_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board_view_head'})
    var['post_title'] = extract_text_from_single_tag(tmp_title_box, 'h6')

    tmp_meta_data_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board_view_info'})
    meta_data_list = extract_children_tag(tmp_meta_data_box, 'span', is_child_multiple=True)
    for meta_data in meta_data_list:
        meta_data_text = extract_text(meta_data)
        meta_data_text_split = meta_data_text.split(' : ')
        if '작성자' in meta_data_text:
            var['uploader'] = meta_data_text_split[1]
        elif '작성일' in meta_data_text:
            var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(
                meta_data_text_split[1]
            )
        elif '조회수' in meta_data_text:
            var['view_count'] = extract_numbers_in_text(meta_data_text_split[1])
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'board_view_body'})
    tmp_contents = decompose_tag(tmp_contents, 'div', child_tag_attrs={'class': 'koglSeView'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


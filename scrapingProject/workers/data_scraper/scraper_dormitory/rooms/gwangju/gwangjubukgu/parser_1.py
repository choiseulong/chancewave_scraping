from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'uploader', 'post_thumbnail']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_data_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'galleryList'})
    data_list = extract_children_tag(tmp_data_box, 'li', is_child_multiple=True)
    if not data_list :
        return
    
    for data in data_list :
        a_tag = extract_children_tag(data, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        var['post_title'].append(
            extract_text_from_single_tag(data, 'strong', child_tag_attrs={'class':'title'})
        )
        img = extract_children_tag(data, 'img')
        src = extract_attrs(img, 'src')
        var['post_thumbnail'].append(
            var['channel_main_url'] + src
        )
        meta_info_span_text = extract_text_from_single_tag(data, 'span', child_tag_attrs={'class':'date'})
        info_text_split = meta_info_span_text.split(' | ')
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                info_text_split[1]
            )
        )
        var['uploader'].append(
            info_text_split[0]
        )
    result = merge_var_to_dict(key_list, var)        
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact',],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_meta_info = extract_children_tag(soup, 'strong', is_child_multiple=True)
    for info in tmp_meta_info:
        info_text = extract_text(info)
        info_value = extract_text(find_next_tag(info))
        if '조회수' in info_text:
            var['view_count'] = extract_numbers_in_text(info_value)

    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'tb_contents'})
    sub_div = extract_children_tag(tmp_contents, 'div', is_child_multiple=True)
    if sub_div:
        sub_div_count = len(sub_div)
        for _ in range(sub_div_count): 
            tmp_contents = decompose_tag(tmp_contents, 'div')
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


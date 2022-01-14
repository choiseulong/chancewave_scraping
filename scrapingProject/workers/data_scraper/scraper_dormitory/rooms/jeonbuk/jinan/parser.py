from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    bbs_list = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'bbsList'})
    li_list = extract_children_tag(bbs_list, 'li', is_child_multiple=True)
    for li in li_list:
        notice_img = extract_children_tag(li, 'img')
        if notice_img :
            if '공지' in extract_attrs(notice_img, 'alt'):
                if var['page_count'] != 1 :
                    continue
        a_tag = extract_children_tag(li, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        var['post_title'].append(
            extract_attrs(a_tag, 'title')
        )
    
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'uploaded_time', 'view_count', 'uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    title_field = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'titleField'})
    li_list = extract_children_tag(title_field, 'li', is_child_multiple=True)
    for li_idx, li in enumerate(li_list):
        li_text = extract_text(li)
        li_text_split = li_text.split(' : ')[1].strip() if len(li_text.split(' : ')) == 2 else ''
        if li_idx == 0 :
            var['uploader'] = li_text_split
        elif li_idx == 1 :
            var['contact'] = li_text_split
        elif li_idx == 2 :
            var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(li_text_split)
        elif li_idx == 3 :
            var['view_count'] = extract_numbers_in_text(li_text)
    tmp_content = extract_children_tag(soup, 'div', {'class' : 'conText'})
    var['post_text'] = extract_text(tmp_content)
    if not var['contact'] :
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_content))
    var['post_image_url'] = search_img_list_in_contents(tmp_content, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    return result


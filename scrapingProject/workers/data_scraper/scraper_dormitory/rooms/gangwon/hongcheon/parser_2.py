from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'post_thumbnail']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    bbs_list = extract_children_tag(soup, 'div', child_tag_attrs={'class':'bbs_list'})
    if type(bbs_list) == type(None):
        print(var['channel_code'], 'CONT ERROR')
        return 
    contents_check_text = extract_text(bbs_list)
    if '등록된 게시물이 없습니다' in contents_check_text:
        return
    cont_list = extract_children_tag(soup, 'li', child_tag_attrs={'class':'list'}, is_child_multiple=True)
    for cont in cont_list :
        a_tag = extract_children_tag(cont, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['post_url_frame'] + href
        )
        post_title = extract_text_from_single_tag(cont, 'p', child_tag_attrs={'class':'title'})
        var['post_title'].append(
            post_title
        )
        img = extract_children_tag(cont, 'img')
        if img :
            src = extract_attrs(img, 'src')
            var['post_thumbnail'].append(
                var['channel_main_url'] + src
            )
        else:
            var['post_thumbnail'].append(None)
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_text_type'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_info = extract_children_tag(soup, 'th', child_tag_attrs={'scope':'row'}, is_child_multiple=True)
    extra_info = {'info_title':'행사상세'}
    var['post_text_type'] = 'both'
    for info in tmp_info:
        info_name = extract_text(info)
        info_value = extract_text(find_next_tag(info))
        extra_info.update({f'info_{len(extra_info)}' : (info_name, info_value)})
        if '문의전화' in info_name:
            var['contact'] = info_value
        elif '내용' in info_name:
            tmp_contents = find_next_tag(info)
            var['post_text'] = extract_text(tmp_contents)
            if not var['contact'] :
                var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
            var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    var['extra_info'].append(extra_info)
    result = convert_merged_list_to_dict(key_list, var)
    print(result)
    return result
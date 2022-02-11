from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'post_thumbnail']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    performance_wrap = extract_children_tag(soup, 'div', child_tag_attrs={'class':'performance_wrap'}, is_child_multiple=True)
    for con in performance_wrap:
        performance_pic = extract_children_tag(con, 'div', child_tag_attrs={'class':'performance_pic'})
        a_tag = extract_children_tag(performance_pic, 'a')
        onclick = extract_attrs(a_tag, 'onclick')
        post_id = parse_post_id(onclick, 0)
        var['post_url'].append(
            var['post_url_frame'].format(post_id)
        )
        post_thumbnail = extract_children_tag(performance_pic, 'img')
        src = extract_attrs(post_thumbnail, 'src')
        var['post_thumbnail'].append(
            var['channel_main_url'] + src
        )
        var['post_title'].append(
            extract_attrs(post_thumbnail, 'alt')
        )
    result = merge_var_to_dict(var=var, key_list=key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'start_date'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    extra_info = {'info_title':'공연/전시 상세'}
    tmp_info = extract_children_tag(soup, 'th', child_tag_attrs={'scope':'row'}, is_child_multiple=True)
    for info in tmp_info:
        info_text = extract_text(info)
        info_con_text = extract_text(find_next_tag(info))
        if '일시' in info_text:
            var['start_date'] = info_con_text
        elif '문의처' in info_text:
            var['contact'] = info_con_text
        elif '내용' in info_text:
            var['post_text'] = info_con_text
        extra_info.update({f'info_{len(extra_info)}':(info_text, info_con_text)})
    var['extra_info'].append(extra_info)
    image_gallery = extract_children_tag(soup, 'ul', child_tag_attrs={'id':'image-gallery'})
    var['post_image_url'] = search_img_list_in_contents(image_gallery, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


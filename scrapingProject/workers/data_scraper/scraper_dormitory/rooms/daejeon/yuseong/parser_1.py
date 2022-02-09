from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'uploader', 'post_thumbnail', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    post_list_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'obj col1'})
    post_list = extract_children_tag(post_list_box, 'div', is_child_multiple=True, is_recursive=False)
    for post in post_list:
        img = extract_children_tag(post, 'img')
        src = extract_attrs(img, 'src')
        var['post_thumbnail'].append(
            var['channel_main_url'] + src
        )
        a_tag = extract_children_tag(post, 'a')
        onclick = extract_attrs(a_tag, 'onclick')
        post_id = parse_post_id(onclick, 0)
        var['post_url'].append(
            var['post_url_frame'].format(post_id)
        )
        var['post_title'].append(
            extract_text_from_single_tag(post, 'strong')
        )
        meta_info = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'list_ul'})
        info_list = extract_children_tag(meta_info, 'li', is_child_multiple=True)
        for info_idx, info in enumerate(info_list):
            info_text =extract_text(info)
            if info_idx == 0:
                var['uploader'].append(info_text)
            elif info_idx == 1:
                var['view_count'].append(
                    extract_numbers_in_text(info_text)
                )
            elif info_idx == 2:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(info_text)
                )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact',],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'bbs--view--cont'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


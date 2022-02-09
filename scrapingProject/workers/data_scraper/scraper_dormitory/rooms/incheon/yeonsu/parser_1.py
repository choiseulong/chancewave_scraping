from cv2 import merge
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'post_thumbnail']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    li_list = extract_children_tag(soup, 'li', is_child_multiple=True)
    for li in li_list:
        img = extract_children_tag(li, 'p', child_tag_attrs={'class':'img'})
        if img:
            img_tag = extract_children_tag(img, 'img')
            src = extract_attrs(img_tag, 'src')
            var['post_thumbnail'].append(
                var['channel_main_url'] + src
            )
        else :
            var['post_thumbnail'].append(None)
        con = extract_children_tag(li, 'p', child_tag_attrs={'class':'con'})
        a_tag = extract_children_tag(con, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        var['post_title'].append(
            extract_text(a_tag)
        )
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text_from_single_tag(li, 'span', child_tag_attrs={'class':'date'})[:10]
            )
        )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact','view_count'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    dt_list = extract_children_tag(soup, 'dt', is_child_multiple=True)
    for dt in dt_list:
        dt_text = extract_text(dt)
        if '조회수' in dt_text:
            var['view_count'] =extract_numbers_in_text(
                    extract_text(find_next_tag(dt))
                )
            break
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'con'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


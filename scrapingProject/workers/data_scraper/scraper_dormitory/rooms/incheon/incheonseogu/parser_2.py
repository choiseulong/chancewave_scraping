from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import bs4

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'post_thumbnail', 'post_subject']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    poster_list_box = extract_children_tag(soup, 'div', child_tag_attrs={'id':'poster'})
    poster_list_box = extract_children_tag(poster_list_box, 'ul')
    poster_list = extract_children_tag(poster_list_box, 'li', is_child_multiple=True, is_recursive=False)
    if type(poster_list) == bs4.element.ResultSet :
        pass 
    elif type(poster_list) == type(None):
        raise f'{var["channel_code"]} CONTENTS LIST ERROR'
    for poster in poster_list:
        p_tag = extract_children_tag(poster, 'p', child_tag_attrs={'class':'img'})
        img = extract_children_tag(p_tag, 'img')
        src = extract_attrs(img, 'src')
        var['post_thumbnail'].append(
            var['channel_main_url'] + src
        )
        p_tag = extract_children_tag(poster, 'p', child_tag_attrs={'class':'tit'})
        var['post_title'].append(
            extract_text(p_tag)
        )
        p_tag = extract_children_tag(poster, 'p', child_tag_attrs={'class':'cate'})
        var['post_subject'].append(
            extract_text(p_tag)
        )
        a_tag = extract_children_tag(poster, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'start_date', 'end_date', \
            'post_content_target', 'linked_post_url'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tit_con = extract_children_tag(soup, 'div', child_tag_attrs={'class':'tit_con'})
    dt_list = extract_children_tag(tit_con, 'dt', is_child_multiple=True)
    extra_info={'info_title':'행사상세'}
    for dt in dt_list :
        dt_text = extract_text(dt)
        dd_text = extract_text(find_next_tag(dt))
        extra_info.update({f'info_{len(extra_info)}' : (dt_text, dd_text)})
        if '기간' in dt_text:
            dd_text_split = dd_text.split(' ~ ')
            if dd_text_split:
                if len(dd_text_split) > 0:
                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(dd_text_split[0])
                else :
                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(None)
                if len(dd_text) > 1:
                    var['end_date'] = convert_datetime_string_to_isoformat_datetime(dd_text_split[0])
                else :
                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(None)
        elif '홈페이지' in dt_text:
            var['linked_post_url'] = dd_text
        elif '대상' in dt_text:
            var['post_content_target'] = dd_text
    var['extra_info'].append(extra_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'con'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


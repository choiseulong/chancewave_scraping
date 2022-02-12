from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'post_thumbnail', 'start_date', 'end_date']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    post_list_box = extract_children_tag(soup, 'div', child_tag_attrs={'id':'list-frame-gallery'})
    post_list = extract_children_tag(post_list_box, 'li', is_child_multiple=True)
    for post in post_list:
        a_tag = extract_children_tag(post, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        img = extract_children_tag(post, 'img')
        src = extract_attrs(img, 'src')
        var['post_thumbnail'].append(
            var['channel_main_url'] + href
        )
        poster = extract_children_tag(post, 'div', child_tag_attrs={'class':'poster-con'}) 
        var['post_title'].append(
            extract_text_from_single_tag(poster, 'a')
        )
        dt_list = extract_children_tag(poster, 'dt', is_child_multiple=True)
        for dt in dt_list:
            dt_text = extract_text(dt)
            if '일시' in dt_text:
                dd_text = extract_text(find_next_tag(dt))
                start_date, end_date = parse_date(dd_text)
                var['start_date'].append(start_date)
                var['end_date'].append(end_date)
    result = merge_var_to_dict(var=var, key_list=key_list)
    return result

def parse_date(text):
    text_split = [convert_datetime_string_to_isoformat_datetime(_) for _ in text.split(' ~ ')]
    return text_split[0], text_split[1]


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact',],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_info = extract_children_tag(soup, 'dt', is_child_multiple=True)
    extra_info = {'info_title':'공연정보'}
    for info in tmp_info:
        info_text = extract_text(info)
        info_value_text = extract_text(find_next_tag(info))
        if '문의처' in info_text:
            var['contact'] =extract_contact_numbers_from_text(
                info_value_text
            )
        extra_info.update({f'info_{len(extra_info)}' : (info_text, info_value_text)})
    var['extra_info'].append(extra_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'culture-contents-data'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


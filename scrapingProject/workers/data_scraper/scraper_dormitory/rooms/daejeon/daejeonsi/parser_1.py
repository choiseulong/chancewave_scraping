from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-19
    var['table_header'] = ["번호", "사진", "행사명", "테마", "장소", "시작일", "종료일"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_thumbnail', 'start_date', 'end_date'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    event_photo = extract_children_tag(soup, 'p', child_tag_attrs={'class':'event_photo'})
    if event_photo:
        var['post_thumbnail'] = var['channel_main_url'] + extract_attrs(
            extract_children_tag(event_photo, 'img'), 'src'
        )
    else :
        var['post_thumbnail'] = None

    extra_info = {'info_title':'행사정보'}
    event = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'event'})
    event_li_list = extract_children_tag(event, 'li', is_child_multiple=True)
    for li in event_li_list:
        li_text = extract_text(li)
        li_text_split = li_text.split(' : ')
        if '기간' in li_text:
            li_text_split_twice = li_text_split[1].split('~')
            var['start_date'] = convert_datetime_string_to_isoformat_datetime(li_text_split_twice[0].strip())
            var['end_date'] = convert_datetime_string_to_isoformat_datetime(li_text_split_twice[1].strip())
        elif '문의' in li_text:
            var['contact'] = li_text_split[1]
        extra_info.update(
            {f'info_{len(extra_info)}' : (li_text_split[0], li_text_split[1])}
        )
    var['extra_info'] = extra_info
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board_txt02'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact'] :
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

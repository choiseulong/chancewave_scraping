from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_title', 'post_url', 'is_going_on']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-02-08
    var['table_header'] = ["강좌명", "교육기간", "수강신청기간", "교육기관", "수강료", "접수방법", "상태"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'start_date', 'start_date2', 'end_date', 'end_date2'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    date_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'t1'})
    date_list = extract_children_tag(date_box, 'span', is_child_multiple=True)
    for date in date_list:
        date_text = extract_text(date)
        if '교육기간' in date_text :
            var['start_date2'], var['end_date2'] = parse_date_text(date_text)
        elif '수강신청기간' in date_text:
            var['start_date'], var['end_date'] = parse_date_text(date_text)

    extra_info = {'info_title':'강좌소개상세'}
    tmp_meta_info = extract_children_tag(soup, 'th', child_tag_attrs={'scope':'row'}, is_child_multiple=True)
    for meta_info in tmp_meta_info:
        meta_info_name = extract_text(meta_info)
        meta_info_value = extract_text(find_next_tag(meta_info))
        extra_info.update({f'info_{len(extra_info)}' : (meta_info_name, meta_info_value)})
        if '문의전화' in meta_info_name:
            var['contact'] = meta_info_value
        elif '강의내용' in meta_info_name:
            tmp_contents = find_next_tag(meta_info)
            var['post_text'] = extract_text(tmp_contents)
            if not var['contact'] :
                var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
            var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    var['extra_info'].append(extra_info)
    result = convert_merged_list_to_dict(key_list, var)
    return result

def parse_date_text(text):
    text_split = text.split(' : ')[1].split(' ~ ')
    if len(text_split) == 2 :
        result = [convert_datetime_string_to_isoformat_datetime(_) for _ in text_split]
        return result[0], result[1]
    else :
        return None, None
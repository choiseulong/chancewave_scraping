from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'is_going_on']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-27
    var['table_header'] = ["강좌명", "대상", "교육기간", "장소", "접수방법", "접수상태"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'start_date', 'start_date2', 'end_date', 'end_date2', 'uploader'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    extra_info = {'info_title':'프로그램 상세'}
    tmp_meta_data = extract_children_tag(soup, 'th', child_tag_attrs={'scope':'row'}, is_child_multiple=True)
    for meta_data in tmp_meta_data:
        meta_data_title = extract_text(meta_data)
        meta_data_value = extract_text(find_next_tag(meta_data))
        extra_info.update({f'info_{len(extra_info)}' : (meta_data_title, meta_data_value)})
        if '접수일자' in meta_data_title:
            meta_data_value_split = [parse_date_text(_) for _ in meta_data_value.split(' ~ ')]
            var['start_date'] = convert_datetime_string_to_isoformat_datetime(meta_data_value_split[0])
            var['end_date'] = convert_datetime_string_to_isoformat_datetime(meta_data_value_split[1])
        elif '교육기간' in meta_data_title:
            meta_data_value_split = [parse_date_text(_) for _ in meta_data_value.split(' ~ ')]
            var['start_date2'] = convert_datetime_string_to_isoformat_datetime(meta_data_value_split[0])
            var['end_date2'] = convert_datetime_string_to_isoformat_datetime(meta_data_value_split[1])
        elif '문의전화' in meta_data_title:
            var['contact'] = meta_data_value
        elif '담당자' in meta_data_title:
            var['uploader'] = meta_data_value
    var['extra_info'] = extra_info
    tmp_contents = extract_children_tag(soup, 'td', child_tag_attrs={'class':'txtarea'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

def parse_date_text(text):
    return text.replace('년', '.').replace('월', '.').replace('일', '').replace(' ', '')

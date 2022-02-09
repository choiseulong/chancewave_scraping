from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['is_going_on', 'post_url', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-25 
    var['table_header'] = ["강좌명", "수강료", "접수기간", "교육기간", "교육기관", "상태"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'start_date', 'end_date',\
            'start_date2', 'end_date2'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_text_type'] = 'both'
    data_list = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'data_list'})
    dt_list = extract_children_tag(data_list, 'dt', is_child_multiple=True)
    extra_info = {'info_title':'교육상세'}
    for dt in dt_list:
        dt_text = extract_text(dt)
        dd_text = extract_text(find_next_tag(dt))
        if '문의전화' in dt_text:
            var['contact'] = extract_contact_numbers_from_text(dd_text)
        elif '접수기간' in dt_text :
            var['start_date'], var['end_date'] = parse_date(dd_text) if parse_date(dd_text) else (None, None)
        elif '교유기간' in dt_text:
            var['start_date2'], var['end_date2'] = parse_date(dd_text) if parse_date(dd_text) else (None, None)
        extra_info.update({f'info_{len(extra_info)}' : (dt_text, dd_text)})
    var['extra_info'] = extra_info
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'con'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

def parse_date(text):
    if '20' in text and '~' in text:
        text = text[text.find('20'):].split(' ~ ')
        return text[0], text[1]
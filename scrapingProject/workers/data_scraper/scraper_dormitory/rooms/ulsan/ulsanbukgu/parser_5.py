from pickle import NONE
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'view_count', 'post_subject', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-24 
    tbody_list = extract_children_tag(soup, 'tbody', is_child_multiple=True)
    var['table_data_box'] = tbody_list[-1]
    var['table_header'] = ["서비스유형", "서비스명", "제공기관", "서비스기간", "조회"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def parse_scripts_string(string, prefix):
    parse_text = extract_text_between_prefix_and_suffix(text=string, prefix=prefix, suffix=';')
    parse_text_split = parse_text.replace('"', '').split('::')
    if parse_text_split :
        return [i.strip() for i in parse_text_split]

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'start_date', 'end_date', 'start_date2', 'end_date2', 'post_content_target'],
        'multiple_type' : ['post_image_url',]
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    scripts = extract_children_tag(soup, 'script', is_child_multiple=True)
    for tag in scripts:
        if type(tag.string) != type(None):
            tag_string = tag.string
            if 'var etc08' in tag_string:
                parse_text_split = parse_scripts_string(tag_string, prefix='var etc08 =')
                date_info ={0:'start_date', 1:'end_date', 2:'start_date2', 3:'end_date2'}
                for text_idx, text in enumerate(parse_text_split) :
                    if text:
                        datetime_string = convert_datetime_string_to_isoformat_datetime(text)
                        var[date_info[text_idx]] = datetime_string
                    else :
                        var[date_info[text_idx]] = None
                parse_text_split = parse_scripts_string(tag_string, prefix='var etc10 =')
                if parse_text_split[0]:
                    var['post_content_target'] = parse_text_split[0]
                else :
                    var['post_content_target'] = None
    tmp_info = extract_children_tag(soup, 'th', child_tag_attrs={'scope':'row'}, is_child_multiple=True)
    for info in tmp_info:
        info_text = extract_text(info)
        info_con_text = extract_text(find_next_tag(info))
        if '연락처' in info_text:
            var['contact'] = info_con_text
    tmp_contents = extract_children_tag(soup, 'td', child_tag_attrs={'class':'contents'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


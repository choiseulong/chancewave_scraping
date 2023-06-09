from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 22-01-13
    var['table_header'] = ["번호", "제목", "등록일", "조회수"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def parse_uploaded_time(**params):
    text = params['child_tag_text']
    result = convert_datetime_string_to_isoformat_datetime(text)
    return result

def parse_post_url(**params):
    child_tag = params['child_tag']
    var = params['var']
    a_tag = extract_children_tag(child_tag, 'a')
    data_id = extract_attrs(a_tag, 'data-id')
    result = var['post_url_frame'].format(data_id)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'bbsV_cont'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'view_count', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-02-08
    var['table_header'] = ["번호", "제목", "글쓴이", "조회", "날짜"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def parse_post_url(**params):
    child_tag = params['child_tag']
    a_tag = extract_children_tag(child_tag, 'a')
    href = extract_attrs(a_tag, 'href')
    return href

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'uploaded_time'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(
        extract_text_from_single_tag(soup, 'strong', child_tag_attrs={'class':'if_date'}).replace('작성일', '').strip()
    )
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'id' : 'bo_v_con'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

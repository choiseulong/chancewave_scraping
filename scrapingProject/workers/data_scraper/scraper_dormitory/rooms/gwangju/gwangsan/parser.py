from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-17 
    var['table_header'] = ["번호", "제목", "작성자", "작성일", "조회"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'uploader', 'post_title'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    error_page = extract_children_tag(soup, 'div', child_tag_attrs={'class':'error_01'})
    if error_page:
        var['post_title'] = extract_text(error_page)
        return {}
    board_view = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board_view'})
    var['post_title'] = extract_text_from_single_tag(board_view, 'h4')
    var['contact'] = extract_contact_numbers_from_text(
        extract_text_from_single_tag(soup, 'li', child_tag_attrs={'class' : 'date'})
    )
    var['uploader'] = extract_text_from_single_tag(soup, 'li', child_tag_attrs={'class' : 'writer'}).replace('작성자', '')
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board_viewDetail'})
    tmp_contents = decompose_tag(tmp_contents, 'div', child_tag_attrs={'class':'mt50'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


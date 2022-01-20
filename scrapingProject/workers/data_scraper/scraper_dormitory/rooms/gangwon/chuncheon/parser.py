from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-17 
    var['table_header_box'] = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board-head'})
    var['table_data_box'] = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'board-body'})
    var['table_header'] = ["번호", "제목", "작성자", "작성일", "첨부"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def parse_uploaded_time(**params):
    text = params['child_tag_text'].replace('작성일', '').strip()
    result = convert_datetime_string_to_isoformat_datetime(text)
    return result

def parse_uploader(**params):
    return params['child_tag_text'].replace('작성자', '').strip()

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'view_count'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_info = extract_children_tag(soup, 'span', child_tag_attrs={'class':'tit'}, is_child_multiple=True)
    for info in tmp_info:
        info_text = extract_text(info)
        if '조회수' in info_text:
            var['view_count'] = extract_numbers_in_text(
                extract_text(find_next_tag(info))
            )
            break
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board-con'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


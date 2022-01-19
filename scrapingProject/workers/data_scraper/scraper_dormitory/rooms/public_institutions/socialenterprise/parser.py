from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-12
    var['table_header'] = ["번호", "제목", "첨부파일", "등록일", "등록자", "조회수"]
    result = parse_board_type_html_page(soup, var, key_list)
    print(result)
    return result

def parse_post_url(**params):
    child_tag = params['child_tag']
    var = params['var']
    post_url_frame = var['post_url_frame']
    a_tag = extract_children_tag(td, 'a')
    if a_tag.has_attr('onclick'):
        onclick = extract_attrs(a_tag, 'onclick')
        post_id = parse_post_id(onclick, 0)
        result = post_url_frame.format(post_id)
    else :
        href = extract_attrs(a_tag, 'href')
        result = var['channel_main_url'] + '/social/board/' + href
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'board_cont'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    print(result)
    return result


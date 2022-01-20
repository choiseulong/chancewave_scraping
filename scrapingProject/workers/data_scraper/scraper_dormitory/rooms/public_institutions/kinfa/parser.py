from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'view_count', 'post_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-10
    var['post_id_idx'] = 1
    var['table_header'] = ["번호", "제목", "첨부", "작성일", "조회"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def parse_post_url(**params):
    child_tag = params['child_tag']
    var = params['var']
    post_id = extract_attrs(child_tag, 'data-seqboardgeneral')
    result = var['post_url_frame'].format(post_id)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title', 'uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    thead = extract_children_tag(soup, 'thead')
    var['post_title'] = extract_text_from_single_tag(thead, 'th')
    tbody = extract_children_tag(soup, 'tbody')
    th_list = extract_children_tag(tbody, 'th', is_child_multiple=True)
    for th in th_list:
        th_text = extract_text(th)
        if '작성자' in th_text:
            var['uploader'] = extract_text(find_next_tag(th))
            break
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'board-view-text'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    return result
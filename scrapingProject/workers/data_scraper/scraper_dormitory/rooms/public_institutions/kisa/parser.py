from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'view_count', 'post_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-10
    var['table_header'] = ["번호", "제목", "게시일", "조회", "첨부"]
    result = parse_board_type_html_page(soup, var, key_list)  
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    tr_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    for tr_idx, tr in enumerate(tr_list) :
        if tr_idx == 0 :
            var['post_title'] = extract_text_from_single_tag(tr, 'strong')
        elif tr_idx == 1 :
            info_span_list = extract_children_tag(tr, 'span', is_child_multiple=True)
            for span_idx, span in enumerate(info_span_list):
                span_text = extract_text(span)
                if span_idx == 0 :
                    var['uploader'] = span_text
                elif span_idx == 1 :
                    var['contact'] = extract_contact_numbers_from_text(span_text)
    tmp_contents = extract_children_tag(soup, 'td', child_tag_attrs={'class' : 'view'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    return result


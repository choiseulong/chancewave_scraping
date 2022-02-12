from email.contentmanager import ContentManager
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    cont_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    for cont in cont_list:
        td_list = extract_children_tag(cont, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 0 and '공지' in td_text:
                if var['page_count'] != 1 :
                    continue
            
            if td_idx == 1:
                a_tag = extract_children_tag(td, 'a')
                href = extract_attrs(a_tag, 'href')
                post_id = parse_post_id(href, 0)
                var['post_url'].append(
                    var['post_url_frame'].format(post_id)
                )
            elif td_idx == 2:
                if td_text.endswith('.') :
                    td_text = td_text[:-1]
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
    result = merge_var_to_dict(key_list, var)
    # 2021-02-12
    # var['table_header'] = ["번호", "제목", "등록일", "첨부파일"]
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_title'] = extract_text_from_single_tag(soup, 'strong', child_tag_attrs={'class':'tit'})
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'viewCont'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


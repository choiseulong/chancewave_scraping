from email.contentmanager import ContentManager
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'view_count', "post_title"]
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    cont_list = extract_children_tag(tbody, 'tr', child_tag_attrs={"class" : False}, is_child_multiple=True)
    for cont in cont_list:
        td_list = extract_children_tag(cont, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 0 and '공지' in td_text:
                continue
            
            if td_idx == 1:
                a_tag = extract_children_tag(td, 'a')
                href = extract_attrs(a_tag, 'href')
                post_id = href.split('nttNo=')[1].split('&')[0]
                var['post_url'].append(
                    var['post_url_frame'].format(post_id)
                )
                var['post_title'].append(td_text)
            elif td_idx == 3:
                var['view_count'].append(extract_numbers_in_text(td_text))
            elif td_idx == 4 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text.strip())
                )
    result = merge_var_to_dict(key_list, var)
    # 2021-02-12
    # var['table_header'] = ["번호", "제목", "등록일", "첨부파일"]
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    text_div = extract_children_tag(soup, 'div', child_tag_attrs={"class" : "text"}, is_child_multiple=False)
    text = extract_text(text_div)
    var['post_text'] = text
    var['contact'] = extract_contact_numbers_from_text(text) 
    # var['post_title'] = extract_text_from_single_tag(soup, 'strong', child_tag_attrs={'class':'tit'})
    # tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'viewCont'})
    # var['post_text'] = extract_text(tmp_contents)
    # var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    # var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


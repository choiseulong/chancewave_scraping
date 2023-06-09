from turtle import onclick
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'view_count', 'post_title', 'post_subject']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    if type(tbody) == type(None):
        raise Exception(f'{var["channel_code"]}, DATA BOX IS NONETYPE')
    cont_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    for cont in cont_list :
        td_list = extract_children_tag(cont, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1:
                var['post_subject'].append(td_text)

            elif td_idx == 2:
                var['post_title'].append(td_text)
                a_tag = extract_children_tag(td, 'a')
                onclick = extract_attrs(a_tag, 'onclick')
                post_id = parse_post_id(onclick, 0)
                var['post_url'].append(
                    var['post_url_frame'].format(post_id)
                )
            elif td_idx == 4:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 6:
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
    # var['table_header'] = ["번호", "구분", "제목", "기간", "등록일", "첨부", "조회수"]
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'start_date', 'end_date', 'uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    th_list = extract_children_tag(soup, 'th', child_tag_attrs={'scope' : 'row'}, is_child_multiple=True)
    uploader = ''
    for th in th_list:
        th_text = extract_text(th)
        td_text = extract_text(find_next_tag(th))
        if '기간' in th_text:
            if '~' in td_text :
                th_text_split = td_text.split('~')
                var['start_date'] = convert_datetime_string_to_isoformat_datetime(th_text_split[0].strip())
                var['end_date'] = convert_datetime_string_to_isoformat_datetime(th_text_split[1].strip())
            else :
                var['start_date'] = None
                var['end_date'] = None 
        elif '전화번호' in th_text:
            var['contact'] = td_text
        elif '담당자' in th_text:
            uploader += td_text + ' '
        elif '담당부서' in th_text:
            uploader += td_text
    var['uploader'] = uploader
    tmp_contents = extract_children_tag(soup, 'td', child_tag_attrs={'class' : 'brdViewCont'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


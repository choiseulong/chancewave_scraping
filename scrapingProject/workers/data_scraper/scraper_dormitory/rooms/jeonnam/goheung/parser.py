from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'uploaded_time', 'view_count', 'uploader', 'post_title', 'post_subject']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    bd_list_body = extract_children_tag(soup, 'div', {'class' : 'bd_list_body'}, is_child_multiple=True)
    if not bd_list_body :
        return

    for bd in bd_list_body :
        p_list = extract_children_tag(bd, 'p', child_tag_attrs={}, is_child_multiple=True)
        uploader = ''
        # 2021-12-29 header [번호, 분류, 제목, 작성자, 작성일, 파일, 조회]
        for p_idx, p in enumerate(p_list):
            p_text = extract_text(p)
            if '공지' in p_text and p_idx == 0:
                if var['page_count'] == 1 :
                    pass
                else :
                    break
            if p_idx == 2 :
                a_tag = extract_children_tag(p, 'a', child_tag_attrs={}, is_child_multiple=False)
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['channel_main_url'] + href 
                )
                var['post_title'].append(
                    p_text
                )
            elif p_idx == 1 :
                var['post_subject'].append(p_text)
            elif p_idx in [3] :
                uploader += p_text + ' '
            elif p_idx == 6:
                var['view_count'].append(
                    extract_numbers_in_text(p_text)
                )
            elif p_idx == 4:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(p_text)
                )
        if '공지' not in p_text:
            var['uploader'].append(uploader)

    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    return result

def parse_href(text):
    return text

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    cont = extract_children_tag(soup, 'div', {'class' : 'bd_view_cont'}, is_child_multiple=False)
    var['post_text'] = extract_text(cont)
    var['contact'] = extract_contact_numbers_from_text(extract_text(cont))
    var['post_image_url'] = search_img_list_in_contents(cont, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result



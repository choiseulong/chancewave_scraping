from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'view_count', 'post_url', 'post_title', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    group_con = extract_children_tag(soup, 'div', child_tag_attrs={'class':'group_con'})
    ul_list = extract_children_tag(group_con, 'ul', is_child_multiple=True)
    for ul in ul_list :
        li_list = extract_children_tag(ul, 'li', is_child_multiple=True)
        for li_idx, li in enumerate(li_list):
            li_text = extract_text(li)
            if li_idx == 0 and '공지' in li_text:
                if var['page_count'] != 1 :
                    break
            
            if li_idx == 1:
                a_tag = extract_children_tag(li, 'a')
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['post_url_frame'] + href
                )
                var['post_title'].append(
                    li_text
                )
            elif li_idx == 2 :
                var['uploader'].append(li_text)
            elif li_idx == 4 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(li_text)
                )
            elif li_idx == 5 :
                var['view_count'].append(
                    extract_numbers_in_text(li_text)
                )
    result = merge_var_to_dict(key_list, var)
    # 2022-01-20 header ["번호", "제목", "작성자", "첨부파일", "작성일", "조회수"]\
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    li_list = extract_children_tag(soup, 'li', is_child_multiple=True)
    for li in li_list:
        li_text = extract_text(li)
        if '전화번호' in li_text:
            var['contact'] = extract_text(find_next_tag(li))
            break
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'view-con'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result
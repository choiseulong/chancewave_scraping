from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'view_count', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    # 2022-01-13 header = ["번호", "분류", "제목", "작성자", "등록일", "첨부파일", "조회수"]
    dbody = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'dbody'})
    ul_list = extract_children_tag(dbody, 'ul', is_child_multiple=True)
    for ul in ul_list:
        li_list = extract_children_tag(ul, 'li', is_child_multiple=True)
        for li_idx, li in enumerate(li_list):
            li_text = extract_text(li)
            if li_idx == 0 and '공지' in li_text:
                if var['page_count'] != 1:
                    continue
            if li_idx == 2 :
                a_tag = extract_children_tag(li, 'a')
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
                var['post_title'].append(extract_attrs(a_tag, 'title'))
            elif li_idx == 3:
                var['uploader'].append(li_text)
            elif li_idx == 4:
                var['uploaded_time'].append(li_text)
            elif li_idx == 6:
                var['view_count'].append(
                    extract_numbers_in_text(li_text)
                )
    
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact',],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'tb_contents'})
    scripts = extract_children_tag(tmp_contents, 'script', is_child_multiple=True)
    if scripts :
        pdf_url = var['channel_main_url'] + extract_values_list_in_both_sides_bracket_text(extract_text(scripts[1]))[0]
    var['post_text'] = extract_text(tmp_contents) if extract_text(tmp_contents) else pdf_url
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    return result


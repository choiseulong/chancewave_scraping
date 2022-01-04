from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'view_count', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_post_list = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'list_tit'}, is_child_multiple=True)
    # 2021-01-04 body [게시글 번호, ~과, 업로드날짜, 조회수, 제목, 축약 내용, 첨부파일] --> 열 형식 포스트가 아님
    for post in tmp_post_list:
        a_tag = extract_children_tag(post, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        var['post_title'].append(
            extract_text_from_single_tag(post, 'strong')
        )
        info_span = extract_children_tag(post, 'span', child_tag_attrs={'class' : 'info'})
        em_list = extract_children_tag(info_span, 'em', is_child_multiple=True)
        for em_idx, em in enumerate(em_list):
            em_text = extract_text(em)
            if em_idx == 0 :
                var['uploader'].append(em_text)
            elif em_idx == 1 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(em_text)
                )
            elif em_idx == 2 :
                var['view_count'].append(
                    extract_numbers_in_text(em_text)
                )
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'bbs_view'})
    composed_contents = decompose_tag(tmp_contents, 'div', child_tag_attrs={'class' : 'bbs_vtop'})
    if composed_contents:
        var['post_text'] = extract_text(composed_contents)
        var['contact'] = extract_contact_numbers_from_text(extract_text(composed_contents))
        var['post_image_url'] = search_img_list_in_contents(composed_contents, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result



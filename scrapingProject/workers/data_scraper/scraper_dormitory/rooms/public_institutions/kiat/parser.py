from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'view_count', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    post_list_box = extract_children_tag(soup, 'ul')
    post_list = extract_children_tag(post_list_box, 'li', is_child_multiple=True)
    for post in post_list:
        span_list = extract_children_tag(post, 'span', is_child_multiple=True)
        for span_idx, span in enumerate(span_list):
            span_text = extract_text(span)
            '''
                0 No.980 2022-01-05 View 223
                1 No.980
                2 2022-01-05
                3 View 223
                4 2022 정부R&D사업 온라인 부처합동 설명회 안내(1/25~27)
                5
            '''
            if span_idx == 0 :
                sub_span_text_list = [extract_text(sub_span_text) for sub_span_text in extract_children_tag(span, 'span', is_child_multiple=True)]
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(sub_span_text_list[1])
                )
                var['view_count'].append(
                    extract_numbers_in_text(sub_span_text_list[2])
                )
            if span_idx == 4 :
                var['post_title'].append(span_text)
                a_tag = extract_children_tag(span, 'a')
                href = extract_attrs(a_tag, 'href')
                post_id = parse_post_id(href, 0)
                var['post_url'].append(
                    var['post_url_frame'].format(post_id)
                )

    
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    info = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'infor2'})
    li_list = extract_children_tag(info, 'li', is_child_multiple=True)
    uploader = ''
    for li in li_list:
        li_text = extract_text(li)
        split_li_text = li_text.split(':')[1]
        if '담당부서' in li_text:
            uploader += split_li_text + ' '
        elif '담당자' in li_text:
            decompose_li = decompose_tag(li, 'a')
            uploader += extract_text(decompose_li).split(' : ')[1] 
        elif '연락처' in li_text:
            var['contact'] = split_li_text
    var['uploader'] = uploader
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'contents'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    return result


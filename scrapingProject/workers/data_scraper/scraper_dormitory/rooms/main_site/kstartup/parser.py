from workers.data_scraper.scraper_dormitory.parser_tools.tools import *



def post_list_parsing_process(**params):
    # update 23.04.27
    target_key_info = {
        'multiple_type' : [
            'post_subject', 'post_title', 'contents_req_params', 
            'view_count', 'uploader', 'end_date', 
            'uploaded_time'
        ]
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_div_list = extract_children_tag(soup, "li", {"class" : "notice"}, is_child_multiple=True)
    for content in content_div_list:
        a_tag = extract_children_tag(
            content,
            "a"
        )
        contents_req_params = extract_attrs(
            a_tag,
            "href"
        )
        contents_req_params = extract_numbers_in_text(contents_req_params)
        var['contents_req_params'].append(contents_req_params)

        post_title = extract_text(
            a_tag
        )
        var['post_title'].append(post_title)

        top_div = extract_children_tag(
            content,
            "div",
            {"class" : "top"}    
        )

        post_subject = extract_children_tag(
            top_div,
            "span",
            is_child_multiple = True
        )

        post_subject = extract_text(post_subject[0])
        var['post_subject'].append(post_subject)

        post_info = extract_children_tag(
            content,
            "span",
            {"class" : "list"},
            is_child_multiple = True
        )

        var["uploader"].append(
            extract_text(
                post_info[1]
            ) 
        )

        var["uploaded_time"].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    post_info[2]
                ).replace("등록일자 ", "")
            )
        )

        var["end_date"].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    post_info[3]
                ).replace("마감일자 ", "")
            )
        )

        var["view_count"].append(
            extract_numbers_in_text(
                extract_text(
                    post_info[4]
                )
            )
        )
        
    result = merge_var_to_dict(key_list, var)
    return result

    # CSRF_NONCE = extract_attrs(
    #     extract_children_tag(soup, 'input', {"name" : "CSRF_NONCE"}, is_child_multiple=False),
    #     'value'
    # )
    # cont_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board_list-wrap'})
    # cont_list = extract_children_tag(cont_box, 'li', is_child_multiple=True)
    # for cont in cont_list :
    #     var['post_subject'].append(
    #         extract_text_from_single_tag(cont, 'span', child_tag_attrs={'class': 'flag'})
    #     )
    #     a_tag = extract_children_tag(cont, 'a')
    #     href = extract_attrs(a_tag, 'href')
    #     post_id_list = parse_post_id(href, [0,1])
    #     req_params = {
    #         "CSRF_NONCE" : CSRF_NONCE,
    #         "mid" : 30004,
    #         "searchPrefixCode" : post_id_list[0],
    #         "searchPostSn" : post_id_list[1]
    #     }
    #     var['contents_req_params'].append(req_params)
    #     var['post_title'].append(
    #         extract_text_from_single_tag(cont, 'p', child_tag_attrs={'class':'tit'})
    #     )
    #     bottom_info = extract_children_tag(cont, 'div', child_tag_attrs={'class':'bottom'})
    #     info_list = extract_children_tag(bottom_info, 'span', child_tag_attrs={'class':'list'}, is_child_multiple=True)
    #     for info_idx, info in enumerate(info_list) :
    #         info_text = extract_text(info)
    #         if info_idx == 1:
    #             var['uploader'].append(info_text)
    #             continue
    #         if '등록일자' in info_text:
    #             var['uploaded_time'].append(
    #                 convert_datetime_string_to_isoformat_datetime(
    #                     info_text.replace('등록일자', '').strip()
    #                 )
    #             )
    #             continue
    #         elif '마감일자' in info_text:
    #             var['end_date'].append(
    #                 convert_datetime_string_to_isoformat_datetime(
    #                     info_text.replace('마감일자', '').strip()
    #                 )
    #             )
    #             continue
    #         elif '조회' in info_text:
    #             var['view_count'].append(
    #                 extract_numbers_in_text(info_text)
    #             )
    #             continue
    # result = merge_var_to_dict(key_list, var)
    # return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_content_target'],
        'multiple_type' : ['extra_info', 'post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    meta_data_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'bg_box'})
    meta_data = extract_children_tag(meta_data_box, 'li', child_tag_attrs={'class':'dot_list'}, is_child_multiple=True)
    extra_info = {'into_title':'모집상세'}
    post_content_target = ''
    for data in meta_data:
        data_name = extract_text_from_single_tag(data, 'p', child_tag_attrs={'class':'tit'})
        data_value = extract_text_from_single_tag(data, 'p', child_tag_attrs={'class':'txt'})
        if '연락처' in data_name:
            var['contact'] = data_value
        elif '대상' in data_name:
            post_content_target += data_value + ' '
        elif '창업기간' in data_name:
            post_content_target += data_value
        extra_info.update({f'info_{len(extra_info)}' : (data_name, data_value)})
    var['extra_info'].append(extra_info)
    var['post_content_target'] = post_content_target
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'k-notice_box'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result 

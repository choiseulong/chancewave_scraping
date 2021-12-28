from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    Board_list01 = extract_children_tag(soup, 'div', {'class' : 'Board_list01'}, DataStatus.not_multiple)
    contents = extract_children_tag(Board_list01, 'ul', DataStatus.empty_attrs, DataStatus.not_multiple)
    liList = extract_children_tag(contents, 'li', DataStatus.empty_attrs, DataStatus.multiple, DataStatus.not_recursive)
    if not liList :
        return
    for li in liList:
        spanList = extract_children_tag(li, 'span', DataStatus.empty_attrs, DataStatus.multiple)
        for span in spanList:
            spanText = extract_text(span)
            if spanText == '게시일' : 
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        extract_text(
                            find_next_tag(span)
                        )
                    )
                )
            elif spanText == '조회':
                var['view_count'].append(
                    extract_numbers_in_text(
                        extract_text(
                            find_next_tag(span)
                        )
                    )
                )
        a_tag = extract_children_tag(li, 'a', {'class' : 'title'}, DataStatus.not_multiple)
        var['post_title'].append(
                clean_text(extract_text(a_tag)
            )
        )
        post_url = extract_attrs(a_tag, 'href')
        if 'http' not in post_url :
            post_url = var['channel_main_url'] + post_url
        var['post_url'].append(post_url)
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text', 'uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    bv_tit_wrap = extract_children_tag(soup, 'div', {'class' : 'bv_tit_wrap'}, DataStatus.not_multiple)
    liList = extract_children_tag(bv_tit_wrap, 'li', DataStatus.empty_attrs, DataStatus.multiple)
    for li in liList:
        spanList = extract_children_tag(li, 'span', DataStatus.empty_attrs, DataStatus.multiple)
        for span in spanList:
            spanText = extract_text(span)
            if '담당자' in spanText or '담당부서' in spanText :
                var['uploader'] += extract_text(
                    find_next_tag(span)
                ) + ' '
            elif '전화번호' in spanText :
                var['contact'] = extract_contact_numbers_from_text(
                    extract_text(
                        find_next_tag(span)
                    )
                )
    bv_content_wrap = extract_children_tag(soup, 'div', {'class' : 'bv_content_wrap'}, DataStatus.not_multiple)
    var['post_text'] = extract_text(bv_content_wrap)
    img_list = extract_children_tag(bv_content_wrap, 'img', {'src' : True}, DataStatus.multiple)
    for img in img_list:
        src = extract_attrs(img, 'src')
        if 'http' not in src and 'base64' not in src :
            src = var['channel_main_url'] + src
        var['post_image_url'].append(src)

    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result
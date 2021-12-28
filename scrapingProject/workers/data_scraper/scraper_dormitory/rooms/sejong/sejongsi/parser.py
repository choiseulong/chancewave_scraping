from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params): 
    target_key_info = {
        'multiple_type' : ['uploader', 'post_title', 'view_count', 'post_url', 'uploaded_time']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    table = extract_children_tag(soup, 'table', {"class" : "board_list"}, DataStatus.not_multiple)
    tr_list = extract_children_tag(table, 'tr', DataStatus.empty_attrs, DataStatus.multiple)
    for tr in tr_list[1:] :
        td_list = extract_children_tag(tr, 'td', {"data-cell-header" : True}, DataStatus.multiple)
        for td in td_list:
            header = extract_attrs(td, 'data-cell-header')
            text = extract_text(td)
            a_tag = extract_children_tag(td, 'a', {"href" : True}, DataStatus.not_multiple)
            if header == '작성자':
                var['uploader'].append(text)
            elif header == '등록일':
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(text)
                )
            elif header == '조회수':
                var['view_count'].append(extract_numbers_in_text(text))
            elif header == '제목':
                var['post_title'].append(
                    clean_text(
                        text.replace('새글', '')
                    )
                )
                var['post_url'].append(
                    var['channel_main_url'] + \
                    extract_attrs(
                        a_tag,
                        'href'
                    )
                )
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_image_url'],
        'single_type' : ['post_text', 'contact']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    contentsBox = extract_children_tag(soup, 'div', {"class" : "bbs--view--cont"}, DataStatus.not_multiple)
    var['post_text'] = clean_text(
            extract_text(
            extract_children_tag(contentsBox, 'div', {'class' : 'bbs--view--content'}, DataStatus.not_multiple)
        )
    )
    var['contact'] = extract_contact_numbers_from_text(var['post_text'])
    var['post_image_url'] = search_img_list_in_contents(contentsBox, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result
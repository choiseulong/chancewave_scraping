from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'post_content_target', 'linked_post_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-24 
    var['table_header'] = ["강좌명", "대상자", "정원", "접수기간", "교육기간", "수강료(원)", "바로가기"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'uploader', 'uploaded_time', 'view_count', \
            'start_date', 'start_date2', 'end_date', 'end_date2', 'post_text_type'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_text_type'] = 'both'
    tmp_info = extract_children_tag(soup, 'tr', child_tag_attrs={'class':False})
    td_list = extract_children_tag(tmp_info, 'td')
    for td_idx, td in enumerate(td_list):
        td_text = extract_text(td)
        if td_idx == 0 :
            var['uploader'] = td_text
        elif td_idx == 1 :
            var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(td_text.strip())
        elif td_idx == 2 :
            var['view_count'] = extract_numbers_in_text(td_text)
    extra_info = {'info_title' : '강좌상세'}
    tmp_info = extract_children_tag(soup, 'tr', is_child_multiple=True, 
        child_tag_attrs={'class':'view_lifelong_learning'})
    for info in tmp_info:
        td_list = extract_children_tag(info, 'td', is_child_multiple=True)
        for td in td_list:
            td_text = extract_text(td)
            span_text = extract_text_from_single_tag(td, 'span')
            extra_info.update({f'info_{len(extra_info)}' : (span_text, td_text.replace(span_text, ''))})
            if '접수기간' in span_text:
                if '~' in td_text:
                    split_text = td_text.replace(span_text, '').split('~')
                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(split_text[0].strip())
                    var['end_date'] = convert_datetime_string_to_isoformat_datetime(split_text[1].strip())
                else :
                    var['start_date'] = None
                    var['end_date'] = None
            elif '교육기간' in span_text:
                if '~' in td_text:
                    split_text = td_text.replace(span_text, '').split('~')
                    var['start_date2'] = convert_datetime_string_to_isoformat_datetime(split_text[0].strip())
                    var['end_date2'] = convert_datetime_string_to_isoformat_datetime(split_text[1].strip())
                else :
                    var['start_date2'] = None
                    var['end_date2'] = None
    var['extra_info'] = extra_info
    tmp_contents = extract_children_tag(soup, 'td', child_tag_attrs={'class':'cont'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


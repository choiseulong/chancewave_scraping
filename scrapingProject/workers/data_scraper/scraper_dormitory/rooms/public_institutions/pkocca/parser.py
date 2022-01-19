from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'view_count', 'post_url', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    body_row_list = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'body_row'}, is_child_multiple=True)
    for div in body_row_list:
        subject = extract_children_tag(div, 'a')
        var['post_url'].append(
            var['channel_main_url'] + \
            extract_attrs(
                subject, 'href'
            )
        )
        var['post_title'].append(extract_text(subject)) 
        var['view_count'].append(
            extract_numbers_in_text(
                extract_text_from_single_tag(div, 'div', child_tag_attrs={'class' : 'hit'})
            )
        )
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text_from_single_tag(div, 'div', child_tag_attrs={'class' : 'date'})
            )
        )
    
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_subject'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    board_view_info = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'board_view_info'})
    span_list = extract_children_tag(board_view_info, 'span', is_child_multiple=True)
    for span in span_list:
        span_text = extract_text(span)
        if '분류' in span_text:
            var['post_subject'] = span_text.replace('분류', '')
            break
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board_view_body'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    return result


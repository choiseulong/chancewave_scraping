from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    list_box = extract_children_tag(soup, 'ul', child_tag_attrs={'class' : 'list_box'})
    list_tit = extract_children_tag(list_box, 'div', child_tag_attrs={'class':'list_tit'}, is_child_multiple=True)
    for div in list_tit:
        a_tag = extract_children_tag(div, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        var['post_title'].append(
            extract_text_from_single_tag(div,'strong')
        )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'uploaded_time', 'view_count', 'uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    bbs_vtop = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'bbs_vtop'})
    span_list = extract_children_tag(bbs_vtop, 'span', is_child_multiple=True)
    for span_idx, span in enumerate(span_list):
        span_text = extract_text(span)
        if span_idx == 0 :
            var['uploader'] = span_text
        elif span_idx == 1 :
            var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(span_text)
        elif span_idx == 2 :
            var['view_count'] = extract_numbers_in_text(span_text)
    tmp_content = extract_children_tag(soup, 'div', {'class' : 'bbs_con'})
    var['post_text'] = extract_text(tmp_content)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_content))
    var['post_image_url'] = search_img_list_in_contents(tmp_content, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


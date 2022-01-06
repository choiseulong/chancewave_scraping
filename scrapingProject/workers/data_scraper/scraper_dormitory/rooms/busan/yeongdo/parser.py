from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'uploaded_time', 'view_count', 'uploader', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    contents_list = extract_children_tag(soup, 'li', is_child_multiple=True, child_tag_attrs={'class' :'li1'})
    for cont in contents_list:
        a_tag = extract_children_tag(cont, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['post_url_frame'] + href
        )
        var['post_title'].append(
            extract_text_from_single_tag(cont, 'strong')
        )
        i_tag = extract_children_tag(cont, 'i', child_tag_attrs={'class' :'wrap1t3'})
        span_list = extract_children_tag(i_tag, 'span', is_child_multiple=True)
        for span_idx, span in enumerate(span_list):
            span_text = extract_text(span)
            if span_idx == 0 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(span_text)
                )
            elif span_idx == 1 :
                var['uploader'].append(
                    span_text
                )
            elif span_idx == 2 :
                var['view_count'].append(
                    extract_numbers_in_text(span_text)
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
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'substance'})
    var['post_text'] = extract_text(tmp_contents)
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result


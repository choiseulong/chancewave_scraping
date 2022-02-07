from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'uploader', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_cont_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'bloglist-wrap'})
    cont_list = extract_children_tag(tmp_cont_box, 'li', is_child_multiple=True)
    for cont in cont_list:
        a_tag = extract_children_tag(cont, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['post_url_frame'] + href
        )
        var['post_title'].append(
            extract_text_from_single_tag(cont, 'span', child_tag_attrs={'class':'btxt'})
        )
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text_from_single_tag(cont, 'span', child_tag_attrs={'class':'date'})
            )
        )
        var['uploader'].append(
            extract_text_from_single_tag(cont, 'span', child_tag_attrs={'class':'cate'})
        )
        var['view_count'].append(
            extract_numbers_in_text(
                extract_text_from_single_tag(cont, 'span', child_tag_attrs={'class':'date'})
            )
        )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'con'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

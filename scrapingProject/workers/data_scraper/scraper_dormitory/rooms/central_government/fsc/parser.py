from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['view_count', 'post_title', 'uploader', 'uploaded_time', 'post_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    contetnsBox = extract_children_tag(soup, 'div', {'class' : 'board-list-wrap'}, DataStatus.not_multiple)
    innerDiv = extract_children_tag(contetnsBox, 'div', {'class' : 'inner'}, DataStatus.multiple)
    for div in innerDiv :
        var['view_count'].append(
            extract_numbers_in_text(
                extract_text(
                    extract_children_tag(div, 'div', {'class' : 'info'}, DataStatus.not_multiple)
                )
            )
        )
        subject = extract_children_tag(div, 'div', {'class' : 'subject'}, DataStatus.not_multiple)
        var['post_title'].append(
            extract_text(
                subject
            )
        )
        href = extract_attrs(
            extract_children_tag(subject, 'a', DataStatus.empty_attrs, DataStatus.not_multiple),
            'href'
        )
        if 'http' not in href:
            href = var['channel_main_url'] + href
        var['post_url'].append(href)
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    extract_children_tag(div, 'div', {'class' : 'day'}, DataStatus.not_multiple)
                )
            )
        )


    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    return result

def parse_href(text):
    prefix = "('"
    suffix = "')"
    result = text[text.find(prefix) + len(prefix) : text.find(suffix)]
    return result

    
def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text'],
        'multiple_type' : ['post_image_url', 'contact']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    contents = extract_children_tag(soup, 'td', {'class' : 'bbs_content'}, DataStatus.not_multiple)
    post_text = extract_text(contents)
    if post_text:
        var['post_text'] = clean_text(post_text)
        var['contact'] = extract_contact_numbers_from_text(post_text)
    var['post_image_url'] = search_img_list_in_contents(contents, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result

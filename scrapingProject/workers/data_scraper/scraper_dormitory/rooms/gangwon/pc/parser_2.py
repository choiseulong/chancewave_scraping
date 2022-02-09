from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['start_date', 'post_url', 'post_title', 'post_thumbnail']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    show_list = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'show_list'})
    cont_list = extract_children_tag(show_list, 'li', is_child_multiple=True, is_recursive=False)
    for cont in cont_list :
        img = extract_children_tag(cont, 'img')
        src = extract_attrs(img, 'src')
        var['post_thumbnail'].append(
            var['channel_main_url'] + src
        )
        a_tag = extract_children_tag(cont, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        var['post_title'].append(
            extract_text_from_single_tag(cont, 'strong', child_tag_attrs={'class':'title'})
        )
        date_text = extract_text_from_single_tag(cont, 'span', child_tag_attrs={'class':'date'})
        parsed_date_text = parse_date_text(date_text)
        if parsed_date_text:
            var['start_date'].append(
                convert_datetime_string_to_isoformat_datetime(parsed_date_text)
            )
        else :
            var['start_date'].append(None)
    result = merge_var_to_dict(key_list, var)
    return result

def parse_date_text(text):
    date_text_split = text.split(' : ')
    if len(date_text_split) == 2:
        date_text_split = text.split(' : ')[1]
        parsed_date_text = date_text_split[:date_text_split.find('(')-1].replace(' ', '')
        return parsed_date_text
    else :
        return None

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_text_type'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_text_type'] = 'both'
    extra_info = {'info_title':'공연상세'}
    info_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'show_detail_table'})
    info_list = extract_children_tag(info_box, 'dt', is_child_multiple=True)
    for info in info_list:
        info_name = extract_text(info)
        info_value = extract_text(find_next_tag(info))
        extra_info.update({f'info_{len(extra_info)}':(info_name, info_value)})
    var['extra_info'].append(extra_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'show_box'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'img_box'})
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


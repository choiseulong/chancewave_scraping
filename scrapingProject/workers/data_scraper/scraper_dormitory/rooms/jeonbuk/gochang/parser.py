from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    bbs_list = extract_children_tag(soup, 'ul', child_tag_attrs={'class' : 'bbs_list'})
    li_list = extract_children_tag(bbs_list, 'li', is_child_multiple=True)
    for li in li_list:
        a_tag = extract_children_tag(li, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        var['post_title'].append(
            extract_text_from_single_tag(li, 'strong')
        )

    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    return result
    
def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'uploaded_time', 'view_count', 'uploader', 'start_date', 'end_date'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    bbs_vtop = extract_children_tag(soup, 'div', child_tag_attrs={'class':'bbs_vtop'})
    li_list = extract_children_tag(bbs_vtop, 'li', is_child_multiple=True)
    for li in li_list :
        li_text = extract_text(li)
        li_text_split = li_text.split(' : ')[1] if len(li_text.split(' : ')) == 2 else ''
        if '작성자' in li_text:
            var['uploader'] = li_text_split
        elif '작성일' in li_text:
            var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(li_text_split)
        elif '조회수' in li_text:
            var['view_count'] = extract_numbers_in_text(li_text) 
        elif '신청기간' in li_text:
            date_text = extract_text(extract_children_tag(li, 'span'))
            date_text_split = date_text.split(' ~ ')
            if len(date_text_split) == 2 :
                var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_text_split[0])
                var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_text_split[1])
        elif '번호' in li_text:
            var['contact'] = extract_text(extract_children_tag(li, 'a'))
    tmp_content = extract_children_tag(soup, 'div', {'class' : 'bbs_con'})
    var['post_text'] = extract_text(tmp_content)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_content))
    var['post_image_url'] = search_img_list_in_contents(tmp_content, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result

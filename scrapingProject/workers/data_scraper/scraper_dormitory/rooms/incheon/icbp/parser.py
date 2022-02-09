from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    generalList = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'generalList'})
    li_list = extract_children_tag(generalList, 'li', is_child_multiple=True, is_recursive=False)
    if not li_list :
        return
    elif type(li_list) == type(None):
        raise f'{var["channel_code"]} CONTENTS LIST ERROR'

    for li in li_list :
        title = extract_children_tag(li, 'p', child_tag_attrs={'class':'title'})
        var['post_title'].append(
            extract_text(title).replace('new', '')
        )
        a_tag = extract_children_tag(title, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        center_li = extract_children_tag(li, 'li', child_tag_attrs={'class':'center'})
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(center_li)
            )
        )
    result = merge_var_to_dict(var=var, key_list=key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact','uploader', 'view_count'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    dt_list = extract_children_tag(soup, 'dt', is_child_multiple=True)
    for dt in dt_list:
        dt_text = extract_text(dt)
        dd_text = extract_text(find_next_tag(dt))
        if '전화번호' in dt_text:
            var['contact'] = dd_text
        elif '작성자' in dt_text:
            var['uploader'] = dd_text
        elif '조회수' in dt_text :
            var['view_count'] = extract_numbers_in_text(dd_text)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'detail'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


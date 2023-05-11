from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, "tbody", is_child_multiple=False)
    tr_list = extract_children_tag(tbody, "tr", is_child_multiple=True)
    for tr in tr_list:
        td_list = extract_children_tag(tr, "td", is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 0 and td_text == '공지':
                if var['page_count'] != 1 :
                    continue
            
            elif td_idx == 1 :
                a_tag = extract_children_tag(td, "a")
                onclick = extract_attrs(a_tag, "onclick")
                post_num = extract_values_list_in_both_sides_bracket_text(onclick)[1]
                var['post_url'].append(
                    var['post_url_frame'].format(post_num.strip())
                )
            elif td_idx == 2 :
                var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(td_text))
            elif td_idx == 4 :
                var['view_count'].append(td_text)
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', "post_title"],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    title_dl = extract_children_tag(soup, "dl", child_tag_attrs={"class" : "title"}, is_child_multiple=False)
    var['post_title'] = extract_text(title_dl).replace("제목", "")
    content = extract_children_tag(soup, "dl", child_tag_attrs={"class" : "content"}, is_child_multiple=False)
    var['post_text'] = extract_text(content)
    var['post_image_url'] = search_img_list_in_contents(content, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


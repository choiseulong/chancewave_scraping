from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'uploader', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    cont_box = extract_children_tag(soup, 'tbody')
    cont_list = extract_children_tag(cont_box, 'tr', is_child_multiple=True)
    for cont in cont_list:
        td_list = extract_children_tag(cont, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1 :
                a_tag = extract_children_tag(td, 'a')
                if type(a_tag) == type(None):
                    break
                href = extract_attrs(a_tag, 'href') 
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
            elif td_idx == 2:
                var['uploader'].append(td_text)
            elif td_idx == 3:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 4:
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )

    # dongnae_2 ['번호', '제목', '작성자', '작성일', '조회수', '파일']

    result = merge_var_to_dict(key_list, var)
    return result



def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_title'] = extract_text_from_single_tag(soup, 'td', child_tag_attrs={'class':'subject'})
    contents = extract_children_tag(soup, 'tbody', child_tag_attrs={'class':'tb'})
    tr_list = extract_children_tag(contents, 'tr', is_child_multiple=True)
    tmp_contents = tr_list[2]
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

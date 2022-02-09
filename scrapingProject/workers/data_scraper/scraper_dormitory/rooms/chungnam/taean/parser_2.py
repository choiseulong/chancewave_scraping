from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'uploader', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    # 2021-01-25 header ["순번", "제목", "부서명", "등록일", "조회", "첨부"]
    tbody = extract_children_tag(soup, 'tbody')
    tr_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    for tr in tr_list:
        td_list = extract_children_tag(tr, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1:
                form = extract_children_tag(td, 'form')
                input_list = extract_children_tag(form, 'input', is_child_multiple=True, child_tag_attrs={'name':True})
                post_url_params = ''
                for input in input_list:
                    input_name = extract_attrs(input, 'name')
                    input_value = extract_attrs(input, 'value')
                    post_url_params += input_name + '=' + input_value + '&'
                var['post_url'].append(
                    var['post_url_frame'] + post_url_params
                )
                submit_input = extract_children_tag(td, 'input', child_tag_attrs={'type':'submit'})
                var['post_title'].append(
                    extract_attrs(submit_input, 'value')
                )
            elif td_idx == 2:
                var['uploader'].append(td_text)
            elif td_idx == 3:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text.strip())
                )
            elif td_idx == 4:
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'bbs_detail_content'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


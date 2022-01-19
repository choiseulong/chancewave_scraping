from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'view_count', 'post_url', 'post_title', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    board_box = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'board_type01'})
    li_list = extract_children_tag(board_box, 'li', is_child_multiple=True)
    for li in li_list:
        a_tag = extract_children_tag(li, 'a')
        onclick = extract_attrs(a_tag, 'onclick')
        post_id_params = parse_post_id(onclick, [0, 1])
        var['post_url'].append(
            var['post_url_frame'].format(post_id_params[0], post_id_params[1])
        )
        var['post_title'].append(
            extract_text_from_single_tag(li, 'span', child_tag_attrs={'class' : 'subject'})
        )
        span_writer = extract_children_tag(li, 'span', child_tag_attrs={'class':'writer'})
        em_list = extract_children_tag(span_writer, 'em', is_child_multiple=True)
        uploader = ''
        for em in em_list:
            uploader += extract_text(em) + ' '
        var['uploader'].append(uploader)
        span_src_text = extract_text(
            extract_children_tag(li, 'span', child_tag_attrs={'class' : 'src'})
        )
        span_src_text_split = span_src_text.split('조회수')
        var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(
                span_src_text_split[0].strip()
            )
        )
        var['view_count'].append(
            extract_numbers_in_text(span_src_text_split[1])
        )
    
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'con_area'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    return result


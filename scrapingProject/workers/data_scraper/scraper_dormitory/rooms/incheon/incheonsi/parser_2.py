from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'post_thumbnail', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    board_list_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board-card-list'})
    board_list = extract_children_tag(board_list_box, 'li', is_child_multiple=True)
    for board in board_list:
        a_tag = extract_children_tag(board, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        img = extract_children_tag(board, 'img')
        src = extract_attrs(img, 'src')
        var['post_thumbnail'].append(
            var['channel_main_url'] + src
        )
        alt = extract_attrs(img, 'alt')
        var['post_title'].append(
            extract_text_from_single_tag(board, 'p', child_tag_attrs={'class':'subject'})
        )
        meta = extract_children_tag(board, 'div', child_tag_attrs={'class':'meta'})
        span_list = extract_children_tag(meta, 'span', is_child_multiple=True)
        for span_idx, span in enumerate(span_list):
            span_text = extract_text(span)
            if span_idx == 0:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(span_text)
                )
            elif span_idx == 1:
                var['view_count'].append(
                    extract_numbers_in_text(span_text)
                )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact','uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    dt_list = extract_children_tag(soup, 'dt', is_child_multiple=True)
    for dt in dt_list:
        dt_text = extract_text(dt)
        dd_text = extract_text(find_next_tag(dt))
        if '담당부서' in dt_text:
            var['contact'] = extract_contact_numbers_from_text(dd_text)
            if '(' in dd_text:
                dd_text = dd_text[:dd_text.find('(')]
            var['uploader'] = dd_text
            break
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board-view-contents'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


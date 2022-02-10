from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'end_date', 'start_date', 'post_thumbnail']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_cont_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'bbs_list'})
    if type(tmp_cont_box) == type(None):
        print(var['channel_code'], 'TMP_CONT_BOX ERROR')
        return
    tmp_cont_box = extract_children_tag(tmp_cont_box, 'ul')
    cont_list = extract_children_tag(tmp_cont_box, 'li', is_child_multiple=True, is_recursive=False)
    for cont in cont_list :
        a_tag = extract_children_tag(cont, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        var['post_title'].append(
            extract_text(a_tag)
        )
        dt_span_list = extract_children_tag(cont, 'span', is_child_multiple=True, child_tag_attrs={'class':'dt'})
        for span in dt_span_list:
            span_text = extract_text(span)
            if '기간' in span_text:
                date_text = extract_text(find_next_tag(span))
                start_date, end_date = parse_date_text(date_text)
                var['start_date'].append(start_date)
                var['end_date'].append(start_date)
        img = extract_children_tag(cont, 'img')
        src = None
        if img:
            src = extract_attrs(img, 'src')
        if src :
            var['post_thumbnail'].append(
                var['channel_main_url'].replace('www', '') + src
            )
        else :
            var['post_thumbnail'].append(
                None
            )
    result = merge_var_to_dict(key_list, var)
    return result

def parse_date_text(text):
    text_split = text.split(' ~ ')
    if len(text_split) == 2 :
        result = [convert_datetime_string_to_isoformat_datetime(_) for _ in text_split]
        return result[0], result[1]
    else:
        return None, None

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact','post_text_type'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    txt_list = extract_children_tag(soup, 'div', child_tag_attrs={'class':'txt_list'})
    span_list = extract_children_tag(txt_list, 'span', child_tag_attrs={'class':'dt'}, is_child_multiple=True)
    extra_info = {'info_title':'행사상세'}
    for span in span_list:
        span_name = extract_text(span)
        span_value = extract_text(find_next_tag(span))
        extra_info.update({f'info:{len(extra_info)}' : (span_name, span_value)})
    var['extra_info'].append(extra_info)
    var['post_text_type'] = 'both'
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'program'})
    tmp_contents = decompose_tag(tmp_contents, 'div', child_tag_attrs={'class':'detail_screen_box'})
    tmp_contents = decompose_tag(tmp_contents, 'div', child_tag_attrs={'class':'btn_group'})
    tmp_contents = decompose_tag(tmp_contents, 'h3')
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


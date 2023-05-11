from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'start_date', "end_date", 'view_count', 
                           'uploader', 'post_title', "is_going_on", "post_thumbnail"]
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    board_result_div = extract_children_tag(soup, 'div', child_tag_attrs={"class" : "board_result"}, is_child_multiple=False)
    li_list = extract_children_tag(board_result_div, "li", is_child_multiple=True)
    
    for li in li_list:
        spt_state = extract_children_tag(li, "div", child_tag_attrs={"class" : "spt_state"}, is_child_multiple=False)
        if spt_state:
            spt_state_text = extract_text(spt_state)
            if spt_state_text == "모집중" :
                var['is_going_on'].append(True)
            else:
                var['is_going_on'].append(False)

        else:
            var['is_going_on'].append(True)
        photo2_area = extract_children_tag(li, "div", child_tag_attrs={"class" : "photo2_area"}, is_child_multiple=False)
        post_thumbnail = extract_children_tag(photo2_area, 'img', is_child_multiple=False)
        post_thumbnail_url = extract_attrs(post_thumbnail, 'src')
        var['post_thumbnail'].append(var['post_url_frame'] + post_thumbnail_url)

        photo2_tit = extract_children_tag(li, "div", child_tag_attrs={"class" : "photo2_tit"}, is_child_multiple=False)
        var['post_title'].append(extract_text(photo2_tit))
        a_tag = extract_children_tag(photo2_tit, "a")
        href = extract_attrs(a_tag, "href")
        var['post_url'].append(var['post_url_frame'] + href)
        info_box2 = extract_children_tag(li, "div", child_tag_attrs={"class" : "info_box2"}, is_child_multiple=False)
        dd_list = extract_children_tag(info_box2, "dd", is_child_multiple=True)
        for dd_idx, dd in enumerate(dd_list):
            dd_text = extract_text(dd)
            if dd_idx == 0 :
                date_string = [i.strip() if i.strip() else '' for i in dd_text.split("~")]
                for i in range(2):
                    if i == 0 :
                        if date_string[i] :
                            var['start_date'].append(convert_datetime_string_to_isoformat_datetime(date_string[0]))
                        else:
                            var['start_date'].append('')
                    elif i == 1 :
                        if date_string[i] :
                            var['end_date'].append(convert_datetime_string_to_isoformat_datetime(date_string[1]))
                        else:
                            var['end_date'].append('')
            elif dd_idx == 1 :
                var['uploader'].append(dd_text)
            elif dd_idx == 2:
                var['view_count'].append(dd_text)
    result = merge_var_to_dict(key_list, var)

    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_content_target', "post_text"],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    dt_list_div = extract_children_tag(soup, 'div', child_tag_attrs={"class" : "dt_list"}, is_child_multiple=False)
    dt_list = extract_children_tag(dt_list_div, "dt", is_child_multiple=True)
    for dt_idx, dt in enumerate(dt_list):
        dt_text = extract_text(dt)
        dd_text = extract_text(find_next_tag(dt))
        if '문의' in dt_text:
            var['contact'] = dd_text
        elif '지원대상' in dt_text:
            var['post_content_target'] = dd_text

    cont_img_div = extract_children_tag(soup, "div", child_tag_attrs={"class" : "cont_img"}, is_child_multiple=False)
    cont_img = extract_children_tag(cont_img_div, "img", is_child_multiple=True)
    if cont_img:
        for img in cont_img:
            src = extract_attrs(img, "src")
            var['post_image_url'].append(src)
    
    text_div = extract_children_tag(soup, "div", child_tag_attrs={"class" : "text"}, is_child_multiple=False)
    var['post_text'] = extract_text(text_div)
    result = convert_merged_list_to_dict(key_list, var)
    return result


from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'post_thumbnail', 'start_date', 'end_date', 'contact', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_cont_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'bbs_gallery3'})
    cont_list = extract_children_tag(tmp_cont_box, 'dl', is_child_multiple=True)
    if type(cont_list) == type(None):
        return
    for cont in cont_list:
        a_tag = extract_children_tag(cont, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        var['post_title'].append(
            extract_text(a_tag)
        )
        img = extract_children_tag(cont, 'img')
        src = extract_attrs(img, 'src')
        var['post_thumbnail'].append(
            var['channel_main_url'] + src
        )
        tmp_meta_info_box = extract_children_tag(cont, 'dd', child_tag_attrs={'class':'infor'})
        meta_info_list = extract_children_tag(tmp_meta_info_box, 'li', is_child_multiple=True)
        for meta_info in meta_info_list:
            meta_info_text = extract_text(meta_info)
            if '기간' in meta_info_text:
                start_date, end_date = parse_date_text(meta_info_text)
                var['start_date'].append(start_date)
                var['end_date'].append(end_date)
            elif '문의전화' in meta_info_text:
                var['contact'].append(meta_info_text.replace('문의전화', '').strip())
            elif '주최' in meta_info_text:
                var['uploader'].append(meta_info_text.replace('주최/', '').replace('기관/', '').strip())
    result = merge_var_to_dict(key_list, var)
    return result

def parse_date_text(text):
    text_split = text.replace('기간', '').split(' ~ ')
    if len(text_split) == 2 :
        result = [convert_datetime_string_to_isoformat_datetime(_.strip()) for _ in text_split]
        return result[0], result[1] 
    else:
        return None, None

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'view_count', 'post_text_type'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_text_type'] = 'both'
    basic = extract_children_tag(soup, 'dd', child_tag_attrs={'class':'basic'})
    basic_list = extract_children_tag(basic, 'li', is_child_multiple=True)
    for li in basic_list:
        li_text = extract_text(li)
        if '조회수' in li_text:
            var['view_count'] = extract_numbers_in_text(li_text)
            break
    extra_info = {'info_title': '기타정보'}
    etc = extract_children_tag(soup, 'dd', child_tag_attrs={'class':'etc'})
    etc_list = extract_children_tag(etc, 'li', is_child_multiple=True)
    for li in etc_list:
        li_name = extract_text_from_single_tag(li, 'span', child_tag_attrs={'class':'name'})
        li_text = extract_text(li).replace(li_name, '').strip()
        extra_info.update({f'info_{len(extra_info)}' : (li_name, li_text)})
    var['extra_info'].append(extra_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'contents'})
    var['post_text'] = extract_text(tmp_contents)
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


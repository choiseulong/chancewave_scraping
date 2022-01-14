from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'view_count', 'post_thumbnail']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    table = extract_children_tag(soup, 'table', child_tag_attrs={'class' : 'bo_basic_list'})
    tr_list =extract_children_tag(table, 'tr', is_child_multiple=True)
    for tr in tr_list:
        td_datetime = extract_children_tag(tr, 'td', child_tag_attrs={'class':'td_datetime'})
        date_text_list = [
            extract_text(div) 
            for div 
            in extract_children_tag(td_datetime, 'div', is_child_multiple=True)
        ]
        date_text = date_text_list[1] + '.' + date_text_list[0]
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(date_text)
        )
        post_thumbnail = search_img_list_in_contents(tr, var['channel_main_url'])
        if post_thumbnail :
            var['post_thumbnail'].append(post_thumbnail[0])
        else:
            var['post_thumbnail'].append(None)
        li_list = extract_children_tag(tr, 'li', is_child_multiple=True)
        for li in li_list:
            li_text = extract_text(li)
            if '조회수' in li_text:
                var['view_count'].append(
                    extract_numbers_in_text(li_text)
                )
        var['post_title'].append(
            extract_text_from_single_tag(tr, 'div', child_tag_attrs={'class': 'subject'})
        )

        btn_div = extract_children_tag(tr, 'div', child_tag_attrs={'class' :'td_list_wr'})
        onclick = extract_attrs(btn_div, 'onclick')
        post_id_list = parse_post_id(onclick, [0,1])
        var['post_url'].append(
            var['post_url_frame'].format(post_id_list[0], post_id_list[1])
        )
    
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'view_content'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    return result


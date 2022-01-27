from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['is_going_on', 'post_url', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-27
    var['table_header'] = ["번호", "강좌명/교육기관", "상태", "접수기간", "교육기간", "교육대상", "신청/정원", "수강료"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_image_url', 'post_subject'],
        'multiple_type' : ['extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_text_type'] = 'only_extra_info'
    view_img = extract_children_tag(soup, 'div', child_tag_attrs={'class':'view_img'})
    img = extract_children_tag(view_img, 'img')
    src = extract_attrs(img, 'src')
    var['post_image_url'] = var['channel_main_url'] + src

    extra_info = []
    tmp_meta_data_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'mt80'}, is_child_multiple=True)
    for meta_data_box in tmp_meta_data_box:
        extra_info_con = {}
        info_title = extract_text_from_single_tag(meta_data_box, 'h4')
        extra_info_con.update({'info_title':info_title})
        meta_data_list = extract_children_tag(meta_data_box, 'tr', is_child_multiple=True)
        for meta_data in meta_data_list:
            meta_data_title = extract_text_from_single_tag(meta_data, 'th')
            meta_data_value = extract_text_from_single_tag(meta_data, 'td')
            extra_info_con.update({f'info_{len(extra_info_con)}' : (meta_data_title, meta_data_value)})

            if meta_data_title == '교육기간':
                meta_data_value_split = meta_data_value.split(' ~ ')
                var['start_date'] = meta_data_value_split[0] if len(meta_data_value_split) == 2 else None
                var['end_date'] = meta_data_value_split[1] if len(meta_data_value_split) == 2 else None
            elif meta_data_title == '강좌분류':
                var['post_subject'] = meta_data_value
            elif meta_data_title == '교육문의':
                var['contact'] = meta_data_value
        extra_info.append(extra_info_con)
    var['extra_info'] = extra_info
    result = convert_merged_list_to_dict(key_list, var)
    return result


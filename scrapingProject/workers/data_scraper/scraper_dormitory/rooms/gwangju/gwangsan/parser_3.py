from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['is_going_on', 'post_url', 'post_title', 'uploader', 'post_subject', 'post_content_target']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    cont_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    for cont in cont_list:
        td_list = extract_children_tag(cont, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            if td_idx == 0:
                is_going_on = extract_text_from_single_tag(td, 'span', child_tag_attrs={'class':True})
                print(is_going_on)
                if '마감' in is_going_on or '교육완료' in is_going_on:
                    var['is_going_on'].append(False)
                elif '접수중' in is_going_on or '교육중' in is_going_on:
                    var['is_going_on'].append(True)
                else :
                    var['is_going_on'].append('ERROR')
                lec_info = extract_children_tag(td, 'li', is_child_multiple=True)
                for info_idx, info in enumerate(lec_info):
                    info_text = extract_text(info)
                    if info_idx == 0:
                        var['post_subject'].append(info_text)
                    elif info_idx == 1:
                        a_tag = extract_children_tag(info, 'a')
                        href = extract_attrs(a_tag, 'href')
                        var['post_url'].append(
                            var['post_url_frame']+href
                        )
                        var['post_title'].append(info_text)
                    elif info_idx == 2:
                        var['uploader'].append(info_text)
            elif td_idx == 3:
                var['post_content_target'].append(
                    extract_text(td)
                )

    result = merge_var_to_dict(key_list, var)
    # 2021-02-11
    # var['table_header'] = ['강좌명/교육기관', '접수기간', '교육기간', '교육대상', '신청/정원', '수강료']
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_image_url'],
        'multiple_type' : ['extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
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
            elif meta_data_title == '교육문의':
                var['contact'] = meta_data_value
        extra_info.append(extra_info_con)
    var['extra_info'].append(extra_info)
    result = convert_merged_list_to_dict(key_list, var)
    return result


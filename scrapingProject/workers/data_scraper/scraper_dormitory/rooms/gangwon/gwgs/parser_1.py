from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_content_target', 'post_url', 'post_title', 'start_date', 'end_date', \
            'is_going_on', 'start_date2', 'end_date2']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    cont_box = extract_children_tag(soup, 'tbody')
    cont_list = extract_children_tag(cont_box, 'tr', is_child_multiple=True)
    if type(cont_list) == type(None):
        return
    for cont in cont_list:
        td_list = extract_children_tag(cont, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 0:
                var['post_title'].append(td_text)
                a_tag = extract_children_tag(td, 'a')
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
            elif td_idx == 1:
                var['post_content_target'].append(
                    td_text
                )
            elif td_idx == 2:
                start_date, end_date = parse_date_text(td_text)
                var['start_date'].append(start_date)
                var['end_date'].append(end_date)
            elif td_idx == 3:
                start_date2, end_date2 = parse_date_text_other(td_text)
                var['start_date2'].append(start_date2)
                var['end_date2'].append(end_date2)
            elif td_idx == 6:
                if td_text in ['대기등록', '모집중']:
                    var['is_going_on'].append(True)
                else :
                    var['is_going_on'].append(False)
    # 2021-02-09 
    # var['table_header'] = ["강좌명/강사명", "대상", "접수기간", "교육기간", "신청인원/모집인원", "시간", "상태"]
    result = merge_var_to_dict(var=var, key_list=key_list)
    return result

def parse_date_text(text):
    start_date = convert_datetime_string_to_isoformat_datetime(text[:16])
    end_date = convert_datetime_string_to_isoformat_datetime(text[17:])
    return start_date, end_date

def parse_date_text_other(text):
    start_date2 = convert_datetime_string_to_isoformat_datetime(text[:10])
    end_date2 = convert_datetime_string_to_isoformat_datetime(text[10:])
    return start_date2, end_date2
    
def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'uploader'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_meta_data = extract_children_tag(soup, 'div', child_tag_attrs={'class':'caption-info'})
    meta_data_list = extract_children_tag(tmp_meta_data, 'div', child_tag_attrs={'class':'li'}, is_child_multiple=True)
    extra_info = {'info_title' : '교육정보'}
    for meta_data in meta_data_list:
        meta_data_name = extract_text_from_single_tag(meta_data, 'b')
        meta_data_value = extract_text(meta_data).replace(meta_data_name, '').strip()
        extra_info.update({f'info_{len(extra_info)}' : (meta_data_name, meta_data_value)})

    tmp_meta_data = extract_children_tag(soup, 'div', child_tag_attrs={'class':'forward-article'})
    meta_data_list = extract_children_tag(tmp_meta_data, 'div', child_tag_attrs={'class':'item'}, is_child_multiple=True)
    for meta_data in meta_data_list:
        meta_data_name = extract_text_from_single_tag(meta_data, 'strong')
        meta_data_value = extract_text_from_single_tag(meta_data, 'em')
        extra_info.update({f'info_{len(extra_info)}' : (meta_data_name, meta_data_value)})

    tmp_meta_data = extract_children_tag(soup, 'div', child_tag_attrs={'class':'content-info__charge'})
    if type(tmp_meta_data) != type(None):
        meta_data_list = extract_children_tag(tmp_meta_data, 'span', is_child_multiple=True)
        for meda_data in meta_data_list:
            meta_data_text = extract_text(meda_data)
            if '연락처' in meta_data_text :
                var['contact'] = meta_data_text.replace('연락처 : ', '')
            elif '담당부서' in meta_data_text:
                var['uploader'] = meta_data_text.replace('담당부서 : ', '')
    
    panel = extract_children_tag(soup, 'div', child_tag_attrs={'class':'panel'}, is_child_multiple=True)
    cont_list = extract_children_tag(panel[1], 'div', is_child_multiple=True)
    cont_header_list = extract_children_tag(panel[1], 'h2', is_child_multiple=True)
    for cont_idx, cont in enumerate(cont_list):
        cont_header = extract_text(cont_header_list[cont_idx])
        cont_value = extract_text(cont)
        if '강좌소개' in cont_header:
            tmp_contents = cont
            var['post_text'] = cont_value
            if not var['contact']:
                var['contact'] = extract_contact_numbers_from_text(cont_value) 
            var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
        extra_info.update({f'info_{len(extra_info)}' : (cont_header, cont_value)})
    var['extra_info'].append(extra_info)
    result = convert_merged_list_to_dict(key_list, var)
    print(result)
    return result


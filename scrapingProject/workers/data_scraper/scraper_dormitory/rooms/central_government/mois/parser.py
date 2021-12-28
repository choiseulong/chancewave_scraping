from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploader', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', DataStatus.empty_attrs, DataStatus.not_multiple)
    tr_list = extract_children_tag(tbody, 'tr', DataStatus.empty_attrs, DataStatus.multiple)
    for tr in tr_list:
        td_list = extract_children_tag(tr, 'td', DataStatus.empty_attrs, DataStatus.multiple)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1:
                a_tag = extract_children_tag(td, 'a', DataStatus.empty_attrs, DataStatus.not_multiple)
                onclick = extract_attrs(a_tag, 'onclick')
                nttId, bbsId = parse_onclick(onclick)
                var['post_url'].append(
                    var['post_url_frame'].format(bbsId, nttId)
                )
                var['post_title'].append(td_text)
            elif td_idx == 3 :
                var['uploader'].append(td_text)
            elif td_idx == 4 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        td_text[:-1]
                    )
                )
            elif td_idx == 5 :
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )

    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    # print(result)
    return result

def parse_onclick(text):
    data = re.findall("'(.+?)'", text)
    nttId, bbsId = data[0], data[1]
    return nttId, bbsId

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    table_info = extract_children_tag(soup, 'div' , {'class' : 'table_info'}, DataStatus.not_multiple)
    var['contact'] = extract_contact_numbers_from_text(extract_text(table_info))
    desc = extract_children_tag(soup, 'div', {'class' : 'desc'}, DataStatus.not_multiple)
    var['post_text'] = clean_text(extract_text(desc))
    var['post_image_url'] = search_img_list_in_contents(desc, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    # print(result)
    return result
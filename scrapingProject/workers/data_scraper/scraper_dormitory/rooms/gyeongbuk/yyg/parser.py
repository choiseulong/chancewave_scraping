from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'view_count', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', DataStatus.empty_attrs, DataStatus.not_multiple)
    tr_list = extract_children_tag(tbody, 'tr', DataStatus.empty_attrs, DataStatus.multiple)
    for tr in tr_list :
        td_list = extract_children_tag(tr, 'td', DataStatus.empty_attrs, DataStatus.multiple)
        uploader = ''
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            # if '공지' in td_text and td_idx == 0:
            #     if var['page_count'] == 1 :
            #         pass
            #     else :
            #         continue
            if td_idx == 1 :
                a_tag = extract_children_tag(td, 'a', DataStatus.empty_attrs, DataStatus.not_multiple)
                href = extract_attrs(a_tag, 'href')
                # print(href)
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
            elif td_idx in [2] :
                uploader += td_text + ' '
            elif td_idx == 4:
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
        var['uploader'].append(uploader)
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    # print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title', 'uploaded_time'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    news_tit = extract_children_tag(soup, 'div', {'class' : 'news_tit'}, DataStatus.not_multiple)
    var['post_title'] = extract_text(
        extract_children_tag(news_tit, 'h3', DataStatus.empty_attrs, DataStatus.not_multiple)
    )
    dtList = extract_children_tag(news_tit, 'dt', DataStatus.empty_attrs, DataStatus.multiple)
    for dt in dtList:
        dtText = extract_text(dt)
        if '작성일' in dtText:
            var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    find_next_tag(dt)
                )
            )
            break
    cont = extract_children_tag(soup, 'div', {'class' : 'board_cont'}, DataStatus.not_multiple)
    var['post_text'] = extract_text(cont)
    var['contact'] = extract_contact_numbers_from_text(extract_text(cont))
    var['post_image_url'] = search_img_list_in_contents(cont, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    print(result)
    return result



from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'uploaded_time', 'view_count', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    bbs_list = extract_children_tag(soup, 'ul', {'class' : 'bbs_list'}, DataStatus.not_multiple)
    liList = extract_children_tag(bbs_list, 'li', DataStatus.empty_attrs, DataStatus.multiple)
    for li in liList :
        a_tag = extract_children_tag(li, 'a', DataStatus.empty_attrs, DataStatus.not_multiple)
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        infoText = extract_text_from_single_tag(li, 'em', DataStatus.empty_attrs)
        infoList = infoText.split('|')
        uploader = ''
        for infoIdx, info in enumerate(infoList):
            if infoIdx == 0 :
                uploader += info.split(' : ')[1] + ' '
            elif infoIdx == 1 :
                uploader += info
            elif infoIdx == 2:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        info.split(' : ')[1]
                    )
                )
            elif infoIdx == 3 :
                var['view_count'].append(
                    extract_numbers_in_text(info)
                )
        var['uploader'].append(uploader)

    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    # print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbdoy = extract_children_tag(soup, 'tbody', DataStatus.empty_attrs, DataStatus.not_multiple)
    thList = extract_children_tag(tbdoy, 'th', DataStatus.empty_attrs, DataStatus.multiple)
    for th in thList:
        thText = extract_text(th)
        if '전화번호' in thText:
            var['contact'] = extract_text(find_next_tag(th))
        elif '제목' in thText:
            var['post_title'] = extract_text(find_next_tag(th))
    cont = extract_children_tag(soup, 'td', {'class' : 'bbs_content'}, DataStatus.not_multiple)
    var['post_text'] = extract_text(cont)
    var['post_image_url'] = search_img_list_in_contents(cont, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    # print(result)
    return result



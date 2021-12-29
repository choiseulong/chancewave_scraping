from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    print
    tr_list = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    for tr in tr_list:
        viewBox = extract_children_tag(tr, 'div', {'class' : 'viewbox'}, is_child_multiple=False)
        var['post_title'].append(extract_text(viewBox))
        params = parse_onclick_params(
            extract_attrs(
                extract_children_tag(viewBox, 'a', child_tag_attrs={}, is_child_multiple=False),
                'onclick'
            )
        )
        var['post_url'].append(
            var['post_url_frame'].format(params)
        )
        td_list = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 4 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        td_text.strip()
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

def parse_onclick_params(text):
    return re.findall("'(.+?)'", text)[0]


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text', 'uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    table = extract_children_tag(soup, 'table', {'class' : 'board_view'}, is_child_multiple=False)
    title_sp = extract_children_tag(table, 'div', {'class' : 'title_sp'}, is_child_multiple=False)
    spanList = extract_children_tag(title_sp, 'span', child_tag_attrs={}, is_child_multiple=True)
    for span in spanList:
        spanText = extract_text(span)
        if '작성자' in spanText or '담당부서' in spanText:
            # spanText = spanText.split(': ')[1]
            var['uploader'] += spanText + ' '
        elif '전화번호' in spanText:
            var['contact'] = extract_contact_numbers_from_text(spanText)
    pList = extract_children_tag(table, 'p', child_tag_attrs={}, is_child_multiple=True)
    for p in pList:
        pText = extract_text(p)
        if pText:
            var['post_text'] += pText + ' '


    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result
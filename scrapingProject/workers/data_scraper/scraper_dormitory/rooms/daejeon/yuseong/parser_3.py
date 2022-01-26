from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploader', 'post_subject', 'post_content_target', \
            'contact', 'extra_info', 'post_text_type']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    thead = extract_children_tag(soup, 'thead')
    header_list = [extract_text(_) for _ in extract_children_tag(thead, 'th', is_child_multiple=True)]
    tbody = extract_children_tag(soup, 'tbody')
    tr_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    if not tr_list and type(tr_list) != type(None):
        return
    elif type(tr_list) == type(None) :
        raise f'{var["channel_code"]} CONTENTS LIST ERROR'
    # 2021-01-26 HEADER ["번호", "분류", "강좌명", "요일", "시간", "모집인원",\
    # "모집대상","기관","문의처","바로가기"]
    for tr in tr_list:
        extra_info = {'info_title': '강좌정보'}
        td_list = extract_children_tag(tr, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1:
                var['post_subject'].append(td_text)
            elif td_idx == 2:
                var['post_title'].append(td_text)
            elif td_idx == 6:
                var['post_content_target'].append(td_text)
            elif td_idx == 7:
                var['uploader'].append(td_text)
            elif td_idx == 8:
                var['contact'].append(td_text)
            elif td_idx == 9:
                a_tag = extract_children_tag(td, 'a')
                href = extract_attrs(a_tag, 'href')
                print(href)
                var['post_url'].append(href)
            extra_info.update({f'info_{len(extra_info)}' : (header_list[td_idx], td_text)})
        var['extra_info'].append(extra_info)
        var['post_text_type'].append('both')
    result = merge_var_to_dict(var=var, key_list=key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text','uploaded_time'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(
        extract_text_from_single_tag(soup, 'span', child_tag_attrs={'date'}).replace('등록일', '')
    )
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'bbs--view--cont'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['post_text']:
        iframe = extract_children_tag(soup, 'iframe', child_tag_attrs={'id':'pdf'})
        if iframe :
            src = extract_attrs(iframe, 'src')
            var['post_text'] = var['channel_main_url'] + src
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


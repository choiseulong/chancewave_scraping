from pickle import NONE
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'post_thumbnail', 'post_content_target', 'start_date2', 'end_date2']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    li_co_list = extract_children_tag(soup, 'div', child_tag_attrs={'class':'li_co'}, is_child_multiple=True)
    for li in li_co_list:
        li_poster = extract_children_tag(li, 'div', child_tag_attrs={'class':'li_poster'})
        post_thumbnail = extract_children_tag(li_poster, 'img')
        src = extract_attrs(post_thumbnail, 'src')
        var['post_thumbnail'].append(src)
        li_info = extract_children_tag(li, 'div', child_tag_attrs={'class':'li_info'})
        var['post_title'].append(extract_text_from_single_tag(li_info, 'h4'))

        li_list = extract_children_tag(li_info, 'li', is_child_multiple=True)
        for li_idx, li_con in enumerate(li_list):
            li_text = extract_text(li_con)
            if li_idx == 0 :
                li_text = li_text.replace('행사기간', '')
                li_text_split = li_text.split(' ~ ')
                var['start_date2'].append(
                    convert_datetime_string_to_isoformat_datetime(li_text_split[0].strip())
                )
                var['end_date2'].append(
                    convert_datetime_string_to_isoformat_datetime(li_text_split[1].strip())
                )
            elif li_idx == 3:
                var['post_content_target'].append(li_text)
        a_tag = extract_children_tag(li, 'a')
        onclick = extract_attrs(a_tag, 'onclick')
        post_id = parse_post_id(onclick, 0)
        var['post_url'].append(
            var['post_url_frame'].format(post_id)
        )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_text_type'] = 'both'
    tmp_info = extract_children_tag(soup, 'table')
    info_list = extract_children_tag(tmp_info, 'tr', is_child_multiple=True)
    extra_info = {'info_title':'공연/행사 정보'}
    for info in info_list:
        info_name = extract_text_from_single_tag(info, 'th')
        info_con = extract_text_from_single_tag(info, 'td')
        extra_info.update({f'info_{len(extra_info)}' : (info_name, info_con)})
    var['extra_info'] = extra_info
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'id':'bbs_cn'})
    var['post_text'] = extract_text(tmp_contents)
    inquire_no = extract_children_tag(soup, 'p', child_tag_attrs={'class':'inquire_no'})
    var['contact'] = extract_text(inquire_no)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])

    per_imgwrap = extract_children_tag(soup, 'div', child_tag_attrs={'class':'per_imgwrap'})
    img = extract_children_tag(per_imgwrap, 'img')
    src = extract_attrs(img, 'src')
    if type(var['post_image_url']) != list :
        var['post_image_url'] = [src]
    else:
        var['post_image_url'].append(src)
    result = convert_merged_list_to_dict(key_list, var)
    return result


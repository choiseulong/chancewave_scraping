from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['is_going_on', 'post_title', 'post_url', 'post_thumbnail', 'uploader', 'start_date', 'end_date', 'post_subject']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    dataList = extract_children_tag(soup, 'div', {"class" : "multi_cont"}, is_child_multiple=False) # tag
    competitionList = extract_children_tag(dataList, 'a', {"class" : "goCompetitionDetail"}, is_child_multiple=True) # list
    for data in competitionList :
        status = extract_text(extract_children_tag(data, 'span', {"class" : "flag_md"}))
        if status == '진행중': 
            var['is_going_on'].append(True)
        else :
            var['is_going_on'].append(False)

        var['post_url'].append(
            var['channel_main_url'] + \
            extract_attrs(
                data, 'href'
            )
        )
        var['post_thumbnail'].append(
            var['channel_main_url'] + \
            extract_attrs(
                extract_children_tag(data, 'img'),
                'src'
            )
        )
        var['post_title'].append(
            extract_text(
                extract_children_tag(data, 'p', {"class" : "tit"})
            )
        )
        var['uploader'].append(
            extract_text(
                extract_children_tag(data, 'p', {"class" : "user"})
            )
        )
        var['post_subject'].append(
            extract_text(
                extract_children_tag(data, 'p', {"class" : "type"})
            ) + ' & ' + \
            extract_text(
                extract_children_tag(data, 'span', {"class" : "flag_md"})
            )   
        )
        start_date, end_date = parsing_date(
            extract_text(
                extract_children_tag(data, 'p', {"class" : "date"})
            )
        )
        var['start_date'].append(
            convert_datetime_string_to_isoformat_datetime(start_date)
        )
        var['end_date'].append(
            convert_datetime_string_to_isoformat_datetime(end_date)
        )

    
    result = merge_var_to_dict(key_list, var)
    return result

def parsing_date(text): 
    result = [k.strip()[:-1] for k in text.split('~')]
    return result[0], result[1]

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['view_count', 'linked_post_url', 'contact', 'post_content_target', 'post_text'],
        'multiple_type' : ['post_image_url']
    } 
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    table = extract_children_tag(soup, 'tbody', child_tag_attrs={}) # return default -> tag
    tr_list = extract_children_tag(table, 'tr', child_tag_attrs={}, is_child_multiple=True) # list
    for tr in tr_list :
        th = extract_children_tag(tr, 'th', child_tag_attrs={}, is_child_multiple=True) # list
        td = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True) # list
        th_text = extract_text(th, is_child_multiple=True)
        td_text = extract_text(td, is_child_multiple=True)

        info = {'조회수' : 'view_count', '문의':'contact', '홈페이지':'linked_post_url', '응모대상' : 'post_content_target'}
        for key in info :
            if key in th_text:
                th_idx = th_text.index(key)
                if key == '조회수':
                    var[info[key]] = extract_numbers_in_text(td_text[th_idx])
                    continue
                var[info[key]] = td_text[th_idx]

    detail_content = extract_children_tag(soup, 'div', {'class' : 'detail'}) # return default -> tag
    detail_img = extract_children_tag(detail_content, 'img', child_tag_attrs={}, is_child_multiple=True)
    if detail_img :
        for img in detail_img :
            var['post_image_url'].append(
                var['channel_main_url'] + extract_attrs(img, 'src')
            )
    detail_text = extract_children_tag(detail_content, 'div', {"class" : "text"})
    var['post_text'] = clean_text(
        extract_text(detail_text)
    )
    
    result = convert_merged_list_to_dict(key_list, var)
    return result

from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info= {
        'multiple_type' : ['uploaded_time', 'post_url', 'view_count']
    }
    var, soup, key_list, _= html_type_default_setting(params, target_key_info)
    tbody= extract_children_tag(soup, 'tbody')
    tr_list= extract_children_tag(tbody, 'tr', is_child_multiple=True)
    for tr in tr_list:
        # 2021-01-12 header= ["번호", "제목", "등록일", "첨부파일", "조회수"]
        td_list= extract_children_tag(tr, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text= extract_text(td)
            if td_idx == 1:
                a_tag= extract_children_tag(tr, 'a')
                href= extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['channel_main_url']+ href
                )
            elif td_idx == 2:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 4:
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info= {
        'single_type' : ['post_text', 'contact', 'uploader', 'post_title'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _= html_type_default_setting(params, target_key_info)
    th_list= extract_children_tag(soup, 'th', is_child_multiple=True, child_tag_attrs={'scope' : 'row'})
    uploader = ''
    for th in th_list:
        th_text= extract_text(th)
        if '담당' in th_text:
            uploader += extract_text(find_next_tag(th)) + ' '
        elif '제목' in th_text:
            var['post_title']= extract_text(find_next_tag(th))
    var['uploader'] = uploader
    tmp_contents= extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'original'})
    var['post_text']= extract_text(tmp_contents)
    var['contact']= extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url']= search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result= convert_merged_list_to_dict(key_list, var)
    return result


from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'uploader', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-18 
    var['post_id_idx'] = [1,2,3]
    var['table_header'] = ["번호", "제목", "파일", "작성자", "작성일", "조회"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    bod_view = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'bod_view'})
    var['post_title'] = extract_text_from_single_tag(bod_view, 'h4')
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'view_cont'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

# def post_list_parsing_process(**params):
#     target_key_info = {
#         'multiple_type' : ['post_url', 'uploaded_time', 'post_title', 'view_count']
#     }
#     var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
#     tbody = extract_children_tag(soup, 'tbody')
#     tr_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
#     if not tr_list :
#         return
#     # 2022-01-05 header [번호, 제목, 작성일, 조회수]
#     # url : https://www.ulju.ulsan.kr/ulju/ulju_news01?curPage={}
#     # 2022-01-21 header [번호, 제목, 파일, 작성자, 작성일, 조회]
#     # url : 
#     for tr in tr_list :
#         td_list = extract_children_tag(tr, 'td', is_child_multiple=True)
#         td_text = ''
#         for td_idx, td in enumerate(td_list):
#             td_text = extract_text(td).strip()
#             if not td_text and td_idx == 0:
#                 if var['page_count'] != 1 :
#                     break
#             if td_idx == 1:
#                 a_tag = extract_children_tag(td, 'a')
#                 href = extract_attrs(a_tag, 'href')
#                 var['post_url'].append(
#                     var['channel_main_url'] + href
#                 )
#                 var['post_title'].append(td_text)
#             elif td_idx == 3 :
#                 var['view_count'].append(
#                     extract_numbers_in_text(td_text)
#                 )
#             elif td_idx == 2:
#                 var['uploaded_time'].append(
#                     convert_datetime_string_to_isoformat_datetime(td_text)
#                 )
    
#     result = merge_var_to_dict(key_list, var)
#     return result

# def post_content_parsing_process(**params):
#     target_key_info = {
#         'single_type' : ['post_text', 'contact', 'uploader'],
#         'multiple_type' : ['post_image_url']
#     }
#     var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
#     th_list = extract_children_tag(soup, 'th', child_tag_attrs={'scope' : 'row'}, is_child_multiple=True)
#     uploader = ''
#     for th in th_list:
#         th_text = extract_text(th)
#         if th_text in ['담당부서', '작성자']:
#             uploader += extract_text(find_next_tag(th)) + ' '
#         elif '전화번호' in th_text:
#             var['contact'] = extract_text(find_next_tag(th))
#     var['uploader'] = uploader
#     tbody = extract_children_tag(soup, 'tbody')
#     tmp_contents = extract_children_tag(tbody, 'td', child_tag_attrs={'class' : 'content'})
#     decomposed_tmp_contents = decompose_tag(tmp_contents, 'div', child_tag_attrs={'class' : 'content-footer'})
#     var['post_text'] = extract_text(decomposed_tmp_contents)
#     var['post_image_url'] = search_img_list_in_contents(decomposed_tmp_contents, var['channel_main_url'])
#     if not var['contact']:
#         var['contact'] = extract_contact_numbers_from_text(extract_text(decomposed_tmp_contents))
#     result = convert_merged_list_to_dict(key_list, var)
#     return result


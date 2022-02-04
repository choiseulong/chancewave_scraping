from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'post_thumbnail']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    cont_body = extract_children_tag(soup, 'div', child_tag_attrs={'class':'cont_body'})
    post_list = extract_children_tag(cont_body, 'li', is_child_multiple=True)
    print(post_list[1])
    for post in post_list:
        
        var['post_title'].append(
            extract_text_from_single_tag(post, 'span', child_tag_attrs={'class':'tit'})
        )
        img = extract_children_tag(post, 'img')
        src = extract_attrs(img, 'src')
        var['post_thumbnail'].append(
            var['channel_main_url'] + src
        )
        a_tag = extract_children_tag(post, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            href
        )
    result = merge_var_to_dict(key_list, var)
    return result

# def post_content_parsing_process(**params):
#     target_key_info = {
#         'single_type' : ['post_text', 'contact', 'post_title'],
#         'multiple_type' : ['post_image_url']
#     }
#     var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
#     dt_list = extract_children_tag(soup, 'dt', is_child_multiple=True)
#     for dt in dt_list:
#         dt_text = extract_text(dt)
#         if '제목' in dt_text:
#             var['post_title'] = extract_text(find_next_tag(dt))
#             break
#     tmp_contents = extract_children_tag(soup, 'dl', child_tag_attrs={'class':'content'})
#     var['post_text'] = extract_text(tmp_contents).replace('글내용', '')
#     var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
#     var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
#     result = convert_merged_list_to_dict(key_list, var)
#     return result


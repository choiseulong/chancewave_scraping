from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : [
            'uploaded_time', 'post_url', 'post_thumbnail',
            'start_date', 'end_date', 'start_date2', 'end_date2'
        ]
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    course_list = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'course_list'})
    li_list = extract_children_tag(course_list, 'li', is_child_multiple=True)
    for li in li_list:
        div_list = extract_children_tag(li, 'div', is_child_multiple=True, is_recursive=False)
        print(len(div_list))
        # for div_idx, div in enumerate(div_list):
        #     if div_idx == 0:
        #         img = extract_children_tag(div, 'img')
        #         src = extract_attrs(img, 'src')
        #         var['post_thumbnail'].append(
        #             var['post_main_url'] + src
        #         )
        #     elif div_idx == 1 :
        #         var['post_title'].append(
        #             extract_text_from_single_tag(div, 'strong')
        #         )
        #         sub_con = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'sub_con'})
        #         li_list = extract_children_tag(sub_con, 'li', is_child_multiple=True)
        #         for li_idx, li in enumerate(li_list):
        #             li = decompose_tag(li, 'strong')
        #             li_text = extract_text(li)
        #             if li_idx == 0 :
        #                 if li_text :
        #                     li_text_split = li_text.split('~')
        #                     var['start_date'].append(
        #                         convert_datetime_string_to_isoformat_datetime(li_text_split[0].strip())
        #                     )
        #                     var['end_date'].append(
        #                         convert_datetime_string_to_isoformat_datetime(li_text_split[1].strip())
        #                     )
        #                 else :
        #                     var['start_date'].append(None)
        #                     var['end_date'].append(None)
        #             elif li_idx == 1 :
        #                 if li_text :
        #                     li_text_split = li_text.split('~')
        #                     var['start_date2'].append(
        #                         convert_datetime_string_to_isoformat_datetime(li_text_split[0].strip())
        #                     )
        #                     var['end_date2'].append(
        #                         convert_datetime_string_to_isoformat_datetime(li_text_split[1].strip())
        #                     )
        #                 else :
        #                     var['start_date2'].append(None)
        #                     var['end_date2'].append(None)

    # 2021-01-22 
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'view_cont'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


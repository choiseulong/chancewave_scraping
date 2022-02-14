from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'view_count', 'post_thumbnail']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    board_gallery2 = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board_gallery2'})
    li_list = extract_children_tag(board_gallery2, 'li', is_child_multiple=True, child_tag_attrs={'class':False})
    for li in li_list:
        photo = extract_children_tag(li, 'div', child_tag_attrs={'class':'photo'})
        if photo:
            img = extract_children_tag(photo, 'img')
            src = extract_attrs(img, 'src')
            var['post_thumbnail'].append(
                var['channel_main_url'] + src
            )
        else :
            var['post_thumbnail'].append(
                ''
            )
        a_tag = extract_children_tag(li, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        var['post_title'].append(
            extract_text(a_tag)
        )
        p_tag = extract_children_tag(li, 'p', child_tag_attrs={'class':True})
        p_tag_text = extract_text(p_tag)
        p_tag_text_split = p_tag_text.split('/')
        var['view_count'].append(
            extract_numbers_in_text(
                p_tag_text_split[1]
            )
        )
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                parse_uploaded_time(
                    p_tag_text_split[0]
                )
            )
        )
    result = merge_var_to_dict(key_list, var)
    return result

def parse_uploaded_time(text):
    year = extract_numbers_in_text(text.split('년')[0])
    month = extract_numbers_in_text(text[text.find('년'):].split('월')[0])
    days = extract_numbers_in_text(text.split('월')[1])
    result = str(year)+'-'+str(month)+'-'+str(days)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact',],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'con'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result


from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'view_count', 'post_thumbnail']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    board_gallery2 = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board_gallery2'})
    li_box = extract_children_tag(board_gallery2, 'ul')
    li_list = extract_children_tag(li_box, 'li', is_child_multiple=True, child_tag_attrs={'class':False})
    for li in li_list :
        photo = extract_children_tag(li, 'div', child_tag_attrs={'class':'photo'})
        if photo:
            img = extract_children_tag(photo, 'img')
            src = extract_attrs(img, 'src')
            var['post_thumbnail'].append(
                var['channel_main_url'] + src
            )
        else :
            var['post_thumbnail'].append(
                None
            )
        a_tag = extract_children_tag(li, 'a')
        var['post_title'].append(
            extract_text(a_tag)
        )
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        p_tag = extract_children_tag(li, 'p', child_tag_attrs={'class':True})
        p_tag_text = extract_text(p_tag)
        p_tag_text_split = p_tag_text.split('|')
        var['view_count'].append(
            extract_numbers_in_text(p_tag_text_split[0])
        )
        var['uploaded_time'].append(
            parse_uploaded_time(p_tag_text_split[1])
        )
    result = merge_var_to_dict(var=var, key_list=key_list)
    return result

def parse_uploaded_time(text):
    year = text.split('년')[0]
    month = text[text.find('년'):].split('월')[0]
    days = text.split('월')[1]
    result = year+'-'+month+'-'+days
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


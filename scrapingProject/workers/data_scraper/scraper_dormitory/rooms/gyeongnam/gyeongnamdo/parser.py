from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import re

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'view_count', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    for tr in tr_list:
        td_list = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if '공지' in td_text:
                if var['page_count'] == 1 :
                    pass
                else :
                    break

            if td_idx == 1 : 
                var['post_title'].append(td_text)
                a_tag = extract_children_tag(td, 'a', child_tag_attrs={}, is_child_multiple=False)
                href = extract_attrs(a_tag, 'href')
                postId = parse_href(href)
                var['post_url'].append(
                    var['post_url_frame'].format(postId)
                )
            elif td_idx == 3 :
                var['uploader'].append(td_text)
            elif td_idx == 4 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 5 :
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )

    
    result = merge_var_to_dict(key_list, var)
    
    return result

def parse_href(text):
    return text[text.find('&dataSid=') + len('&dataSid='):]




def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    titleField = extract_children_tag(soup, 'div', {'class' : 'titleField'}, is_child_multiple=False)
    strongList = extract_children_tag(titleField, 'strong', child_tag_attrs={}, is_child_multiple=True)
    for strong in strongList:
        strongText = extract_text(strong)
        if '연락처' in strongText:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(find_next_tag(strong))
            )
            break
    
    conText = extract_children_tag(soup, 'div', {'class' : 'conText'}, is_child_multiple=False)
    var['post_text'] = clean_text(extract_text(conText))
    var['post_image_url'] = search_img_list_in_contents(conText, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    
    return result


def postListParsingProcess_1(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'post_image_url', 'post_text_type'],
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    photoList = extract_children_tag(soup, 'div', {'class' : 'photoList'}, is_child_multiple=False)
    aTagList = extract_children_tag(photoList, 'a', child_tag_attrs={}, is_child_multiple=True)
    for a_tag in aTagList:
        href = extract_attrs(a_tag, 'href')
        img = extract_children_tag(a_tag, 'img', {'src' : True}, is_child_multiple=False)
        src = extract_attrs(img, 'src')
        var['post_image_url'].append(
            var['channel_main_url'] + src
        )
        var['post_title'].append(
            extract_attrs(img, 'alt')
        )
        var['post_url'].append(href)
        var['post_text_type'].append(None)
    
    result = merge_var_to_dict(key_list, var)
    
    return result



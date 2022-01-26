from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'post_thumbnail', 'post_text']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    popupzone = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'popupzone'})
    li_list = extract_children_tag(popupzone, 'li', is_child_multiple=True)
    for li in li_list:
        a_tag = extract_children_tag(li, 'a')
        img = extract_children_tag(li, 'img')
        alt = extract_attrs(img, 'alt')
        src = extract_attrs(img, 'src')
        if a_tag :
            href = extract_attrs(a_tag, 'href')
            var['post_url'].append(
                var['channel_main_url'] + href
            )
            var['post_title'].append(alt)
            var['post_text'].append(None)
        else :
            var['post_url'].append(None)
            var['post_title'].append(None)
            var['post_text'].append(alt)
        var['post_thumbnail'].append(
            var['channel_main_url'] + src
        )
    result = merge_var_to_dict(key_list, var)
    return result

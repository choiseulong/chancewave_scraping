from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['start_date', 'post_title', 'post_thumbnail', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    cont_list = extract_children_tag(soup, 'li', child_tag_attrs={'class':'cont'}, is_child_multiple=True)
    if type(None) == type(cont_list):
        return
    for cont in cont_list :
        img = extract_children_tag(cont, 'img')
        src = extract_attrs(img, 'src')
        var['post_thumbnail'].append(
            var['channel_main_url'] + src
        )
        bundle_cont = extract_children_tag(cont, 'ul', child_tag_attrs={'class' : 'bundle_cont'})
        tmp_meta_data = extract_children_tag(bundle_cont, 'li', is_child_multiple=True)
        extra_info = {'info_title':'행사상세'}
        for meta_data_idx, meta_data in enumerate(tmp_meta_data) :
            meta_data_name = '행사명'
            if meta_data_idx != 0:
                meta_data_name = extract_text_from_single_tag(meta_data, 'strong')
            meta_data_value = extract_text_from_single_tag(meta_data, 'span')
            extra_info.update({f'info_{len(extra_info)}' : (meta_data_name, meta_data_value)})
            if '일자' in meta_data_name:
                var['start_date'].append(convert_datetime_string_to_isoformat_datetime(meta_data_value))
            elif '행사명' in meta_data_name:
                var['post_title'].append(meta_data_value)
        var['extra_info'].append(extra_info)
    result = merge_var_to_dict(key_list, var)
    return result

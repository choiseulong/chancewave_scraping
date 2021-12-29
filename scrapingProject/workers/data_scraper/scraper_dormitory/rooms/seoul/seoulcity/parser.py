from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'uploaded_time', 'post_subject'],
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    item_div = extract_children_tag(soup, "div", {"class" : "item"}, is_child_multiple=True)
    var["post_url"] = [
        extract_attrs(
            extract_children_tag(div, 'a'),
            'href'
        ) \
        for div \
        in item_div
    ]
    em_date = extract_children_tag(soup, "em", {"class" : "date"}, is_child_multiple=True)
    var["uploaded_time"] = [
        convert_datetime_string_to_isoformat_datetime(extract_text(date)[:19])
        for date \
        in em_date
    ]
    checkedDateRange = [check_date_range_availability(var['date_range'], date) for date in var["uploaded_time"]]
    var['post_subject'] = [
        extract_text(
            extract_children_tag(div, 'i')
        )[1:-1]\
        for div \
        in item_div
    ]
    value_list = [
        [_ for idx, _ in enumerate(var[key]) if checkedDateRange[idx] == 'vaild'] \
        for key \
        in key_list
    ]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    return result
 
def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'uploader', 'post_title'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    div_viewTop = extract_children_tag(soup, "div", {"id" : "view_top"})
    var['post_title'] = extract_text(
        extract_children_tag(div_viewTop, 'h3', child_tag_attrs={})
    )
    div_postText = extract_children_tag(soup, "div", {"id" : "post_content"})
    pTagList = extract_children_tag(div_postText, 'p', {"class" : ['indent20', 'mt20']}, is_child_multiple=True)
    
    if not pTagList:
        pTagList = [p for p in extract_children_tag(div_postText, 'p', child_tag_attrs={}, is_child_multiple=True)]
    postTextList = [
        clean_text(
            extract_text(p)
        ) \
        for p \
        in pTagList
    ]
    var['post_text'] = ' '.join(postTextList) if postTextList else ''

    for ptag in pTagList:
        if 'class' in ptag.attrs:
            classAttrs = extract_attrs(ptag, 'class')
            if classAttrs in ['txt-1', 'txt-2', 'btn']:
                continue
        else :
            img = extract_children_tag(ptag, 'img', child_tag_attrs={}, is_child_multiple=True)
            if img :
                for i in img :
                    src = extract_attrs(i, 'src')
                    var['post_image_url'].append(
                        src 
                    )

    contact = extract_children_tag(soup, "dl", {"class" : "top-row row2"})
    uploader = extract_children_tag(extract_children_tag(soup, "dd", {"class" : "dept"}), 'span', child_tag_attrs={}, is_child_multiple=True)
    var['contact'] = extract_text(extract_children_tag(contact, 'dd')) if contact else None
    var['uploader'] = ' & '.join(
            [
                clean_text(extract_text(text)) \
                for text \
                in uploader
            ]
        ) \
        if uploader else None
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result

def search_total_post_count(result):
    postNumberIdx = result['post_title'].find(']')
    postNumber = extract_numbers_in_text(result['post_title'][:postNumberIdx])
    totalPageCount = divmod(int(postNumber), 10)[0] + 1
    return totalPageCount
    




    
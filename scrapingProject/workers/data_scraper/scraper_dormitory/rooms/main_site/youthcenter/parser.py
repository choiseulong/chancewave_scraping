from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    var = reflect_params(locals(), params)
    target_key_info = {
        'multiple_type' : ['is_going_on', 'post_subject', 'post_title', 'uploader', 'contents_req_params'],
        'single_type' : ['Cookie','_csrf']
    }
    var, soup, _, _ = html_type_default_setting(params, target_key_info)
    # var, _ = reflect_key(var, target_key_info)
    # soup = change_to_soup(
    #     var['response'].text
    # )

    postCountBox = extract_children_tag(soup, 'div', {'class' : ['sch-result-wrap compare-result-list']}, is_child_multiple=False)
    postCount = extract_numbers_in_text(
            extract_text(
            extract_children_tag(postCountBox, 'div', {'class' : 'l'}, is_child_multiple=False)
        )
    )
    if postCount < var['page_count'] * 12 :
        return 'endpoint'

    post_list_box = extract_children_tag(soup, "div", {"class" : "result-list-box"}, is_child_multiple=False)
    post_list = extract_children_tag(post_list_box, "li", child_tag_attrs={}, is_child_multiple=True)
    
    var['_csrf'] = extract_attrs(
        extract_children_tag(soup, "meta", {"name" : "_csrf"}, is_child_multiple=False),
        "content"
    )
    labelColorList = []
    for post in post_list:
        var['contents_req_params'].append(
            {
                "_csrf" : var['_csrf'],
                "bizId" : extract_attrs(
                    extract_children_tag(post, "input", {"name" : "cmprCheckbox"}),
                    "value"
                )
            }
        ) 
        var['post_title'].append(
            extract_text(
                extract_children_tag(post, "a"),
            )
        )
        var['post_subject'].append(
            extract_text(
                extract_children_tag(post, "span", {"class" : "srh-cate-data"}),
            ) 
        )
        badge = extract_children_tag(post, "div", {"class" : "badge"})
        var['uploader'].append(
            extract_text(badge)
        )
        badgeLabelColor = extract_attrs(
            extract_children_tag(badge, 'span'),
            'class'
        )
        if 'red-label' in badgeLabelColor:
            var['is_going_on'].append(True)
        else :
            var['is_going_on'].append(False)
            
    value_list = [
        [_ for idx, _ in enumerate(var[key])] \
       for key \
        in target_key_info['multiple_type']
    ]

    result = merge_var_to_dict(target_key_info['multiple_type'], value_list)
    var['Cookie'] = var['response'].cookies.get_dict()['YOUTHCENTERSESSIONID']
    result.append({'Cookie' : 'YOUTHCENTERSESSIONID=' + var['Cookie']})
    return result

def post_content_parsing_process(**params):
    var = reflect_params(locals(), params)
    target_key_info = {
        'multiple_type' : ['extra_info'],
        'single_type' : ['post_text_type']
    }
    var, key_list = reflect_key(var, target_key_info)
    soup = change_to_soup(
        var['response'].text
    )
    info_title = [
        extract_text(h5) \
        for h5 \
        in extract_children_tag(soup, 'h5', {"class" : "view_tit"}, is_child_multiple=True)
    ]
    infoTable = [table for table in extract_children_tag(soup, 'div', {"class" : "table_wrap"}, is_child_multiple=True)]
    for tableIdx, table in enumerate(infoTable) :
        var['extra_info'].append({'info_title' : info_title[tableIdx]}) 
        contentsTitle = [
            extract_text(_) \
            for _ \
            in extract_children_tag(table, 'div', {"class" : "list_tit"}, is_child_multiple=True)
        ]
        contents = [
            extract_text(_) \
            for _ \
            in extract_children_tag(table, 'div', {"class" : "list_cont"}, is_child_multiple=True)
        ]
        for title, cont in zip(contentsTitle, contents):
            infoNum = len(var['extra_info'][tableIdx])
            var['extra_info'][tableIdx].update({f'info_{infoNum}' : [title, cont]})
    var['post_text_type'] = 'only_extra_info'
    
    result = convert_merged_list_to_dict(key_list, var)
    return result
        
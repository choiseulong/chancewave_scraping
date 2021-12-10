from workers.dataScraper.scraperDormitory.parserTools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'uploadedTime', 'postSubject'],
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    item_div = extract_children_tag(soup, "div", {"class" : "item"}, childIsMultiple)
    var["postUrl"] = [
        extract_attrs(
            extract_children_tag(div, 'a'),
            'href'
        ) \
        for div \
        in item_div
    ]
    em_date = extract_children_tag(soup, "em", {"class" : "date"}, childIsMultiple)
    var["uploadedTime"] = [
        convert_datetime_string_to_isoformat_datetime(extract_text(date)[:19])
        for date \
        in em_date
    ]
    checkedDateRange = [check_date_range_availability(var['dateRange'], date) for date in var["uploadedTime"]]
    var['postSubject'] = [
        extract_text(
            extract_children_tag(div, 'i')
        )[1:-1]\
        for div \
        in item_div
    ]
    valueList = [
        [_ for idx, _ in enumerate(var[key]) if checkedDateRange[idx] == 'vaild'] \
        for key \
        in keyList
    ]
    result = merge_var_to_dict(keyList, valueList)
    return result
 
def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['postText', 'contact', 'uploader', 'postTitle'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    div_viewTop = extract_children_tag(soup, "div", {"id" : "view_top"})
    var['postTitle'] = extract_text(
        extract_children_tag(div_viewTop, 'h3', dummyAttrs)
    )
    div_postText = extract_children_tag(soup, "div", {"id" : "post_content"})
    pTagList = extract_children_tag(div_postText, 'p', {"class" : ['indent20', 'mt20']}, childIsMultiple)
    
    if not pTagList:
        pTagList = [p for p in extract_children_tag(div_postText, 'p', dummyAttrs, childIsMultiple)]
    postTextList = [
        clean_text(
            extract_text(p)
        ) \
        for p \
        in pTagList
    ]
    var['postText'] = ' '.join(postTextList) if postTextList else ''

    for ptag in pTagList:
        if 'class' in ptag.attrs:
            classAttrs = extract_attrs(ptag, 'class')
            if classAttrs in ['txt-1', 'txt-2', 'btn']:
                continue
        else :
            img = extract_children_tag(ptag, 'img', dummyAttrs, childIsMultiple)
            if img :
                for i in img :
                    src = extract_attrs(i, 'src')
                    var['postImageUrl'].append(
                        src 
                    )

    contact = extract_children_tag(soup, "dl", {"class" : "top-row row2"})
    uploader = extract_children_tag(extract_children_tag(soup, "dd", {"class" : "dept"}), 'span', dummyAttrs, childIsMultiple)
    var['contact'] = extract_text(extract_children_tag(contact, 'dd')) if contact else None
    var['uploader'] = ' & '.join(
            [
                clean_text(extract_text(text)) \
                for text \
                in uploader
            ]
        ) \
        if uploader else None
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result

def search_total_post_count(result):
    postNumberIdx = result['postTitle'].find(']')
    postNumber = extract_numbers_in_text(result['postTitle'][:postNumberIdx])
    totalPageCount = divmod(int(postNumber), 10)[0] + 1
    return totalPageCount
    




    
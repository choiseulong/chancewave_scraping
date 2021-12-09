from workers.dataScraper.scraperDormitory.parserTools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploadedTime', 'uploader', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)

    contents = extract_children_tag(soup, 'ul', {'class' : 'list_post'}, childIsNotMultiple)
    liList = extract_children_tag(contents, 'li', dummyAttrs, childIsMultiple)
    for li in liList :
        aTag = extract_children_tag(li, 'a', {'title' : True}, childIsNotMultiple)
        postId = extract_text_between_prefix_and_suffix(
            'boardSeq=',
            '&amp',
            extract_attrs(
                aTag,
                'href'
            )
        )
        var['postUrl'].append(
            var['postUrlFrame'].format(postId)
        )
        var['postTitle'].append(
            extract_text(aTag)
        )
        postInfoList = extract_children_tag(li, 'div', {'class' : 'post_info'}, childIsMultiple)
        for infoIdx, postInfo in enumerate(postInfoList):
            infoText = extract_text(postInfo).split(':')[-1].strip()
            if infoIdx == 0 :
                var['uploader'].append(infoText)
            elif infoIdx == 1 :
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(infoText)
                )
            elif infoIdx == 2 :
                var['viewCount'].append(
                    extract_numbers_in_text(infoText)
                )
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    # print(result)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, fullText = html_type_default_setting(params, targetKeyInfo)
    if type(soup) == str :
        # ERROR 예외 : [local variable 'match' referenced before assignment] 
        fullText = parse_fullText(fullText)
        post_content = change_to_soup(fullText)
        postText = clean_text(extract_text(post_content))
        var['postText'] = clean_text(postText)
        var['contact'] = extract_contact_numbers_from_text(postText)
    else :
        post_content = extract_children_tag(soup, 'div', {'class' : 'post_content'}, childIsNotMultiple)
        postText = extract_text(post_content)
        var['contact'] = extract_contact_numbers_from_text(postText)
        var['postText'] = clean_text(postText)
    imgList = extract_children_tag(post_content, 'img', {'src' : True}, childIsMultiple)
    if imgList:
        for img in imgList:
            src = extract_attrs(img, 'src')
            if 'http' not in src:
                src = var['channelMainUrl'] + src
            var['postImageUrl'].append(src)
    
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result

def parse_fullText(text):
    prefix = '<div class="post_content">'
    suffix = '<div class="hwp_editor_board_content"'
    return text[text.find(prefix) : text.find(suffix)] + '</div>'
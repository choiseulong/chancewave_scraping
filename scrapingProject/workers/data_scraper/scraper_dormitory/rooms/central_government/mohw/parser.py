from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    for tr in tr_list :
        td_list = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1:
                a_tag = extract_children_tag(td, 'a', child_tag_attrs={}, is_child_multiple=False)
                onclick = extract_attrs(a_tag, 'onclick')
                postId = extract_text_between_prefix_and_suffix("('", "')", onclick)
                var['post_url'].append(
                    var['post_url_frame'].format(postId)
                )
                var['post_title'].append(td_text)
            elif td_idx == 2 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 3 :
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )

    
    result = merge_var_to_dict(key_list, var)
    # print(result)
    return result

def parse_href(text):
    return text[text.find('&seq=') + len('&seq='):]

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text', 'uploader', 'start_date', 'end_date'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    bv_category = extract_children_tag(soup, 'div', {'class' : 'bv_category'}, is_child_multiple=False)
    spanList = extract_children_tag(bv_category, 'span', child_tag_attrs={}, is_child_multiple=True)
    uploader=''
    uploaderCount = 0 
    for spanIdx, span in enumerate(spanList):
        spanText = extract_text(span)
        nextSpanText =  extract_text(spanList[spanIdx+1])
        if '담당자' in spanText or '담당부서' in spanText : 
            uploader += nextSpanText + ' '
            uploaderCount += 1
        elif '전화번호' in spanText:
            var['contact'] = extract_contact_numbers_from_text(nextSpanText)
        elif '기간' in spanText:
            date = [i.strip() for i in nextSpanText.split('~') if i]
            if len(date) == 2 :
                date = [convert_datetime_string_to_isoformat_datetime(d) for d in date]
                var['start_date']= date[0]
                var['end_date'] = date[1]
            elif len(date) == 1 :
                var['start_date']= convert_datetime_string_to_isoformat_datetime(date[0])
            break
        if uploaderCount == 2:
            var['uploader'] = uploader     
    bv_content = extract_children_tag(soup, 'div', {'class' : 'bv_content'}, is_child_multiple=False)
    var['post_text'] = clean_text(extract_text(bv_content))
    var['post_image_url'] = search_img_list_in_contents(bv_content, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    # print(result)
    return result

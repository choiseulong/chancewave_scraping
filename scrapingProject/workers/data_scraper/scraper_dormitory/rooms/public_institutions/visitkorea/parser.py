from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import datetime

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_subject', 'post_url', 'post_title', 'contact', 'uploader', 'post_text']
    }
    # var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    # for key in key_list :
    #     var[f'parse_{key}'] = globals()[f'parse_{key}']
    # # 2021-01-11
    # var['table_header'] = ["제목", "담당부서", "연락처", "등록일", "조회수"]
    # result = parse_board_type_html_page(soup, var, key_list)

    var, json_data, key_list = json_type_default_setting(params, target_key_info)

    data_list = json_data['list']
    for data in data_list:
        if 'regDt' in data.keys():
            var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(data['regDt']))
        else:
            var['uploaded_time'].append('')
        if 'chrgrTelno' in data.keys():

            var['contact'].append(data['chrgrTelno'])
        else:
            var['contact'].append('')
        uploader = ''
        if 'chgeDpcd' in data.keys():
            uploader += data['chgeDpcd'] + ' '
        if 'chrgrNm' in data.keys():
            uploader += data['chrgrNm'] + ' '
        var['uploader'].append(uploader)
        var['post_subject'].append(data['CTGRY_NM'])
        var['post_title'].append(data['ttl'])
        var['post_url'].append(
            var['post_url_frame'].format(data['BBS_NM'], data['bbsId'])
        )
        var['post_text'].append(clean_text(remove_tags(data['cn'])))

    result = merge_var_to_dict(key_list, var)
    return result

def parse_creatDttm(uploaded_time):
    return datetime.datetime.utcfromtimestamp(uploaded_time / 1000)

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    customer = extract_text_from_single_tag(soup, 'div', child_tag_attrs={'class' : 'customer'})
    var['contact'] = extract_contact_numbers_from_text(customer)

    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'cont'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    return result


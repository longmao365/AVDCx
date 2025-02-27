#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os
import json
from PIL import Image
from Getter import iqqtv_new, javbus, javdb, jav321, dmm, javlibrary_new, avsox, xcity, mgstage, fc2, fc2club, fc2hub, airav
import Function.config as cf

# ========================================================================补全字段判断缺失字段


def getTheData(json_data_more, json_data, flag_suren=False):
    json_data['req_web'] = json_data_more['req_web']
    json_data['log_info'] = json_data_more['log_info']
    # 原json_data无数据
    if not getDataState(json_data):
        return json_data_more
    # 补全网站未刮削到内容
    if not getDataState(json_data_more):
        return json_data
    # 补全网站刮削到内容
    if not json_data['actor'] or json_data['actor'] == '素人' or flag_suren:
        json_data['actor'] = json_data_more['actor']
        json_data['actor_photo'] = json_data_more['actor_photo']
    if not json_data['outline']:
        json_data['outline'] = json_data_more['outline']
    if not json_data['tag']:
        json_data['tag'] = json_data_more['tag']
    if not json_data['release']:
        json_data['release'] = json_data_more['release']
    if not json_data['year']:
        json_data['year'] = json_data_more['year']
    if not json_data['runtime']:
        json_data['runtime'] = json_data_more['runtime']
    if not json_data['score']:
        json_data['score'] = json_data_more['score']
    if not json_data['series']:
        json_data['series'] = json_data_more['series']
    if not json_data['director']:
        json_data['director'] = json_data_more['director']
    if not json_data['studio']:
        json_data['studio'] = json_data_more['studio']
    if not json_data['publisher']:
        json_data['publisher'] = json_data_more['publisher']
    if not json_data['cover_small']:
        json_data['cover_small'] = json_data_more['cover_small']
        json_data['image_download'] = json_data_more['image_download']
        json_data['image_cut'] = json_data_more['image_cut']
    # 如果是素人，且有小图，则改成下载poster
    if (flag_suren or 'VR' in json_data['tag']) and json_data['cover_small']:
        json_data['image_download'] = True
    if not json_data['extrafanart']:
        json_data['extrafanart'] = json_data_more['extrafanart']
    try:
        if json_data_more['mosaic'] and not json_data['mosaic']:
            json_data['mosaic'] = json_data_more['mosaic']
    except:
        pass
    return json_data


# ========================================================================补全字段


def getMoreData(number, appoint_url, json_data):
    config = cf.get_config()
    main_like = config.get('main_like')
    more_website = config.get('more_website')
    req_web = json_data['req_web']
    log_info = json_data['log_info']
    flag_suren = False
    # 未开启偏好字段 or 未勾选补全网站
    if not main_like or not more_website:
        return json_data
    # 提取类似259luxu-1111素人番号，使用javdb的演员名字替换
    if re.search(r'\d{2,}[a-zA-Z]{2,}-\d{3,}', number) or 'LUXU' in number.upper() or 'SIRO' in number.upper() or 'GANA' in number.upper() or 'ARA-' in number.upper() or 'MIUM' in number.upper():
        number = re.search(r'[a-zA-Z]+-\d+', number).group()
        flag_suren = True
    # 使用网站补全
    if 'javdb' in more_website and 'javdb' not in req_web:
        json_data_more = json.loads(javdb.main(number, appoint_url, log_info, req_web))
        json_data = getTheData(json_data_more, json_data, flag_suren)
        req_web = json_data['req_web']
        log_info = json_data['log_info']
    if 'jav321' in more_website and 'jav321' not in req_web:
        json_data_more = json.loads(jav321.main(number, appoint_url, log_info, req_web))
        json_data = getTheData(json_data_more, json_data)
        req_web = json_data['req_web']
        log_info = json_data['log_info']
    if 'javlibrary' in more_website and 'javlibrary' not in req_web:
        json_data_more = json.loads(javlibrary_new.main(number, appoint_url, log_info, req_web))
        json_data = getTheData(json_data_more, json_data)
        req_web = json_data['req_web']
        log_info = json_data['log_info']
    if 'dmm' in more_website and 'dmm' not in req_web:
        json_data_more = json.loads(dmm.main(number, appoint_url, log_info, req_web))
        json_data = getTheData(json_data_more, json_data)
    return json_data


# ========================================================================是否为无码


def is_uncensored(number):
    if re.match(r'^\d{4,}', number) or re.match(r'n\d{4}', number) or 'HEYZO' in number.upper() or re.search(r'[^.]+\.\d{2}\.\d{2}\.\d{2}', number):
        return True
    else:
        return False


# ========================================================================元数据获取失败检测


def getDataState(json_data):
    if json_data['title'] == '' or json_data['title'] == 'None' or json_data['title'] == 'null':
        return False
    else:
        return True


# ========================================================================获取视频列表


def movie_lists(escape_folder, movie_type, movie_path):
    if escape_folder != '':
        escape_folder = re.split('[,，]', escape_folder)
    total = []
    file_type = movie_type.split('|')
    file_root = movie_path.replace('\\', '/')
    for root, dirs, files in os.walk(file_root):
        if escape_folder != '':
            flag_escape = 0
            root = root.replace('\\', '/') + '/'
            for folder in escape_folder:
                if folder in root:
                    flag_escape = 1
                    break
            if flag_escape == 1:
                continue
        for f in files:
            file_name, file_type_current = os.path.splitext(f)
            if re.search(r'^\..+', file_name):
                continue
            if file_type_current.lower() in file_type:
                path = os.path.join(root, f)
                # path = path.replace(file_root, '.')
                path = path.replace("\\\\", "/").replace("\\", "/")
                total.append(path)
    return total


# ========================================================================获取番号


def getNumber(filepath, escape_string):
    filepath = filepath.upper().replace('1080P', '').replace('720P', '').replace('-C.', '.').replace('.PART', '-CD').replace('-PART', '-CD').replace(' ', '-')
    filename = os.path.splitext(os.path.split(filepath)[1])[0]
    # 排除多余字符
    escape_string_list = re.split('[,，]', escape_string)
    for string in escape_string_list:
        filename = filename.replace(string.upper(), '')
    # 再次排除多余字符
    filename = filename.replace('HEYDOUGA-', '').replace('HEYDOUGA', '').replace('CARIBBEANCOM', '').replace('CARIB', '').replace('1PONDO', '').replace('1PON', '').replace('PACOMA', '').replace('PACO', '').replace('10MUSUME', '').replace('-10MU', '').replace('FC2PPV', 'FC2-').replace('--', '-')
    part = ''
    if re.search(r'-CD\d+', filename):
        part = re.findall(r'-CD\d+', filename)[0]
    filename = filename.replace(part, '')
    filename = str(re.sub(r"-\d{4}-\d{1,2}-\d{1,2}", "", filename))              # 去除文件名中时间
    filename = str(re.sub(r"\d{4}-\d{1,2}-\d{1,2}-", "", filename))              # 去除文件名中时间
    if re.search(r'[^.]+\.\d{2}\.\d{2}\.\d{2}', filename):                       # 提取欧美番号 sexart.11.11.11
        try:
            file_number = re.search(r'[^.]+\.\d{2}\.\d{2}\.\d{2}', filename).group()
            return file_number.lower()
        except:
            return filename.lower()
    elif re.search(r'XXX-AV-\d{4,}', filename):                                  # 提取xxx-av-11111
        file_number = re.search(r'XXX-AV-\d{4,}', filename).group()
        return file_number
    elif re.search(r'TH101-\d{3,}-\d{5,}', filename):                            # 提取th101-140-112594
        file_number = re.search(r'TH101-\d{3,}-\d{5,}', filename).group().lower()
        return file_number
    elif '-' in filename or '_' in filename:                                     # 普通提取番号 主要处理包含减号-和_的番号
        if 'FC2' in filename:
            filename = filename.replace('PPV', '').replace('_', '-').replace('--', '-')
            if re.search(r'FC2-\d{5,}', filename):                               # 提取类似fc2-111111番号
                file_number = re.search(r'FC2-\d{5,}', filename).group()
        elif re.search(r'\d+[a-zA-Z]+-\d+', filename):                           # 提取类似259luxu-1456番号
            file_number = re.search(r'\d+[a-zA-Z]+-\d+', filename).group()
        elif re.search(r'[a-zA-Z]+-\d+', filename):                              # 提取类似mkbd-120番号
            if 'LUXU' in filename:                                               # 提取类似luxu-1111番号
                file_number = '259' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'GANA' in filename:                                             # 200GANA-2556
                file_number = '200' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'MAAN' in filename or 'MIUM' in filename or 'NTK-' in filename: # 300MAAN-673/300MIUM-745/300NTK-635
                file_number = '300' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'JAC-' in filename:                                             # 390JAC-034
                file_number = '390' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'DCV-' in filename:                                             # 277DCV-102
                file_number = '277' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'NTR-' in filename:                                             # 348NTR-001
                file_number = '348' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'ARA-' in filename:                                             # 261ARA-094
                file_number = '261' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'TEN-' in filename:                                             # 459TEN-024
                file_number = '459' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'GCB-' in filename:                                             # 485GCB-015
                file_number = '485' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'SEI-' in filename:                                             # 502SEI-001
                file_number = '502' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'KNB-' in filename:                                             # 336KNB-172
                file_number = '336' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'SUKE-' in filename:                                            # 428SUKE-086
                file_number = '428' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'HHH-' in filename:                                             # 451HHH-027
                file_number = '451' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'MLA-' in filename:                                             # 476MLA-043
                file_number = '476' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'KJO-' in filename:                                             # 326KJO-002
                file_number = '326' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'SIMM-' in filename:                                            # 345SIMM-662
                file_number = '345' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'MFC-' in filename:                                             # 435MFC-142
                file_number = '435' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'SHN-' in filename:                                             # 116SHN-045
                file_number = '116' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'NAMA-' in filename:                                            # 332NAMA-077
                file_number = '332' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'CUTE-' in filename:                                            # 229SCUTE-953
                file_number = '229' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            elif 'KIRAY-' in filename:                                           # 314KIRAY-128
                file_number = '314' + \
                    re.search(r'[a-zA-Z]+-\d+', filename).group()
            else:
                file_number = re.search(r'[a-zA-Z]+-\d+', filename).group()
        elif re.search(r'[a-zA-Z]+-[a-zA-Z]\d+', filename):                      # 提取类似mkbd-s120番号
            file_number = re.search(r'[a-zA-Z]+-[a-zA-Z]\d+', filename).group()
        elif re.search(r'\d+-\d+', filename):                                    # 提取类似 111111-000 番号
            file_number = re.search(r'\d+-\d+', filename).group()
        elif re.search(r'\d+_\d+', filename):                                    # 提取类似 111111_000 番号
            file_number = re.search(r'\d+_\d+', filename).group()
        elif re.search(r'\d+-[a-zA-Z]+', filename):                              # 提取类似 111111-MMMM 番号
            file_number = re.search(r'\d+-[a-zA-Z]+', filename).group()
        else:
            file_number = filename
        return file_number
    elif re.search(r'[A-Z]{3,}00\d{3}', filename):                               # 提取ssni00644为ssni-644
        file_number = re.search(r'[A-Z]{3,}00\d{3}', filename).group()
        file_char = re.search(r'[A-Z]{3,}', file_number).group()
        a = file_char + '00'
        b = file_char + '-'
        file_number = file_number.replace(a, b)
        return file_number
    elif re.search(r'N\d{4}', filename):                                         # 提取N1111
        file_number = re.search(r'N\d{4}', filename).group()
        return file_number.lower()
    else:                                                                        # 提取不含减号-的番号，FANZA CID 保留ssni00644，将MIDE139改成MIDE-139
        try:
            find_num = re.findall(r'\d+', filename)[0]
            find_char = re.findall(r'\D+', filename)[0]
            if len(find_num) <= 4 and len(find_char) > 1:
                file_number = find_char + '-' + find_num
            return file_number
        except:
            return filename


# ========================================================================根据番号获取数据


def getDataFromJSON(file_number, website_mode, appoint_url, translate_language, json_data): # 从JSON返回元数据
    c_word = json_data['c_word']
    leak = json_data['leak']
    cd_part = json_data['cd_part']
    destroyed = json_data['destroyed']
    mosaic = json_data['mosaic']
    version = json_data['version']

    # ================================================网站规则添加开始================================================

    if website_mode == 1:                                                      # 从全部网站刮削

        # =======================================================================FC2-111111
        if 'FC2' in file_number.upper():
            file_number = re.search(r'\d{4,}', file_number).group()
            json_data = json.loads(fc2.main(file_number, appoint_url))
            # if not getDataState(json_data):   # 暂时屏蔽，该网站目前不可用
            #     req_web = json_data['req_web']
            #     log_info = json_data['log_info']
            #     json_data = json.loads(fc2club.main(file_number, appoint_url, log_info, req_web))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(fc2hub.main(file_number, appoint_url, log_info, req_web))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(avsox.main(file_number, appoint_url, log_info, req_web))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(airav.main(file_number, appoint_url, translate_language, log_info, req_web))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(javdb.main(file_number, appoint_url, log_info, req_web))

        # =======================================================================sexart.15.06.14
        elif re.search(r'[^.]+\.\d{2}\.\d{2}\.\d{2}', file_number):
            json_data = json.loads(javdb.main(file_number, appoint_url))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(javbus.main(file_number, appoint_url, log_info, req_web))

        # =======================================================================无码抓取:111111-111,n1111,HEYZO-1111,SMD-115
        elif mosaic == '无码' or mosaic == '無碼':
            json_data = json.loads(iqqtv_new.main(file_number, appoint_url, translate_language))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(javbus.main(file_number, appoint_url, log_info, req_web))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(javdb.main(file_number, appoint_url, log_info, req_web, True))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(jav321.main(file_number, appoint_url, log_info, req_web, True))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(avsox.main(file_number, appoint_url, log_info, req_web))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(airav.main(file_number, appoint_url, translate_language, log_info, req_web))

        # =======================================================================259LUXU-1111
        elif re.match(r'\d+[a-zA-Z]+-\d+', file_number) or 'SIRO' in file_number.upper():
            json_data = json.loads(mgstage.main(file_number, appoint_url))
            file_number1 = re.search(r'[a-zA-Z]+-\d+', file_number).group()
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(jav321.main(file_number1, appoint_url, log_info, req_web))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(javdb.main(file_number1, appoint_url, log_info, req_web))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(javbus.main(file_number1, appoint_url, log_info, req_web))

        # =======================================================================ssni00321
        elif re.match(r'\D{2,}00\d{3,}', file_number) and '-' not in file_number and '_' not in file_number:
            json_data = json.loads(dmm.main(file_number, appoint_url))

        # =======================================================================MIDE-139
        else:
            json_data = json.loads(iqqtv_new.main(file_number, appoint_url, translate_language))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(javbus.main(file_number, appoint_url, log_info, req_web))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(javdb.main(file_number, appoint_url, log_info, req_web))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(jav321.main(file_number, appoint_url, log_info, req_web))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(airav.main(file_number, appoint_url, translate_language, log_info, req_web))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(javlibrary_new.main(file_number, appoint_url, log_info, req_web))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(xcity.main(file_number, appoint_url, log_info, req_web))
            if not getDataState(json_data):
                req_web = json_data['req_web']
                log_info = json_data['log_info']
                json_data = json.loads(avsox.main(file_number, appoint_url, log_info, req_web))
    elif website_mode == 2:                                                    # 仅从iqqtv
        json_data = json.loads(iqqtv_new.main(file_number, appoint_url, translate_language))
    elif website_mode == 3:                                                    # 仅从javbus
        json_data = json.loads(javbus.main(file_number, appoint_url))
    elif website_mode == 4:                                                    # 仅从javdb
        json_data = json.loads(javdb.main(file_number, appoint_url))
    elif website_mode == 5:                                                    # 仅从jav321
        json_data = json.loads(jav321.main(file_number, appoint_url))
    elif website_mode == 6:                                                    # 仅从dmm
        json_data = json.loads(dmm.main(file_number, appoint_url))
    elif website_mode == 7:                                                    # 仅从avsox
        json_data = json.loads(avsox.main(file_number, appoint_url))
    elif website_mode == 8:                                                    # 仅从xcity
        json_data = json.loads(xcity.main(file_number, appoint_url))
    elif website_mode == 9:                                                    # 仅从mgstage
        json_data = json.loads(mgstage.main(file_number, appoint_url))
    elif website_mode == 10:                                                   # 仅从fc2
        json_data = json.loads(fc2.main(file_number, appoint_url))
    elif website_mode == 11:                                                   # 仅从fc2club
        json_data = json.loads(fc2club.main(file_number, appoint_url))
    elif website_mode == 12:                                                   # 仅从fc2hub
        json_data = json.loads(fc2hub.main(file_number, appoint_url))
    elif website_mode == 13:                                                   # 仅从airav
        json_data = json.loads(airav.main(file_number, appoint_url, translate_language))
    elif website_mode == 14:                                                   # 仅从javlibrary
        json_data = json.loads(javlibrary_new.main(file_number, appoint_url))

    # ================================================网站规则添加结束================================================
    # ======================================补全字段
    json_data = getMoreData(file_number, appoint_url, json_data)

    # ======================================超时或未找到返回
    if json_data['error_type'] or json_data['title'] == '':
        return json_data

    # ======================================处理得到的信息
    config = cf.get_config()
    # 番号
    number = json_data['number']

    # 演员
    actor = str(json_data['actor']).strip(" [ ]").replace("'", '').replace(', ', ',').replace('<', '(').replace('>', ')').strip(',') # 列表转字符串（避免个别网站刮削返回的是列表）

    # 标题处理，去除标题尾巴的演员名
    title = json_data['title']
    if config.get('del_actor_name'):
        title = title.replace((' ' + actor), '')

    if not actor:
        actor = config.get('actor_no_name')

    # 发行日期
    release = json_data['release']
    release = release.replace('/', '-').strip('. ')

    # poster图
    try:
        cover_small = json_data['cover_small']
    except:
        cover_small = ''

    # 标签
    tag = str(json_data['tag']).strip(" [ ]").replace("'", '').replace(', ', ',').replace(',720P', '').replace(',1080P', '').replace(',720p', '').replace(',1080p', '').replace(',HD高画质', '').replace(',HD高畫質', '').replace(',高画质', '').replace(',高畫質', '') # 列表转字符串（避免个别网站刮削返回的是列表）

    # outline
    try:
        json_data['outline'] = json_data['outline'].replace(u'\xa0', '').replace(u'\u3000', '').replace(u'\u2800', '').strip('. ')
    except:
        json_data['outline'] = ''

    # studio
    try:
        json_data['studio'] = json_data['studio'].replace(u'\xa0', '').replace(u'\u3000', '').replace(u'\u2800', '').strip('. ')
    except:
        json_data['studio'] = ''

    # publisher
    try:
        json_data['publisher'] = json_data['publisher'].replace(u'\xa0', '').replace(u'\u3000', '').replace(u'\u2800', '').strip('. ')
    except:
        json_data['publisher'] = json_data['studio']

    # 马赛克
    try:
        json_data['mosaic']
    except:
        json_data['mosaic'] = ''
    finally:
        if not json_data['mosaic']:
            if is_uncensored(number):
                json_data['mosaic'] = '无码'
            else:
                json_data['mosaic'] = '有码'
        print(number, json_data['mosaic'])

    # 命名规则
    naming_media = config.get('naming_media')
    naming_file = config.get('naming_file')
    folder_name = config.get('folder_name')

    # 返回处理后的json_data
    json_data['title'] = title.replace(u'\xa0', '').replace(u'\u3000', '').replace(u'\u2800', '').strip('. ')
    json_data['number'] = number
    json_data['actor'] = actor.replace(u'\xa0', '').replace(u'\u3000', '').replace(u'\u2800', '').strip('. ')
    json_data['release'] = release
    json_data['cover_small'] = cover_small
    json_data['tag'] = tag.replace(u'\xa0', '').replace(u'\u3000', '').replace(u'\u2800', '').strip('. ')
    json_data['naming_media'] = naming_media
    json_data['naming_file'] = naming_file
    json_data['folder_name'] = folder_name
    json_data['c_word'] = c_word
    json_data['leak'] = leak
    json_data['cd_part'] = cd_part
    json_data['destroyed'] = destroyed
    json_data['actor_href'] = ''
    json_data['version'] = version

    return json_data


# ========================================================================返回json里的数据


def get_info(json_data):
    for key, value in json_data.items():                                       # 去除unknown
        if str(value).lower() == 'unknown':
            json_data[key] = ''

    title = json_data['title']
    studio = json_data['studio']
    publisher = json_data['publisher']
    year = json_data['year']
    outline = json_data['outline']
    runtime = json_data['runtime']
    director = json_data['director']
    actor_photo = json_data['actor_photo']
    actor = json_data['actor']
    release = json_data['release']
    tag = json_data['tag']
    number = json_data['number']
    cover = json_data['cover']
    website = json_data['website']
    series = json_data['series']
    mosaic = json_data['mosaic']
    definition = json_data['definition']

    return title, studio, publisher, str(year), outline, str(runtime), director, actor_photo, actor, release, tag, number, cover, website, series, mosaic, definition


# ========================================================================检查图片


def check_pic(path_pic):
    if os.path.exists(path_pic):
        try:
            img = Image.open(path_pic)
            img.load()
            return True
        except:
            try:
                os.removie(path_pic)
            except:
                pass
            # print('文件损坏')
    return False

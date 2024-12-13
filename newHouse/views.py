import base64
import json
from datetime import date

from django.shortcuts import render
import requests
import jsonpath
from django.core.cache import cache

from newHouse.models import Building


def index(request):
    projectname = request.GET.get('projectname')
    entname = request.GET.get('entName')

    cookies = {
        'ASP.NET_SessionId': 'arkkpe50xfwqomoqri0qz552',
    }

    headers = {
        'authority': 'www.cq315house.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        # 'cookie': 'ASP.NET_SessionId=arkkpe50xfwqomoqri0qz552',
        'origin': 'https://www.cq315house.com',
        'pragma': 'no-cache',
        'referer': 'https://www.cq315house.com/HtmlPage/serviceSeaList.html?projectname=%E5%8D%B0%E6%82%A6',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.121 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    json_data = {
        'siteid': '',
        'useType': '',
        'areaType': '',
        'projectname': projectname,
        'entName': entname,
        'location': '',
        'minrow': '1',
        'maxrow': '11',
    }

    response = requests.post(
        'https://www.cq315house.com/WebService/WebFormService.aspx/getParamDatas',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    project = response.text
    project = (project.lstrip('{"d":"').rstrip('"}')).replace('\\"', '"')
    project = json.loads(project)

    context = {'Project': project}
    return render(request, 'index.html', context)


def getproject(request):
    projectId = request.GET.get('projectId')
    if projectId == None:
        projectId = 833345

    cookies = {
        'ASP.NET_SessionId': 'arkkpe50xfwqomoqri0qz552',
    }

    headers = {
        'authority': 'www.cq315house.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        # 'cookie': 'ASP.NET_SessionId=arkkpe50xfwqomoqri0qz552',
        'origin': 'https://www.cq315house.com',
        'referer': 'https://www.cq315house.com/HtmlPage/serviceSeaListDes.html?projectid=901142',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.121 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    json_data = {
        'projectId': projectId,
    }

    response = requests.post(
        'https://www.cq315house.com/WebService/WebFormService.aspx/getProjectInfoByProjectId',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    project = response.text
    project = (project.lstrip('{"d":"').rstrip('"}')).replace('\\"', '"')
    project = json.loads(project)
    context = {'Project': project}
    return render(request, 'getproject.html', context)


def getbuilding(request):
    buildingid = request.GET.get('buildingid')

    if buildingid == None:
        buildingid = '_aqavcBJHT/NX4YLhxn7aA'

    blockname = request.GET.get('blockname')
    cache.set('blockname_key', blockname, timeout=300)

    type1 = request.GET.get('type')
    if type1 == None:
        type1 = '1'

    cookies = {
        'ASP.NET_SessionId': 'arkkpe50xfwqomoqri0qz552',
    }

    headers = {
        'authority': 'www.cq315house.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type1': 'application/json',
        # 'cookie': 'ASP.NET_SessionId=arkkpe50xfwqomoqri0qz552',
        'origin': 'https://www.cq315house.com',
        'pragma': 'no-cache',
        'referer': 'https://www.cq315house.com/HtmlPage/ShowRooms.html?buildingid=TccuKHqrr_wKCxTwHj4YLA&block=%E8%A7%84%E5%88%923%E5%8F%B7%E6%A5%BC',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.121 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    json_data = {
        'buildingid': buildingid,
    }

    response_RoomJson = requests.post(
        'https://www.cq315house.com/WebService/WebFormService.aspx/GetRoomJson',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    response_BuildingInfo = requests.post(
        'https://www.cq315house.com/WebService/WebFormService.aspx/GetBuildingInfo',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    raw_string = response_BuildingInfo.text
    # 解析原始字符串为Python字典
    data_dict = json.loads(raw_string)

    # 解析嵌套的字符串为Python字典
    nested_dict = json.loads(data_dict['d'])

    # 将整个数据结构转换为格式良好的JSON字符串
    data_b = json.dumps(nested_dict, ensure_ascii=False, indent=4)
    data_b = json.loads(data_b)

    d = response_RoomJson.text  # 获取JSON
    d = (d.lstrip('{"d":"').rstrip('"}')).replace('\\"', '"')  # 整理格式
    cache.set('room_info', d, timeout=3000)
    # print(type(d))  # 测试用
    data = json.loads(d)  # 加载JSON

    units_count = len(data)  # 获取单元数
    floors_count = max(jsonpath.jsonpath(data, '$..y'))  # 取得最大楼物理层数
    units_rooms_count = []  # 初始化每个单元一层楼有多少房间数
    for i in range(units_count):
        units_rooms_count.append(data[i]['maxX'])  # 遍历每个单元，并取每个单元一层楼有多少房间数

    # 取得data[rooms]roomstatus=='状态'的数量
    def get_sale_count(data, roomstatus):
        count = 0
        for building in data:
            for room in building['rooms']:
                if room['roomstatus'] == roomstatus and room['use'] != '其他用房' and room['use'] != '物管用房':
                    count += 1
        return str(count)

    def get_total_area(data):
        area = 0
        for building in data:
            for room in building['rooms']:
                if room['use'] != '其他用房' and room['use'] != '物管用房':
                    area += room['bArea']
        return area

    def get_total_price(data):
        price = 0
        for building in data:
            for room in building['rooms']:
                if room['nsjmjg'] != 0:
                    price += room['bArea'] * room['nsjmjg']
        return price

    total_area = round(get_total_area(data), 2)
    total_price = round(get_total_price(data) / 10000)
    if total_area != 0:
        average_price = round(get_total_price(data) / get_total_area(data))
    else:
        average_price = 0

    def get_nosale_count(data):
        count = 0
        for building in data:
            for room in building['rooms']:
                if room['use'] == '其他用房' or room['use'] == '物管用房':
                    count += 1
        return str(count)

    # 定义函数，通过单元号，Y，X，返回所需数据key的值，若为空则返回str
    def get_room_data(data, name, y, x, key, str1):
        for building in data:
            if building['name'] == name:
                for room in building['rooms']:
                    if room['y'] == y and room['x'] == x:
                        if key == 'nsjmjg':
                            return str(round(float(room[key])))
                        return str(room[key])
        return str1

    # 获取房间是否不可售
    def get_room_status(data, name, y, x):
        if get_room_data(data, name, y, x, 'use', '') == '其他用房' or get_room_data(data, name, y, x, 'use',
                                                                                     '') == '物管用房':
            return '不可售'
        else:
            return ''

    # 通过data，生成表格的HTML

    # 生成单元表头
    table_html = '<table><thead><tr><th>楼栋</th><th>' + blockname + '</th>'
    for i in range(units_count):
        table_html += '<th colspan="' + str(units_rooms_count[i]) + '">' + str(i + 1) + '单元</th>'
    table_html += '</tr>'

    # 生成房号表头
    table_html += '<tr><th>物理层</th><th>名义层</th>'
    for i in range(units_count):
        for j in range(units_rooms_count[i]):
            table_html += '<th>' + str(j + 1) + '号房</th>'
    table_html += '</tr></thead><tbody>'

    # 生成每层楼数据（显示房号）
    if type1 == '1':
        for y in range(floors_count, 0, -1):
            table_html += '<tr><td>第' + str(y) + '层</td><td>第' + get_room_data(data, str(1), y, 1, 'flr',
                                                                                  '未知') + '层</td>'
            for name in range(units_count):
                for x in range(units_rooms_count[name]):
                    table_html += '<td id="' + get_room_status(data, str(name + 1), y,
                                                               x + 1) + '" class="' + get_room_data(
                        data, str(name + 1), y, x + 1, 'roomstatus',
                        '') + '"><a href="#" onclick="window.open(\'/getroom/?fid=' + get_room_data(data, str(name + 1),
                                                                                                    y,
                                                                                                    x + 1, 'id',
                                                                                                    '') + '\', \'_blank\', \'width=954,height=233\'); return false;">' + get_room_data(
                        data, str(name + 1), y,
                        x + 1, 'flr',
                        '') + '-' + get_room_data(
                        data,
                        str(name + 1),
                        y,
                        x + 1,
                        'rn',
                        '') + '</a></td>'
            table_html += '</tr>'
        table_html += '</tbody></table>'
    # 生成每层楼数据（显示面积）
    if type1 == '2':
        for y in range(floors_count, 0, -1):
            table_html += '<tr><td>第' + str(y) + '层</td><td>第' + get_room_data(data, str(1), y, 1, 'flr',
                                                                                  '未知') + '层</td>'
            for name in range(units_count):
                for x in range(units_rooms_count[name]):
                    table_html += '<td id="' + get_room_status(data, str(name + 1), y,
                                                               x + 1) + '" class="' + get_room_data(
                        data, str(name + 1), y, x + 1, 'roomstatus',
                        '') + '"><a href="#" onclick="window.open(\'/getroom/?fid=' + get_room_data(data, str(name + 1),
                                                                                                    y,
                                                                                                    x + 1, 'id',
                                                                                                    '') + '\', \'_blank\', \'width=954,height=233\'); return false;">' + get_room_data(
                        data, str(name + 1), y,
                        x + 1, 'bArea',
                        '') + '</a></td>'
            table_html += '</tr>'
        table_html += '</tbody></table>'
        # 生成每层楼数据（显示单价）
    if type1 == '3':
        for y in range(floors_count, 0, -1):
            table_html += '<tr><td>第' + str(y) + '层</td><td>第' + get_room_data(data, str(1), y, 1, 'flr',
                                                                                  '未知') + '层</td>'
            for name in range(units_count):
                for x in range(units_rooms_count[name]):
                    table_html += '<td id="' + get_room_status(data, str(name + 1), y,
                                                               x + 1) + '" class="' + get_room_data(
                        data, str(name + 1), y, x + 1, 'roomstatus',
                        '') + '"><a href="#" onclick="window.open(\'/getroom/?fid=' + get_room_data(data,
                                                                                                    str(name + 1),
                                                                                                    y,
                                                                                                    x + 1, 'id',
                                                                                                    '') + '\', \'_blank\', \'width=954,height=233\'); return false;">' + get_room_data(
                        data, str(name + 1), y,
                        x + 1, 'nsjmjg',
                        '') + '</a></td>'
            table_html += '</tr>'
        table_html += '</tbody></table>'

    # 获取今天的日期
    today = date.today()

    # 查询 date_added 等于今天的 Building 对象
    existing_buildings = Building.objects.filter(date_added=today, buildingid=buildingid)

    if not existing_buildings.exists():
        new_building = Building(
            buildingid=buildingid,
            online_signatures=get_sale_count(data, '网签'),
            subscriptions=get_sale_count(data, '认购'),
            ready_houses=get_sale_count(data, '现房'),
            future_houses=get_sale_count(data, '期房'),
            mortgages=get_sale_count(data, '房屋抵押'),
            unsold_units=get_nosale_count(data),
            project_name=data_b['projectName']
        )
        new_building.save()

    buildings = Building.objects.filter(buildingid=buildingid).order_by('-date_added')

    context = {'table_html': table_html,
               'sing': get_sale_count(data, '网签'),
               'buy': get_sale_count(data, '认购'),
               'now': get_sale_count(data, '现房'),
               'period': get_sale_count(data, '期房'),
               'mortgage': get_sale_count(data, '房屋抵押'),
               'nosale': get_nosale_count(data),
               'Buildings': buildings,
               'data_b': data_b,
               'buildingid': buildingid,
               'blockname': blockname,
               'total_area': total_area,
               'total_price': total_price,
               'average_price': average_price
               }

    return render(request, 'getbuilding.html', context)


def getroom(request):
    fid = request.GET.get('fid')
    data = cache.get('room_info')
    # print(data)
    data = json.loads(data)

    def get_room_data(data, fid, key):
        for item in data:
            for room in item['rooms']:
                if room['id'] == fid:
                    return room.get(key)
        return '未知'

    roomname = str(get_room_data(data, fid, 'flr')) + '-' + str(get_room_data(data, fid, 'rn'))
    block = cache.get('blockname_key')
    bArea = get_room_data(data, fid, 'bArea')
    iArea = get_room_data(data, fid, 'iArea')
    use = get_room_data(data, fid, 'use')
    rType = get_room_data(data, fid, 'rType')
    nsjg = get_room_data(data, fid, 'nsjg')
    nsjmjg = get_room_data(data, fid, 'nsjmjg')
    location = get_room_data(data, fid, 'location')
    roomstatus = get_room_data(data, fid, 'roomstatus')

    context = {
        'roomname': roomname,
        'block': block,
        'bArea': bArea,
        'iArea': iArea,
        'use': use,
        'rType': rType,
        'nsjg': nsjg,
        'nsjmjg': nsjmjg,
        'location': location,
        'roomstatus': roomstatus
    }

    return render(request, 'getroom.html', context)

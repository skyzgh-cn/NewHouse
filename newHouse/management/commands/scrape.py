import json
import time

from django.core.management.base import BaseCommand
import requests
from newHouse.models import Building
from datetime import date


class Command(BaseCommand):
    help = 'Scrapes data from a website'

    def handle(self, *args, **options):
        today = date.today()

        today_building_ids = Building.objects.filter(date_added=today).values_list('buildingid',
                                                                                   flat=True)  # 这段代码筛选出今天有数据的 buildingid

        all_building_ids = Building.objects.values_list('buildingid', flat=True).distinct()  # 这段代码获取所有 buildingid

        task = set(all_building_ids) - set(today_building_ids)

        count = 0

        def get_nosale_count(data):
            count = 0
            for building in data:
                for room in building['rooms']:
                    if room['use'] == '其他用房' or room['use'] == '物管用房':
                        count += 1
            return str(count)

        def get_sale_count(data, roomstatus):
            count = 0
            for building in data:
                for room in building['rooms']:
                    if room['roomstatus'] == roomstatus and room['use'] != '其他用房' and room['use'] != '物管用房':
                        count += 1
            return str(count)

        # 定义爬取参数
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
            'referer': 'https://www.cq315house.com/HtmlPage/ShowRooms.html?buildingid=TccuKHqrr_wKCxTwHj4YLA&block=%E8%A7%84%E5%88%923%E5%8F%B7%E6%A5%BC',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.121 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        for buildingid in task:
            json_data = {
                'buildingid': buildingid,
            }
            response = requests.post(
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
            print(data_b)

            d = response.text  # 获取JSON
            d = (d.lstrip('{"d":"').rstrip('"}')).replace('\\"', '"')  # 整理格式
            data = json.loads(d)  # 加载JSON
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
            count += 1
            time.sleep(1)  # 暂停 1 秒

        self.stdout.write(self.style.SUCCESS('共计' + str(len(task)) + '个爬取任务，已完成' + str(count)))

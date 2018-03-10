import json
from pprint import pprint
import requests_html

session = requests_html.HTMLSession()


def get_one_page(url):
    query = {
        'city': '杭州',
        'isSchoolJob': 0,
        'needAddtionalResult': 'false'
    }
    form = {
        'first': 'true',
        'kd': 'python爬虫',
        'pn': 1
    }
    headers = {
        'Referer': 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?o'
                   'query=Python&fromSearch=true&labelWords=relative&city=%E6%9D%AD%E5%B7%9E'
    }
    try:
        response = session.post(url, params=query, data=form, headers=headers, timeout=3)
        if response.status_code == 200:
            return response
        return None
    except Exception as e:
        print(e)


def parse_one_page(response):
    data = json.loads(response.text)
    if data:
        # cnt = data.get('content').get('positionResult').get('totalCount')
        result = data.get('content').get('positionResult').get('result')
    pprint(result)




def main():
    url = 'https://www.lagou.com/jobs/positionAjax.json'
    r = get_one_page(url)
    parse_one_page(r)


if __name__ == '__main__':
    main()






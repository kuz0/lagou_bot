import time
import json
from pprint import pprint
from requests_html import HTMLSession as session


class LagouSpider(object):
    CITY = '杭州'
    KEYWORD = 'python爬虫'

    def __init__(self):
        self.headers = {
            'Referer': 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?o'
                       'query=Python&fromSearch=true&labelWords=relative&city=%E6%9D%AD%E5%B7%9EE',
            'Cookie': 'JSESSIONID=ABAAABAACBHABBI0F2B37E283D7144A43DEB69877C78088;'
                      ' _ga=GA1.2.2025928436.1521095805;'
                      ' _gat=1;'
                      ' user_trace_token=20180315143644-3aad5add-281b-11e8-b1ed-5254005c3644;'
                      ' LGSID=20180315143644-3aad5d45-281b-11e8-b1ed-5254005c3644;'
                      ' PRE_UTM=;'
                      ' PRE_HOST=www.bing.com;'
                      ' PRE_SITE=https%3A%2F%2Fwww.bing.com%2F;'
                      ' PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F;'
                      ' LGRID=20180315144113-daacb6e4-281b-11e8-b23d-525400f775ce;'
                      ' LGUID=20180315143644-3aad5fa9-281b-11e8-b1ed-5254005c3644;'
                      ' Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1521095806;'
                      ' Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1521096073;'
                      ' index_location_city=%E6%9D%AD%E5%B7%9E;'
                      ' hideSliderBanner20180305WithTopBannerC=1;'
                      ' TG-TRACK-CODE=index_navigation;'
                      ' SEARCH_ID=926d323df92a49279b49897910e64fac'
        }

    def get_one_page(self, pn=1):
        url = 'https://www.lagou.com/jobs/positionAjax.json'
        query = {
            'city': self.CITY,
            'isSchoolJob': 0,
            'needAddtionalResult': 'false'
        }
        form = {
            'first': 'true',
            'kd': self.KEYWORD,
            'pn': pn
        }
        try:
            response = session.post(url=url, params=query, data=form, headers=self.headers)
            if response.status_code == 200:
                return response
            return None
        except Exception as e:
            print(e)

    def parse_one_page(self, response):
        _ = self
        data = json.loads(response.text)
        if data:
            results = data.get('content').get('positionResult').get('result')
            for result in results:
                yield {
                    '公司名称': result.get('companyFullName') + '-' + result.get('companyShortName'),
                    '公司URL': 'https://www.lagou.com/gongsi/{}.html'.format(result.get('companyId')),
                    '公司规模': result.get('companySize'),
                    '公司发展': result.get('financeStage'),
                    '学历要求': result.get('education'),
                    '工作类型': result.get('jobNature'),
                    '职位URL': 'https://www.lagou.com/jobs/{}.html'.format(result.get('positionId')),
                    '职位名称': result.get('positionName'),
                    '职位福利': result.get('positionAdvantage'),
                    '工资': result.get('salary'),
                    '工作经验': result.get('workYear')
                }

    def get_position_detail(self, url):
        try:
            response = session.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            return None
        except Exception as e:
            print(e)

    def parse_position_detail(self, response):
        html = response.html
        description = html.find('.job_bt > div').text
        # description = html.xpath('dl#job_detail/dd.job_bt/div').text
        address = html.re()

    def main(self):
        print('第 1 页')
        response = self.get_one_page()
        for result in self.parse_one_page(response):
            pprint(result)

        data = json.loads(response.text)
        if data:
            count = data.get('content').get('positionResult').get('totalCount')//15 + 1
            print('共{}页'.format(count))

            for i in range(2, count + 1):

                time.sleep(3)

                print('第{}页'.format(i))
                response = self.get_one_page(pn=i)
                print(response.status_code)
                for result in self.parse_one_page(response):
                    pprint(result)


if __name__ == '__main__':
    spider = LagouSpider()
    spider.main()

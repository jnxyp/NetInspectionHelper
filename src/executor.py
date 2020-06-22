from pprint import pprint

from config import MAX_RETRY
from sites import SITES
from util import p


class Executor:
    def __init__(self, companies: list, included_sites: list = SITES):

        self.sites = included_sites
        self.companies = companies

        self.failed_sites = {company_name: list() for company_name in self.get_companies()}

    def get_companies(self) -> list:
        return self.companies

    def get_sites(self) -> list:
        return self.sites

    def execute(self):
        self.grab_all()
        self.print_failed_summary()

    def grab_all(self):
        p("开始从{}个页面抓取{}个公司的信息".format(len(self.get_sites()), len(self.get_companies())))
        for company_name in self.get_companies():
            p("\t开始抓取公司信息：{}".format(company_name))
            for site in self.get_sites():
                attempt = 1
                while attempt <= MAX_RETRY:
                    result = site.grab(company_name)
                    if result:
                        break
                    p("\t\t第{}次尝试失败".format(attempt))
                    attempt += 1
                if attempt > MAX_RETRY:
                    self.failed_sites[company_name].append(site)
                    p("\t放弃抓取页面")
            p("\t{} 相关信息抓取完成".format(company_name))

    def print_failed_summary(self):
        p("=" * 20)
        p("以下页面抓取失败：")
        pprint(self.failed_sites)




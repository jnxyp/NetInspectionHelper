from pprint import pprint

from config import MAX_RETRY
from document_generator import InspectionReport
from sites import SITES
from util import p


class Executor:
    def __init__(self, companies: list, included_sites: list = SITES):

        self.sites = included_sites
        self.companies = companies

        self.failed_sites = {company_name: list() for company_name in self.get_companies()}
        self.failed_reports = []

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
            p("\t{}".format(company_name))
            p("\t\t开始抓取公司信息".format(company_name))
            for site in self.get_sites():
                attempt = 1
                try:
                    while attempt <= MAX_RETRY:
                        result = site.grab(company_name)
                        if result:
                            break
                        p("\t\t第{}次尝试失败".format(attempt))
                        attempt += 1
                    if attempt > MAX_RETRY:
                        self.failed_sites[company_name].append(site.get_name())
                        p("\t放弃抓取页面")
                except NotImplementedError as e:
                    self.failed_sites[company_name].append(site.get_name())
                    p("\t\t\t" + repr(e))
            p("\t\t公司信息抓取完毕".format(company_name))
            p("\t\t开始生成报告".format(company_name))
            try:
                report = InspectionReport(company_name, self.get_sites())
                report.generate()
                report.save()
                p("\t\t√ 报告生成完毕".format(company_name))
            except Exception as e:
                p("\t\t× 报告生成失败".format(company_name))
                p("\t\t\t" + repr(e))
                self.failed_reports.append(company_name)
            p("\t{} 全部完成".format(company_name))

    def print_failed_summary(self):
        p("=" * 20)
        p("以下页面抓取失败：")
        pprint(self.failed_sites)
        p("以下报告生成失败：")
        pprint(self.failed_reports)

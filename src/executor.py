from pprint import pprint

from PIL import Image

from config import MAX_RETRY, SCREENSHOT_FILENAME_PAGE, SCREENSHOT_FILENAME_SCREEN, \
    SCREENSHOT_PAGE_TASKBAR_HEIGHT, SCREENSHOT_PAGE_TASKBAR_RESIZE_FACTOR, SCREENSHOT_PAGE_TASKBAR
from document_generator import InspectionReport
from sites import SITES, Site
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
            self.grab_sites(company_name)

            self.generate_report(company_name)

            p("\t{} 全部完成".format(company_name))

    def grab_sites(self, company_name: str):
        p("\t{}".format(company_name))
        p("\t\t开始抓取公司信息".format(company_name))
        for site in self.get_sites():
            attempt = 1
            try:
                while attempt <= MAX_RETRY:
                    result = site.grab(company_name)
                    if result:
                        if SCREENSHOT_PAGE_TASKBAR:
                            self.append_taskbar(company_name, site)
                        break
                    p("\t\t第{}次尝试失败".format(attempt))
                    attempt += 1
                if attempt > MAX_RETRY:
                    self.failed_sites[company_name].append(site.get_name())
                    p("\t放弃抓取页面")
            except Exception as e:
                self.failed_sites[company_name].append(site.get_name())
                p("\t\t\t" + repr(e))
        p("\t\t公司信息抓取完毕".format(company_name))

    def append_taskbar(self, company_name: str, site: Site):
        p("\t\t\t- 为页面截图添加任务栏")
        screen_shot_path_page = site.get_screenshot_file_name_full(company_name,
                                                                   SCREENSHOT_FILENAME_PAGE)
        screen_shot_path_screen = site.get_screenshot_file_name_full(company_name,
                                                                     SCREENSHOT_FILENAME_SCREEN)

        page = Image.open(screen_shot_path_page)
        screen = Image.open(screen_shot_path_screen)

        taskbar_height = int(SCREENSHOT_PAGE_TASKBAR_HEIGHT * SCREENSHOT_PAGE_TASKBAR_RESIZE_FACTOR)

        screen_width, screen_height = screen.size

        taskbar_image = screen.crop(
            (0, screen_height - taskbar_height, screen_width, screen_height))

        page_width, page_height = page.size

        resize_ratio = page_width / screen_width
        taskbar_image = taskbar_image.resize((page_width, int(taskbar_height * resize_ratio)))

        new_page = Image.new('RGBA', (page_width, page_height+taskbar_height))
        new_page.paste(page)
        new_page.paste(taskbar_image, (0, page_height))
        new_page.save(screen_shot_path_page)
        p("\t\t\t√ 添加完毕")

    def generate_report(self, company_name: str):
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

    def print_failed_summary(self):
        p("=" * 20)
        p("以下页面抓取失败：")
        pprint(self.failed_sites)
        p("以下报告生成失败：")
        pprint(self.failed_reports)

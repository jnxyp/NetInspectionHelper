import inspect
import os
import sys
import time
from abc import ABC
from os.path import join, exists

from mss import mss
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import ROOT_PATH, SCREENSHOT_PATH, SCREENSHOT_FILENAME, MONITOR_ID
from util import p


class Site(ABC):
    name = None  # type:str
    initial_url = None  # type:str
    site_id = None  # type:int

    def get_name(self) -> str:
        return self.name

    def get_initial_url(self, company_name: str) -> str:
        return self.initial_url.format(company_name=company_name)

    def get_id(self) -> int:
        return self.site_id

    def grab(self, company_name: str, monitor_id: int = MONITOR_ID) -> bool:
        screen_shot_path = SCREENSHOT_PATH.format(company_name=company_name)

        if not exists(screen_shot_path):
            os.makedirs(screen_shot_path)

        return self.take_screenshots(screen_shot_path=screen_shot_path, monitor_id=monitor_id,
                                     company_name=company_name)

    def take_screenshots(self, company_name: str, screen_shot_path: str,
                         monitor_id: int) -> bool:
        p("\t\t\t- " + self.get_name() + " 开始抓取...")
        screen_shot_path_full = join(screen_shot_path,
                                     SCREENSHOT_FILENAME.format(
                                         site_name=str(self.get_id()) + "-" + self.get_name(),
                                         file_name="full.png"))
        screen_shot_path_screen = join(screen_shot_path,
                                       SCREENSHOT_FILENAME.format(
                                           site_name=str(self.get_id()) + "-" + self.get_name(),
                                           file_name="screen.png"))
        driver = webdriver.Edge()
        try:
            ele = self.get_screenshot_element(company_name, driver)

            ele.screenshot(screen_shot_path_full)

            with mss() as sct:
                sct.shot(mon=monitor_id, output=screen_shot_path_screen)

            p("\t\t\t√ " + self.get_name() + " 抓取完成。")
            return True
        except Exception as e:
            p("\t\t\t× " + self.get_name() + " 抓取失败。")
            p("\t\t\t\t" + repr(e))
            return False
        finally:
            try:
                driver.quit()
            except WebDriverException as e:
                p("\t\t\t" + self.get_name() + "关闭驱动程序失败，窗口可能已被关闭。")
                p("\t\t\t\t" + repr(e))

    def get_screenshot_element(self, company_name: str, driver: WebDriver):
        driver.get(self.get_initial_url(company_name))
        driver.maximize_window()

        time.sleep(2)

        return driver.find_element_by_tag_name('body')

    def __str__(self):
        return self.get_name()


class SSE(Site):
    site_id = 1
    name = "上交所公司债券项目信息平台"
    initial_url = "http://bond.sse.com.cn/bridge/information/index_search.shtml?key={company_name}"

    def get_screenshot_element(self, company_name: str, driver: WebDriver):
        driver.get(self.get_initial_url(company_name))
        driver.maximize_window()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#zeroRecordDiv_js_search, .tr_odd'))
        )

        return driver.find_element_by_tag_name('body')


class SZSE(Site):
    site_id = 2
    name = "深交所固收信息平台"
    initial_url = "http://bond.szse.cn/application/search/index.html?keyword={company_name}"


class KQ(Site):
    site_id = 3
    name = "孔雀开屏系统"
    initial_url = "http://zhuce.nafmii.org.cn/fans/publicQuery/manager"

    def get_screenshot_element(self, company_name: str, driver: WebDriver):
        driver.get(self.get_initial_url(company_name))
        driver.maximize_window()

        time.sleep(5)

        text_input = driver.find_element_by_id('regFileName')
        text_input.send_keys(company_name)

        search_button = driver.find_element_by_id('bn_search')
        search_button.click()

        time.sleep(1.5)

        return driver.find_element_by_tag_name('body')


class SHC(Site):
    site_id = 4
    name = "上海清算所"
    initial_url = "https://www.shclearing.com/shchapp/pages/client/search/information_disclosure.jsp"

    def get_screenshot_element(self, company_name: str, driver: WebDriver):
        driver.get(self.get_initial_url(company_name))
        driver.maximize_window()

        time.sleep(1)

        text_input = driver.find_element_by_id('organ')
        text_input.send_keys(company_name)

        search_button = driver.find_element_by_id('button')
        search_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#oragns td[align="right"]'))
        )

        return driver.find_element_by_tag_name('body')


class BAIDU(Site):
    site_id = 6
    name = "百度"
    initial_url = "https://baike.baidu.com/item/{company_name}"


class MEM(Site):
    site_id = 16
    name = "国家应急管理部网站"
    initial_url = "https://www.mem.gov.cn/was5/web/sousuo/index.html?sw={company_name}"


class MEE(Site):
    site_id = 17
    name = "国家生态环境部网站"
    initial_url = "http://www.mee.gov.cn/qwjs2019/?orsen=&andsen=&total={company_name}&exclude=&orderby=-docreltime&datetimepicker=&timestart=&datetimepicker=&timeend=&searchscope="


class MIIT(Site):
    site_id = 18
    name = "国家工信部网站"
    initial_url = "http://www.miit.gov.cn/Searchweb/news.jsp"

    def get_screenshot_element(self, company_name: str, driver: WebDriver):
        driver.get(self.get_initial_url(company_name))
        driver.maximize_window()

        time.sleep(1)

        text_input = driver.find_element_by_id('fullText')
        text_input.send_keys(company_name)
        text_input.send_keys(Keys.RETURN)

        time.sleep(4)

        return driver.find_element_by_tag_name('body')


class SAFE(Site):
    site_id = 19
    name = "国家外汇管理局网站"
    initial_url = "http://www.safe.gov.cn/safe/search/index.html?q={company_name}&siteid=safe&order=releasetime"


class NDRC(Site):
    site_id = 20
    name = "国家发改委网站"
    initial_url = "https://so.ndrc.gov.cn/s?qt=\"{company_name}\"&siteCode=bm04000007"


class PBC(Site):
    site_id = 21
    name = "中国人民银行"
    initial_url = "http://wzdig.pbc.gov.cn:8080/search/pcRender?pageId=d55d03ab47b14e86879d1993e8a0ff7c"

    def get_screenshot_element(self, company_name: str, driver: WebDriver):
        driver.get(self.get_initial_url(company_name))
        driver.maximize_window()

        text_input1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        text_input1.send_keys(company_name)
        text_input2 = driver.find_element_by_css_selector(
            '#adv_query_form > table > tbody > tr:nth-child(3) > td:nth-child(3) > input')
        text_input2.send_keys(company_name)

        button = driver.find_element_by_id('button')
        button.click()

        time.sleep(5)

        return driver.find_element_by_tag_name('body')


class CSRC(Site):
    site_id = 22
    name = "中国证监会网站"
    initial_url = "http://www.csrc.gov.cn/pub/newsite/"

    def get_screenshot_element(self, company_name: str, driver: WebDriver):
        # todo: slow page loading
        driver.get(self.get_initial_url(company_name))
        driver.maximize_window()

        text_input = driver.find_element_by_id("schword")
        text_input.clear()
        text_input.send_keys(company_name)
        driver.find_element_by_css_selector("input.so_btn[type='submit']").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.tishi > span'))
        )

        return driver.find_element_by_tag_name('body')


class CBIRC(Site):
    site_id = 23
    # todo: slow page loading
    name = "中国银保监会网站"
    initial_url = "http://www.cbirc.gov.cn/cn/view/pages/index/jiansuo.html?keyWords={company_name}"


class SAMR(Site):
    site_id = 24
    # todo: slow page loading
    name = "国家市场监督管理总局网站"
    initial_url = "http://www.samr.gov.cn/so/s?qt={company_name}&x=14&y=13&token=849&siteCode=bm30000012"

    def get_screenshot_element(self, company_name: str, driver: WebDriver):
        driver.get(self.get_initial_url(company_name))
        driver.maximize_window()

        return driver.find_element_by_tag_name('html')


class MOA(Site):
    site_id = 25
    name = "国家农业农村部网站"
    initial_url = "http://www.moa.gov.cn/was5/web/search?searchword={company_name}&channelid=233424&orderby=-DOCRELTIME"


class STATS(Site):
    site_id = 26
    name = "国家统计局网站"
    initial_url = "http://www.stats.gov.cn/was5/web/search?channelid=288041&andsen={company_name}"


class NEA(Site):
    site_id = 27
    name = "国家能源局网站"
    initial_url = "http://so.news.cn/was5/web/search?channelid=229767&searchword={company_name}"


class MOF(Site):
    site_id = 28
    name = "国家财政部网站"
    initial_url = "http://www.mof.gov.cn/index.htm"

    def get_screenshot_element(self, company_name: str, driver: WebDriver):
        driver.get(self.get_initial_url(company_name))
        driver.maximize_window()

        text_input = driver.find_element_by_id("swd")
        text_input.clear()
        text_input.send_keys(company_name)

        driver.execute_script('goSearch(0)')

        driver.switch_to.window(driver.window_handles[1])

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.paixubox'))
        )

        return driver.find_element_by_tag_name('body')


class CCGP(Site):
    site_id = 29
    name = "中国政府采购网"
    initial_url = "http://search.ccgp.gov.cn/znzxsearch?searchtype=1&page_index=1&searchchannel=0&kw={company_name}&start_time=&end_time=&timeType=0"


class MNR(Site):
    site_id = 30
    name = "中华人民共和国自然资源部"
    initial_url = "http://s.lrn.cn/jsearchfront/search.do?websiteid=110000000000000&pg=1&p=1&searchid=1&tpl=13&cateid=1&q={company_name}&filter=001&x=14&y=20"


class CE(Site):
    site_id = 31
    name = "信用能源网"
    initial_url = "http://www.creditenergy.gov.cn/report/search?name={company_name}&type="


class MOHURD(Site):
    site_id = 32
    name = "全国建筑市场监管公共服务平台"
    initial_url = "http://jzsc.mohurd.gov.cn/data/company?complexname={company_name}"


class BEIAN(Site):
    site_id = 33
    name = "工业和信息化部 ICP IP 地址 域名信息备案管理系统"
    initial_url = "http://beian.miit.gov.cn/"


SITES = [SSE(),
         SZSE(),
         KQ(),
         SHC(),
         BAIDU(),
         MEM(),
         MEE(),
         MIIT(),
         SAFE(),
         NDRC(),
         PBC(),
         CSRC(),
         CBIRC(),
         SAMR(),
         MOA(),
         STATS(),
         NEA(),
         MOF(),
         CCGP(),
         MNR(),
         CE(),
         MOHURD(),
         BEIAN(), ]

SITES_BY_NAME = {
    s.get_name(): s for s in SITES
}

SITES_BY_ID = {
    s.get_id(): s for s in SITES
}

if __name__ == '__main__':
    # print(SITES)
    # company_name = "常高新集团有限公司"
    # for s in SITES:
    #     s.grab(company_name)
    pass
    # print(SITES_BY_ID.keys())

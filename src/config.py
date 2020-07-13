import json
from os.path import dirname, abspath, join

from docx.shared import Mm
from selenium import webdriver

DEBUG = True
ROOT_PATH = dirname(abspath(__file__))

CONFIG = {
  "screenshots": {
    "page": True,
    "screen": True
  }
}

with open('config.json') as f:
    CONFIG = json.load(f)

# 截图选用的显示器，1为主显示器
MONITOR_ID = 1

# 截图输出文件路径和文件名格式
SCREENSHOT_PATH = join(ROOT_PATH, 'screenshots', '{company_name}')
SCREENSHOT_FILENAME = '{site_name}_{file_name}'

SCREENSHOT_FILENAME_SCREEN = 'screen.png'
SCREENSHOT_FILENAME_PAGE = 'page.png'

SCREENSHOT_TAKE_SCREEN = CONFIG['screenshots']['screen']
SCREENSHOT_TAKE_PAGE = CONFIG['screenshots']['page']

# 报告输出文件路径和文件名格式
REPORT_PATH = join(ROOT_PATH, 'reports')
REPORT_FILENAME = '{company_name}.docx'

# 报告页面大小 297*210mm = A4
REPORT_PAGE_HEIGHT = Mm(297)
REPORT_PAGE_WIDTH = Mm(210)

REPORT_FONT_NAME = '宋体'
REPORT_IMAGE_WIDTH = Mm(140)

# 配置文件路径
COMPANY_NAME_FILE_PATH = join(ROOT_PATH, 'company_names.txt')
INCLUDED_SITES_FILE_PATH = join(ROOT_PATH, 'included_sites.txt')

# 抓取失败后的最大重试次数
MAX_RETRY = 3

# 浏览器类型及驱动路径
# Edge Legacy
# WEBDRIVER = webdriver.Edge
# WEBDRIVER_PATH = 'MicrosoftWebDriver.exe'

# Edge 83.0.478.54
WEBDRIVER = webdriver.Edge
WEBDRIVER_PATH = join(ROOT_PATH, 'msedgedriver_83.0.478.54.exe')

if __name__ == '__main__':
    print(SCREENSHOT_PATH)

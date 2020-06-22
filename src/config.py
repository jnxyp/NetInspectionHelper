from os.path import dirname, abspath, join

from selenium import webdriver

DEBUG = True
ROOT_PATH = dirname(abspath(__file__))

# 截图选用的显示器，1为主显示器
MONITOR_ID = 1

# 截图输出文件路径和文件名格式
SCREENSHOT_PATH = join(ROOT_PATH, 'screenshots', '{company_name}')
SCREENSHOT_FILENAME = '{site_name}_{file_name}'

# 配置文件路径
COMPANY_NAME_FILE_PATH = join(ROOT_PATH, 'company_names.txt')
INCLUDED_SITES_FILE_PATH = join(ROOT_PATH, 'included_sites.txt')

# 抓取失败后的最大重试次数
MAX_RETRY = 3

# 浏览器类型及驱动路径
# WEBDRIVER = webdriver.Chrome
WEBDRIVER = webdriver.Edge
# WEBDRIVER_PATH = join(ROOT_PATH, 'msedgedriver.exe')
WEBDRIVER_PATH = 'MicrosoftWebDriver.exe'

if __name__ == '__main__':
    print(ROOT_PATH)
    print(SCREENSHOT_PATH)
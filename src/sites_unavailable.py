
# class GSXT(Site):
#     def get_name(self) -> str:
#         return "全国企业信用信息公示系统"
#
#     def grab(self, company_name: str, monitor_id: int = 1):
#         screen_shot_path = self.get_screenshot_path(company_name)
#
#         if not exists(screen_shot_path):
#             os.makedirs(screen_shot_path)
#
#         url = "http://www.gsxt.gov.cn/index.html"
#
#         self.company_name = company_name
#         self.take_screenshots(url=url, screen_shot_path=screen_shot_path, monitor_id=monitor_id,
#                               company_name=company_name)
#
#     def get_screenshot_element(self, url: str, company_name: str, driver: WebDriver):
#         driver.get(url)
#         driver.maximize_window()
#
#         time.sleep(1)
#
#         text_input = driver.find_element_by_id('keyword')
#         text_input.send_keys(company_name)
#         text_input.send_keys(Keys.RETURN)
#
#         first_result = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located(
#                 (By.CSS_SELECTOR, '#advs > div > div:nth-child(2) > a:nth-child(1)'))
#         )
#
#         detail_url = first_result.get_attribute('href')
#         driver.get(detail_url)
#
#         time.sleep(2)
#
#         return driver.find_element_by_class_name('container')


# class CreditChina(Site):
#     def get_name(self) -> str:
#         return "信用中国"
#
#     def grab(self, company_name: str, monitor_id: int = 1):
#         screen_shot_path = self.get_screenshot_path(company_name)
#
#         if not exists(screen_shot_path):
#             os.makedirs(screen_shot_path)
#
#         url = "https://www.creditchina.gov.cn/home/index.html"
#
#         self.company_name = company_name
#         self.take_screenshots(url=url, screen_shot_path=screen_shot_path, monitor_id=monitor_id,
#                               company_name=company_name)
#
#     def take_screenshots(self, url: str, company_name: str, screen_shot_path: str,
#                          monitor_id: int = 1):
#         screen_shot_path_full = join(screen_shot_path, "full.png")
#         screen_shot_path_screen = join(screen_shot_path, "screen.png")
#         driver = webdriver.Edge()
#         try:
#             driver.get(url)
#             driver.maximize_window()
#
#             text_input = WebDriverWait(driver, 200).until(
#                 EC.presence_of_element_located(
#                     (By.CSS_SELECTOR, '#search_input'))
#             )
#
#             text_input.send_keys(company_name)
#             text_input.send_keys(Keys.RETURN)
#
#             driver.switch_to.window(driver.window_handles[1])
#
#             first_result = WebDriverWait(driver, 200).until(
#                 EC.presence_of_element_located(
#                     (By.CSS_SELECTOR, '#companylists > li > p.company-name'))
#             )
#             first_result.click()
#
#             driver.switch_to.window(driver.window_handles[2])
#
#             time.sleep(3)
#
#             ele = driver.find_element_by_class_name('wrapper')
#             ele.screenshot(screen_shot_path_full)
#
#             with mss() as sct:
#                 sct.shot(mon=monitor_id, output=screen_shot_path_screen)
#         except Exception as e:
#             print(e)
#         finally:
#             driver.quit()

# class SIPO(Site):
#     def __init__(self):
#         super().__init__("中国专利公布公告", "http://epub.sipo.gov.cn/index.action")
#
#     def get_screenshot_element(self, company_name: str, driver: WebDriver):
#         driver.get(self.get_initial_url(company_name))
#         driver.maximize_window()
#
#         text_input = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, '#soso_text'))
#         )
#         text_input.clear()
#         text_input.send_keys(company_name)
#
#         driver.execute_script('patqs()')
#
#         time.sleep(5)
#
#         return driver.find_element_by_tag_name('body')


# class CUSTOMS(Site):
#     def __init__(self):
#         super().__init__("海关总署", "http://www.customs.gov.cn/")
#
#     def get_screenshot_element(self, company_name: str, driver: WebDriver):
#         driver.get(self.get_initial_url(company_name))
#         driver.maximize_window()
#
#         text_input1 = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, '#ess_ctr151088_ListC_Info_ctl00_KEYWORDS'))
#         )
#
#         text_input1.send_keys(company_name)
#         driver.execute_script('onFullTextSearchLinkClick()')
#
#         driver.switch_to.window(driver.window_handles[1])
#
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, 'span.result-count'))
#         )
#
#         return driver.find_element_by_tag_name('huilan-amj-page-container')

# class CTAX_JS(Site):
#     site_id = 37
#     name = "国家税务总局江苏省税务局网站"
#     initial_url = "https://jiangsu.chinatax.gov.cn/jsearchfront/search.do?websiteid=320000000000000&searchid=21&pg=&p=1&tpl=22&q={company_name}&pq={company_name}&oq=&eq=&pos=&sortType=&begin=&end="
#
#     @classmethod
#     def get_screenshot_element(cls, company_name: str, driver: WebDriver):
#         driver.get(cls.get_initial_url(company_name))
#         driver.maximize_window()
#
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, 'div.con_left'))
#         )
#
#         return driver.find_element_by_tag_name('body')
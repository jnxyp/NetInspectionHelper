from os.path import dirname, abspath, join

DEBUG = True
ROOT_PATH = dirname(dirname(abspath(__file__)))
SCREENSHOT_PATH = join(ROOT_PATH, 'screenshots', '{company_name}')
SCREENSHOT_FILENAME = '{site_name}_{file_name}'

MAX_RETRY = 3

if __name__ == '__main__':
    print(ROOT_PATH)
    print(SCREENSHOT_PATH)
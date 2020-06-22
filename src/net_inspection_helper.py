from os.path import join, exists

from config import COMPANY_NAME_FILE_PATH, INCLUDED_SITES_FILE_PATH
from executor import Executor
from sites import SITES_BY_ID
from util import read_file

if __name__ == '__main__':

    company_names = [s.rstrip() for s in read_file(COMPANY_NAME_FILE_PATH) if s != '']
    included_sites = [SITES_BY_ID[int(x)] for x in read_file(INCLUDED_SITES_FILE_PATH) if x != '']

    exe = Executor(company_names, included_sites)
    exe.execute()

    input("按任意键退出。")
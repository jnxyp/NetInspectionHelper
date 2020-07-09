from os.path import join, exists

from config import COMPANY_NAME_FILE_PATH, INCLUDED_SITES_FILE_PATH
from document_generator import InspectionReport
from executor import Executor
from sites import SITES_BY_ID
from util import read_file, p

if __name__ == '__main__':

    try:
        company_names = [s.rstrip() for s in read_file(COMPANY_NAME_FILE_PATH) if s != '']
        included_sites = [SITES_BY_ID[int(x)] for x in read_file(INCLUDED_SITES_FILE_PATH) if
                          x != '']

        exe = Executor(company_names, included_sites)
        exe.execute()
    except Exception as e:
        p('出现错误，请将下方报错信息反馈给开发者')
        p(repr(e))


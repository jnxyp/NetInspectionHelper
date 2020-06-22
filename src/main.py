from executor import Executor

if __name__ == '__main__':
    company_names = [
        '常高新集团有限公司',
    ]

    exe = Executor(company_names)
    exe.execute()
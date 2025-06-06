import sys
from reports import *

# python main.py data1.csv data2.csv data3.csv --report output

if __name__ == "__main__":
    report_type = sys.argv[sys.argv.index('--report') + 1]
    csv_files = sys.argv[1:sys.argv.index('--report')]
    if report_type == "payout":
        pr = PayoutReport(csv_files)
        pr.export('payout.json')
        print(pr)
    else:
        print('Такой тип отчёта не был добавлен')
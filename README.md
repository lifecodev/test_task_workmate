# Скрипт для формирования отчёта по зарплатам сотрудников и его конвертации в json формат
Пример вывода отчёта в консоль
<p align="center"><img src="https://github.com/lifecodev/test_task_workmate/blob/master/img.png?raw=true" width="1000px"></p>

## Как добавить новые отчёты?
Чтобы добавить новый отчёт можно наследовать класс Report
пример:
```python
class PayoutReport(Report): # Уже существующий класс PayoutReport для формирования отчёта по зарплатам
    def __init__(self, csv_name: str | list, header=None, separator: str = ','):
        if header is None:
            header = ["id", "email", "name", "department", "hours_worked", ["hourly_rate", "rate", "salary"]]
        # Можно добавить сразу же заголовок данных.
        # Вложенный список нужен для обхвата разных названий столбцов в csv в один
        super().__init__(csv_name, header, separator)

        self.report_type = "Payout"
        self.payout()

    def payout(self): # Можно написать свою функцию
        data = []
        hours = self.get_column('hours_worked')
        salary = self.get_column('salary')

        for hours_el, salary_el in zip(hours, salary):
            data.append(f'${int(hours_el) * int(salary_el)}')

        self.add_column('payout', data)
```
Также стоит отредактировать main.py
```python
if report_type == "payout":
  pr = PayoutReport(csv_files)
  pr.export('payout.json')
  print(pr)
elif report_type == "ваше-название":
  ...
else:
  print('Такой тип отчёта не был добавлен')
```

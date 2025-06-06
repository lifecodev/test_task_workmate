# Основной класс для формирования репортов
import datetime
import json

from exceptiongroup import catch


class Report:
    def __init__(self, csv_name: str | list, header: list, separator: str = ','):
        self.sep = separator
        self.header = header
        self.rows = []

        self.report_type = "Default"

        if isinstance(csv_name, str):
            self._read(csv_name)
        elif isinstance(csv_name, list):
            for name in csv_name:
                self._read(name)

    # Чтение csv файла и его "обработка"
    def _read(self, csv_name):
        column_ids = []
        try:
            with open(csv_name, "r", encoding='utf-8') as file:
                line = file.readline()
                line = line.strip()
                columns = line.split(self.sep)
                for target in columns:
                    if target in self.header:
                        column_ids.append(self.header.index(target))
                    else:
                        for header_item in self.header:
                            if isinstance(header_item, list):
                                if target in header_item:
                                    column_ids.append(self.header.index(header_item))

                for line in file:
                    line = line.strip()
                    data = line.split(self.sep)
                    row = [-1] * len(data)
                    for i in range(0, len(data)):
                        index_data = column_ids[i]
                        if data[i].isdigit():
                            row[index_data] = int(data[i])
                        else:
                            row[index_data] = data[i]
                    self.rows.append(row)
        except Exception as e:
            print(f'Ошибка: {e}')

    def add_column(self, column_name: str | list, data: list):
        self.header.append(column_name)
        for index, row in enumerate(self.rows):
            if len(data) - 1 < index:
                row.append(None)
            else:
                row.append(data[index])

    def add_row(self, data: list):
        if len(data) == len(self.header):
            self.rows.append(data)
        else:
            raise Exception('Количество добавляемых данных меньше или больше!')

    def get_row(self, index_row):
        try:
            return self.rows[index_row]
        except Exception as e:
            print(f'Ошибка: {e}')

    def get_rows_by_key(self, key, data):
        is_exists = False
        col_index = -1
        if key in self.header:
            is_exists = True
            col_index = self.header.index(key)
        else:
            for header_item in self.header:
                if isinstance(header_item, list):
                    if key in header_item:
                        is_exists = True
                        col_index = self.header.index(header_item)

        if is_exists is True:
            rows = []
            for row in self.rows:
                if row[col_index] == data:
                    rows.append(row)
            return rows
        else:
            raise Exception(f'Не найдено название столбца {key} в таблице!')

    def get_column(self, column_name: str):
        index = None
        if column_name in self.header:
            index = self.header.index(column_name)
        else:
            for header_item in self.header:
                if isinstance(header_item, list):
                    if column_name in header_item:
                        index = self.header.index(header_item)

        if index is not None:
            data = []
            for row in self.rows:
                data.append(row[index])
            return data
        else:
            raise Exception("Название столбца не было найдено!")

    def export(self, path):
        report_obj = {
            'type': self.report_type,
            'date': datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            'report_data': []
        }

        data = []
        key_header = []
        for header in self.header:
            if isinstance(header, list):
                key_header.append(header[0])
            elif isinstance(header, str):
                key_header.append(header)
            else:
                raise Exception('В заголовке таблицы некорректный тип данных!')

        for row in self.rows:
            json_obj = {}
            for index, row_data in enumerate(row):
                json_obj.__setitem__(key_header[index], row_data)
            data.append(json_obj)

        report_obj['report_data'] = data

        try:
            with open(path, "w+", encoding='utf-8') as file:
                file.write(json.dumps(report_obj, indent=4))
        except (PermissionError, FileNotFoundError) as e:  # Ошибки доступа/пути
            print(f"Ошибка записи файла: {e}")
        except TypeError as e:  # Если report_obj содержит несериализуемые данные
            print(f"Ошибка сериализации JSON: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
        return report_obj

    # Строковое представление данных
    def __str__(self):
        text = ''
        data_header = []
        for el in self.header:
            if not isinstance(el, list):
                data_header.append(el)
            else:
                data_header.append(el[0])

        widths = [len(h) for h in data_header]
        for row in self.rows:
            for i, item in enumerate(row):
                widths[i] = max(widths[i], len(str(item)))

        # Создаем формат строки
        header_format = "  ".join(f"{{:<{w}}}" for w in widths)
        f_format = []
        for width in widths:
            f_format.append(f"{{:>{width}}}")

        row_format = "  ".join(f_format)

        text += header_format.format(*data_header) + '\n'
        text += "-" * (sum(widths) + len(widths) * 2) + '\n'
        for row in self.rows:
            text += row_format.format(*row) + '\n'
        return text



# Репорт с опцией ЗП
class PayoutReport(Report):
    def __init__(self, csv_name: str | list, header=None, separator: str = ','):
        if header is None:
            header = ["id", "email", "name", "department", "hours_worked", ["hourly_rate", "rate", "salary"]]
        super().__init__(csv_name, header, separator)

        self.report_type = "Payout"
        self.payout()

    def payout(self):
        data = []
        hours = self.get_column('hours_worked')
        salary = self.get_column('salary')

        for hours_el, salary_el in zip(hours, salary):
            data.append(f'${int(hours_el) * int(salary_el)}')

        self.add_column('payout', data)

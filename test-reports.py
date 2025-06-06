from reports import Report, PayoutReport
import pytest

class TestReport:
    @pytest.fixture
    def report(self):
        csv_names = ['data1.csv']

        return Report(
            csv_names,
            ["id", "email", "name", "department", "hours_worked", ["hourly_rate", "rate", "salary"]]
        )

    def test_read(self, report):
        test_rows = [
            [1, "alice@example.com", "Alice Johnson", "Marketing", 160, 50],
            [2,"bob@example.com","Bob Smith","Design",150,40],
            [3,"carol@example.com","Carol Williams","Design",170,60]
        ]
        test_report = Report('data1.csv',
                             ["id", "email", "name", "department", "hours_worked", ["hourly_rate", "rate", "salary"]])
        assert report.rows == test_rows
        assert test_report.rows == test_rows

    def test_add_column(self, report):
        test_rows = [
            [1, "alice@example.com", "Alice Johnson", "Marketing", 160, 50, 1],
            [2, "bob@example.com", "Bob Smith", "Design", 150, 40, 1],
            [3, "carol@example.com", "Carol Williams", "Design", 170, 60, None]
        ]

        test_data = [1,1]
        report.add_column('test_data', test_data)
        assert report.rows == test_rows
        assert report.header[-1] == 'test_data'

    def test_add_row(self, report):
        test_rows = [
            [1, "alice@example.com", "Alice Johnson", "Marketing", 160, 50],
            [2, "bob@example.com", "Bob Smith", "Design", 150, 40],
            [3, "carol@example.com", "Carol Williams", "Design", 170, 60],
            [4, "a", "a", "a", 5, 5]
        ]
        report.add_row([4, "a", "a", "a", 5, 5])
        assert report.rows == test_rows
        with pytest.raises(Exception):
            report.add_row([4, "a"])

    def test_get_row(self, report):
        assert report.get_row(1) == [2, "bob@example.com", "Bob Smith", "Design", 150, 40]

    def test_get_rows_by_key(self, report):
        assert report.get_rows_by_key('id', 1) == [[1, "alice@example.com", "Alice Johnson", "Marketing", 160, 50]]
        assert report.get_rows_by_key('department', 'Design') == [
            [2, "bob@example.com", "Bob Smith", "Design", 150, 40],
            [3, "carol@example.com", "Carol Williams", "Design", 170, 60]
        ]
        assert report.get_rows_by_key('salary', 40) == [
            [2, "bob@example.com", "Bob Smith", "Design", 150, 40]
        ]

    def test_get_column(self, report):
        test_result = ["alice@example.com", "bob@example.com", "carol@example.com"]
        test_result_2 = [50, 40, 60]
        assert report.get_column('email') == test_result
        assert report.get_column('hourly_rate') == test_result_2
        assert report.get_column('salary') == test_result_2
        with pytest.raises(Exception):
            report.get_column("abc")

    def test_export(self, report):
        export = report.export('./test-default-report.json')
        test_export_data = [{
            "id": 1,
            "email": "alice@example.com",
            "name": "Alice Johnson",
            "department": "Marketing",
            "hours_worked": 160,
            "hourly_rate": 50
        },
        {
            "id": 2,
            "email": "bob@example.com",
            "name": "Bob Smith",
            "department": "Design",
            "hours_worked": 150,
            "hourly_rate": 40
        },
        {
            "id": 3,
            "email": "carol@example.com",
            "name": "Carol Williams",
            "department": "Design",
            "hours_worked": 170,
            "hourly_rate": 60
        }]

        assert export['type'] == 'Default'
        assert export['report_data'] == test_export_data
        with pytest.raises(Exception):
            report.header[-1] = {'a':'c'}
            report.export('./test-default-report.json')

    def test_str(self, report):
        test = str(report)
        test_text = """id  email              name            department  hours_worked  hourly_rate
------------------------------------------------------------------------------
 1  alice@example.com   Alice Johnson   Marketing           160           50
 2    bob@example.com       Bob Smith      Design           150           40
 3  carol@example.com  Carol Williams      Design           170           60\n"""
        print(test_text, test)
        assert type(test) == str
        assert test == test_text


class TestPayoutReport:
    @pytest.fixture
    def report(self):
        csv_names = ['data1.csv', 'data2.csv', 'data3.csv']
        return PayoutReport(csv_names)

    def test_init (self, report):
        assert report.header == ["id", "email", "name", "department", "hours_worked", ["hourly_rate", "rate", "salary"], "payout"]
        assert report.report_type == "Payout"

    def test_payout(self, report):
        test_data = ["$8000", "$6000", "$10200", "$7200", "$5250", "$6004", "$8250", "$6510", "$5920"]
        print(report.get_column('payout'))
        assert report.get_column('payout') == test_data

    def test_export(self, report):
        export = report.export('test-payout.json')
        test_report_data = [
            {
                "id": 1,
                "email": "alice@example.com",
                "name": "Alice Johnson",
                "department": "Marketing",
                "hours_worked": 160,
                "hourly_rate": 50,
                "payout": "$8000"
            },
            {
                "id": 2,
                "email": "bob@example.com",
                "name": "Bob Smith",
                "department": "Design",
                "hours_worked": 150,
                "hourly_rate": 40,
                "payout": "$6000"
            },
            {
                "id": 3,
                "email": "carol@example.com",
                "name": "Carol Williams",
                "department": "Design",
                "hours_worked": 170,
                "hourly_rate": 60,
                "payout": "$10200"
            },
            {
                "id": 101,
                "email": "grace@example.com",
                "name": "Grace Lee",
                "department": "HR",
                "hours_worked": 160,
                "hourly_rate": 45,
                "payout": "$7200"
            },
            {
                "id": 102,
                "email": "henry@example.com",
                "name": "Henry Martin",
                "department": "Marketing",
                "hours_worked": 150,
                "hourly_rate": 35,
                "payout": "$5250"
            },
            {
                "id": 103,
                "email": "ivy@example.com",
                "name": "Ivy Clark",
                "department": "HR",
                "hours_worked": 158,
                "hourly_rate": 38,
                "payout": "$6004"
            },
            {
                "id": 201,
                "email": "karen@example.com",
                "name": "Karen White",
                "department": "Sales",
                "hours_worked": 165,
                "hourly_rate": 50,
                "payout": "$8250"
            },
            {
                "id": 202,
                "email": "liam@example.com",
                "name": "Liam Harris",
                "department": "HR",
                "hours_worked": 155,
                "hourly_rate": 42,
                "payout": "$6510"
            },
            {
                "id": 203,
                "email": "mia@example.com",
                "name": "Mia Young",
                "department": "Sales",
                "hours_worked": 160,
                "hourly_rate": 37,
                "payout": "$5920"
            }
        ]
        assert export['type'] == "Payout"
        assert export['report_data'] == test_report_data



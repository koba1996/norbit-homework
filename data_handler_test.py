import unittest
import data_handler
from decimal import Decimal

class DataHandlerTest(unittest.TestCase):

    def test_0_read_file_not_exists(self):
        invalid_filename = "file-not-exists.txt"
        expected_outcome = []
        actual_result = data_handler.read_from_file(invalid_filename)
        self.assertEqual(expected_outcome, actual_result)

    
    def test_1_read_sonar_data_not_exists(self):
        invalid_filename = "sonar-data-not-exists.txt"
        start_time = 0
        expected_outcome = []
        actual_result = data_handler.read_sonar_data(invalid_filename, start_time)
        self.assertEqual(expected_outcome, actual_result)

    
    def test_2_read_regular_data_not_exists(self):
        invalid_filename = "invalid-filename.txt"
        start_time = 0
        frequency = 0
        headers = []
        expected_outcome = []
        actual_result, invalid_data = data_handler.read_data(invalid_filename, start_time, frequency, headers)
        self.assertEqual(expected_outcome, actual_result)


    def test_3_read_regular_data_not_exists(self):
        invalid_filename = "invalid-filename.txt"
        start_time = 0
        frequency = 0
        headers = []
        expected_outcome = True
        data, actual_result = data_handler.read_data(invalid_filename, start_time, frequency, headers)
        self.assertEqual(expected_outcome, actual_result)


    def test_4_format_regular_data_missing_header(self):
        one_line_of_data = [1, 2, 3]
        time = 0
        headers = ["first_header", "second_header"]
        expected_outcome = {}
        actual_result = data_handler.format_data(one_line_of_data, time, headers)
        self.assertEqual(expected_outcome, actual_result)


    def test_5_format_regular_data_missing_data(self):
        one_line_of_data = [1, 2]
        time = 0
        headers = ["first_header", "second_header", "third_header"]
        expected_outcome = {}
        actual_result = data_handler.format_data(one_line_of_data, time, headers)
        self.assertEqual(expected_outcome, actual_result)


    def test_6_format_regular_data_invalid_data(self):
        one_line_of_data = ["not_number"]
        time = 0
        headers = ["header"]
        expected_outcome = {}
        actual_result = data_handler.format_data(one_line_of_data, time, headers)
        self.assertEqual(expected_outcome, actual_result)


    def test_7_format_regular_data_valid_data(self):
        one_line_of_data = [1]
        time = 0
        headers = ["header"]
        expected_outcome = {
            "time": 0,
            "header": Decimal(1)
        }
        actual_result = data_handler.format_data(one_line_of_data, time, headers)
        self.assertEqual(expected_outcome, actual_result)


    def test_8_format_sonar_data_invalid_timestamp(self):
        one_line_of_data = ["timestamp", "1,1", "2,2"]
        time_diff = 0
        expected_outcome = {}
        actual_result = data_handler.format_sonar_data(one_line_of_data, time_diff)
        self.assertEqual(expected_outcome, actual_result)


    def test_9_format_sonar_data_valid_timestamp(self):
        one_line_of_data = [1, "1,1", "2,2"]
        time_diff = 0
        expected_outcome = Decimal(1)
        actual_result = data_handler.format_sonar_data(one_line_of_data, time_diff)["time"]
        self.assertEqual(expected_outcome, actual_result)


    def test_10_format_sonar_data_invalid_first_data(self):
        one_line_of_data = [1, "not_number,1", "2,2"]
        time_diff = 0
        expected_outcome = [{
            "angle": Decimal(2),
            "sample_index": Decimal(2) 
        }]
        actual_result = data_handler.format_sonar_data(one_line_of_data, time_diff)["angle_index_pairs"]
        self.assertEqual(expected_outcome, actual_result)


    def test_11_format_sonar_data_missing_separator(self):
        one_line_of_data = [1, "11", "2,2"]
        time_diff = 0
        expected_outcome = [{
            "angle": Decimal(2),
            "sample_index": Decimal(2) 
        }]
        actual_result = data_handler.format_sonar_data(one_line_of_data, time_diff)["angle_index_pairs"]
        self.assertEqual(expected_outcome, actual_result)


    def test_12_format_sonar_data_valid_data(self):
        one_line_of_data = [1, "1,1", "2,2"]
        time_diff = 0
        expected_outcome = [{
            "angle": Decimal(1),
            "sample_index": Decimal(1)
        },
        {
            "angle": Decimal(2),
            "sample_index": Decimal(2) 
        }]
        actual_result = data_handler.format_sonar_data(one_line_of_data, time_diff)["angle_index_pairs"]
        self.assertEqual(expected_outcome, actual_result)


    def test_13_extend_sonar_data_no_lines_skipped(self):
        sonar_data = [{
            "time": Decimal(1)
        }]
        other_data = [{
            "time": Decimal(0),
            "data": "should not connect"
        }, {
            "time": Decimal(100),
            "data": "should connect"
        }]
        headers = ["data"]
        frequency = 1
        expected_result = [{
            "time": Decimal(1),
            "data": "should connect"
        }]
        actual_result = data_handler.extend_sonar_data(sonar_data, other_data, headers, frequency)
        self.assertEqual(expected_result, actual_result)


    def test_14_extend_sonar_data_no_lines_skipped_large_time_number(self):
        sonar_data = [{
            "time": Decimal(100)
        }]
        other_data = [{
            "time": Decimal(0),
            "data": "should not connect"
        }, {
            "time": Decimal(1),
            "data": "should connect"
        }]
        headers = ["data"]
        frequency = 1
        expected_result = [{
            "time": Decimal(100),
            "data": "should connect"
        }]
        actual_result = data_handler.extend_sonar_data(sonar_data, other_data, headers, frequency)
        self.assertEqual(expected_result, actual_result)


    def test_15_extend_sonar_data_no_lines_skipped_zero_frequency(self):
        sonar_data = [{
            "time": Decimal(1)
        }]
        other_data = [{
            "time": Decimal(0),
            "data": "should not connect"
        }, {
            "time": Decimal(1),
            "data": "should connect"
        }]
        headers = ["data"]
        frequency = 0
        expected_result = [{
            "time": Decimal(1),
            "data": "should connect"
        }]
        actual_result = data_handler.extend_sonar_data(sonar_data, other_data, headers, frequency)
        self.assertEqual(expected_result, actual_result)


    def test_16_extend_sonar_data_no_lines_skipped_negative_frequency(self):
        sonar_data = [{
            "time": Decimal(1)
        }]
        other_data = [{
            "time": Decimal(0),
            "data": "should not connect"
        }, {
            "time": Decimal(1),
            "data": "should connect"
        }]
        headers = ["data"]
        frequency = -1
        expected_result = [{
            "time": Decimal(1),
            "data": "should connect"
        }]
        actual_result = data_handler.extend_sonar_data(sonar_data, other_data, headers, frequency)
        self.assertEqual(expected_result, actual_result)


    def test_17_extend_sonar_data_no_lines_skipped_negative_time(self):
        #in case of negative START_TIME reference point time values can be negative
        sonar_data = [{
            "time": Decimal(-5)
        }]
        other_data = [{
            "time": Decimal(0),
            "data": "should connect"
        }, {
            "time": Decimal(1),
            "data": "should not connect"
        }]
        headers = ["data"]
        frequency = 1
        expected_result = [{
            "time": Decimal(-5),
            "data": "should connect"
        }]
        actual_result = data_handler.extend_sonar_data(sonar_data, other_data, headers, frequency)
        self.assertEqual(expected_result, actual_result)


    def test_18_extend_sonar_data_lines_skipped(self):
        sonar_data = [{
            "time": Decimal(1)
        }]
        other_data = [{
            "time": Decimal(0),
            "data": "should connect"
        }, {
            "time": Decimal(100),
            "data": "should not connect"
        }]
        headers = ["data"]
        frequency = 1
        lines_skipped = True
        expected_result = [{
            "time": Decimal(1),
            "data": "should connect"
        }]
        actual_result = data_handler.extend_sonar_data(sonar_data, other_data, headers, frequency, lines_skipped)
        self.assertEqual(expected_result, actual_result)


    def test_19_extend_sonar_data_lines_skipped_negative_time(self):
        sonar_data = [{
            "time": Decimal(-3)
        }]
        other_data = [{
            "time": Decimal(-4),
            "data": "should connect"
        }, {
            "time": Decimal(-1),
            "data": "should not connect"
        }]
        headers = ["data"]
        frequency = 1
        lines_skipped = True
        expected_result = [{
            "time": Decimal(-3),
            "data": "should connect"
        }]
        actual_result = data_handler.extend_sonar_data(sonar_data, other_data, headers, frequency, lines_skipped)
        self.assertEqual(expected_result, actual_result)


    def test_20_extend_sonar_data_lines_skipped_small_difference(self):
        sonar_data = [{
            "time": Decimal(0)
        }]
        other_data = [{
            "time": Decimal(0.00000001),
            "data": "should connect"
        }, {
            "time": Decimal(0.00000002),
            "data": "should not connect"
        }]
        headers = ["data"]
        frequency = 1
        lines_skipped = True
        expected_result = [{
            "time": Decimal(0),
            "data": "should connect"
        }]
        actual_result = data_handler.extend_sonar_data(sonar_data, other_data, headers, frequency, lines_skipped)
        self.assertEqual(expected_result, actual_result)


if __name__ == '__main__':
    unittest.main()
import unittest
import point_locator
from decimal import Decimal


class PointLocatorTest(unittest.TestCase):
    
    def test_0_calculate_distance_double_sound_speed(self):
        speed_of_sound = Decimal(10)
        sample_index = Decimal(10)
        multiplier = 2
        original_distance = point_locator.calculate_distance(sample_index, speed_of_sound)
        expected_outcome = original_distance * multiplier
        actual_value = point_locator.calculate_distance(sample_index, speed_of_sound * multiplier)
        self.assertEqual(expected_outcome, actual_value)


    def test_1_calculate_distance_half_sample_index(self):
        speed_of_sound = Decimal(10)
        sample_index = Decimal(10)
        divider = 2
        original_distance = point_locator.calculate_distance(sample_index, speed_of_sound)
        expected_outcome = original_distance / divider
        actual_value = point_locator.calculate_distance(sample_index / divider, speed_of_sound)
        self.assertEqual(expected_outcome, actual_value)


    def test_2_calculate_distance_negative_sound_speed(self):
        """
        In theory it is possible to get negative numbers, since data_handler only skips
        data if it cannot be converted to Decimal, so further validation is needed.
        """
        speed_of_sound = Decimal(-10)
        sample_index = Decimal(10)
        self.assertRaises(ValueError, point_locator.calculate_distance, sample_index, speed_of_sound)


    def test_3_calculate_distance_negative_sample_index(self):
        """
        In theory it is possible to get negative numbers, since data_handler only skips
        data if it cannot be converted to Decimal, so further validation is needed.
        """
        speed_of_sound = Decimal(10)
        sample_index = Decimal(-10)
        self.assertRaises(ValueError, point_locator.calculate_distance, sample_index, speed_of_sound)


if __name__ == '__main__':
    unittest.main()
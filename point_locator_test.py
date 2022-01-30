import unittest
import main
from decimal import Decimal


class PointLocatorTest(unittest.TestCase):
    
    def test_0_calculate_distance_double_sound_speed(self):
        speed_of_sound = Decimal(10)
        sample_index = Decimal(10)
        multiplier = 2
        original_distance = main.calculate_distance(sample_index, speed_of_sound)
        expected_outcome = original_distance * multiplier
        actual_value = main.calculate_distance(sample_index, speed_of_sound * multiplier)
        self.assertEqual(expected_outcome, actual_value)


    def test_1_calculate_distance_half_sample_index(self):
        speed_of_sound = Decimal(10)
        sample_index = Decimal(10)
        divider = 2
        original_distance = main.calculate_distance(sample_index, speed_of_sound)
        expected_outcome = original_distance / divider
        actual_value = main.calculate_distance(sample_index / divider, speed_of_sound)
        self.assertEqual(expected_outcome, actual_value)


    def test_2_calculate_distance_negative_sound_speed(self):
        """
        In theory it is possible to get negative numbers, since data_handler only skips
        data if it cannot be converted to Decimal, so further validation is needed.
        """
        speed_of_sound = Decimal(-10)
        sample_index = Decimal(10)
        self.assertRaises(ValueError, main.calculate_distance, sample_index, speed_of_sound)


    def test_3_calculate_distance_negative_sample_index(self):
        """
        In theory it is possible to get negative numbers, since data_handler only skips
        data if it cannot be converted to Decimal, so further validation is needed.
        """
        speed_of_sound = Decimal(10)
        sample_index = Decimal(-10)
        self.assertRaises(ValueError, main.calculate_distance, sample_index, speed_of_sound)


    def test_4_calculate_altitude_sample_angle_zero(self):
        sample_angle = 0
        distance = 5
        sonar_altitude = 0
        expected_outcome = -5
        actual_value = main.calculate_altitude_of_point(distance, sample_angle, sonar_altitude)
        self.assertEqual(expected_outcome, actual_value)


    def test_5_calculate_altitude_sonar_altitude_decreased(self):
        sample_angle = 0
        distance = 5
        sonar_altitude = 0
        difference = 5
        first_data = main.calculate_altitude_of_point(distance, sample_angle, sonar_altitude)
        sonar_altitude -= difference
        expected_outcome = first_data - difference
        actual_value = main.calculate_altitude_of_point(distance, sample_angle, sonar_altitude)
        self.assertEqual(expected_outcome, actual_value)


    def test_6_transform_coordinates(self):
        longitude = 1
        latitude = 1
        expected_outcome = 517825.18
        actual_value = main.transform_coordinates(longitude, latitude)[0]
        self.assertAlmostEqual(expected_outcome, actual_value, 0)


    def test_7_transform_coordinates(self):
        longitude = 1
        latitude = 1
        expected_outcome = 6350350.27
        actual_value = main.transform_coordinates(longitude, latitude)[1]
        self.assertAlmostEqual(expected_outcome, actual_value, 0)


    def test_8_transform_coordinates_southern_hemisphere(self):
        longitude = 1
        latitude = -1
        expected_outcome = 3649649.73
        actual_value = main.transform_coordinates(longitude, latitude)[1]
        self.assertAlmostEqual(expected_outcome, actual_value, 0)


if __name__ == '__main__':
    unittest.main()
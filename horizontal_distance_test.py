import unittest
import point_locator
from decimal import Decimal
from math import pi


class HorizontalDistanceTest(unittest.TestCase):


    def setup_move_tests(self, sample_angle, heading, attribute_to_change, change_by):
        """
        Negative sample angle, no pitch and roll, heading north.
        Heading decreases: we expect the horizontal distance to decrease.
        """
        distance = Decimal(5)
        angle = Decimal(sample_angle)
        first_data = {
            "heading": Decimal(heading),
            "pitch": Decimal(0),
            "roll": Decimal(0)
        }
        second_data = {
            "heading": Decimal(heading),
            "pitch": Decimal(0),
            "roll": Decimal(0)
        }
        second_data[attribute_to_change] += Decimal(change_by)
        first_distance = point_locator.calculate_horizontal_distance(distance, angle, first_data)
        second_distance = point_locator.calculate_horizontal_distance(distance, angle, second_data)
        return first_distance, second_distance


    def test_0_calculate_horizontal_distance(self):
        """
        Positive sample angle, no pitch and roll, heading north.
        Heading decreases: we expect the horizontal distance to increase (to be less negative).
        """
        first_distance, second_distance = self.setup_move_tests(1, 0, "heading", -0.1)
        self.assertLess(first_distance, second_distance)


    def test_1_calculate_horizontal_distance(self):
        """
        Positive sample angle, no pitch and roll, heading north.
        Heading inreases: we expect the horizontal distance to increase (to be less negative).
        """
        first_distance, second_distance = self.setup_move_tests(1, 0, "heading", 0.1)
        self.assertLess(first_distance, second_distance)


    def test_2_calculate_horizontal_distance(self):
        """
        Negative sample angle, no pitch and roll, heading north.
        Heading decreases: we expect the horizontal distance to decrease.
        """
        first_distance, second_distance = self.setup_move_tests(-1, 0, "heading", -0.1)
        self.assertGreater(first_distance, second_distance)


    def test_3_calculate_horizontal_distance(self):
        """
        Negative sample angle, no pitch and roll, heading north.
        Heading inreases: we expect the horizontal distance to increase (to be less negative).
        """
        first_distance, second_distance = self.setup_move_tests(-1, 0, "heading", 0.1)
        self.assertGreater(first_distance, second_distance)

    
    def test_4_calculate_horizontal_distance(self):
        """
        Positive sample angle, no roll, heading north.
        Pitching decreases: we expect no changes horizontally.
        """
        first_distance, second_distance = self.setup_move_tests(1, 0, "pitch", -0.1)
        self.assertEqual(first_distance, second_distance)


    def test_5_calculate_horizontal_distance(self):
        """
        Positive sample angle, no roll, heading north.
        Pitching increases: we expect no changes horizontally.
        """
        first_distance, second_distance = self.setup_move_tests(1, 0, "pitch", 0.1)
        self.assertEqual(first_distance, second_distance)


    def test_6_calculate_horizontal_distance(self):
        """
        Negative sample angle, no roll, heading north.
        Pitching decreases: we expect no changes horizontally.
        """
        first_distance, second_distance = self.setup_move_tests(-1, 0, "pitch", -0.1)
        self.assertEqual(first_distance, second_distance)


    def test_7_calculate_horizontal_distance(self):
        """
        Negative sample angle, no roll, heading north.
        Pitching increases: we expect no changes horizontally.
        """
        first_distance, second_distance = self.setup_move_tests(-1, 0, "pitch", 0.1)
        self.assertEqual(first_distance, second_distance)


    def test_8_calculate_horizontal_distance(self):
        """
        Positive sample angle, no pitch, heading north.
        Rolling decreases: we expect horizontal distance to increase.
        """
        first_distance, second_distance = self.setup_move_tests(1, 0, "roll", -0.1)
        self.assertLess(first_distance, second_distance)


    def test_9_calculate_horizontal_distance(self):
        """
        Positive sample angle, no pitch, heading north.
        Rolling increases: we expect horizontal distance to decrease.
        """
        first_distance, second_distance = self.setup_move_tests(1, 0, "roll", 0.1)
        self.assertGreater(first_distance, second_distance)


    def test_10_calculate_horizontal_distance(self):
        """
        Negative sample angle, no pitch, heading north.
        Rolling decreases: we expect horizontal distance to increase.
        """
        first_distance, second_distance = self.setup_move_tests(-1, 0, "roll", -0.1)
        self.assertLess(first_distance, second_distance)


    def test_11_calculate_horizontal_distance(self):
        """
        Negative sample angle, no pitch, heading north.
        Rolling increases: we expect horizontal distance to decrease.
        """
        first_distance, second_distance = self.setup_move_tests(-1, 0, "roll", 0.1)
        self.assertGreater(first_distance, second_distance)


    def test_12_calculate_horizontal_distance(self):
        """
        Positive sample angle, no pitch and roll, heading east.
        Heading decreases: we expect the horizontal distance to decrease.
        """
        first_distance, second_distance = self.setup_move_tests(1, pi / 2, "heading", -0.1)
        self.assertGreater(first_distance, second_distance)


    def test_13_calculate_horizontal_distance(self):
        """
        Positive sample angle, no pitch and roll, heading east.
        Heading inreases: we expect the horizontal distance to increase.
        """
        first_distance, second_distance = self.setup_move_tests(1, pi / 2, "heading", 0.1)
        self.assertLess(first_distance, second_distance)


    def test_14_calculate_horizontal_distance(self):
        """
        Negative sample angle, no pitch and roll, heading east.
        Heading decreases: we expect the horizontal distance to increase.
        """
        first_distance, second_distance = self.setup_move_tests(-1, pi / 2, "heading", -0.1)
        self.assertLess(first_distance, second_distance)


    def test_15_calculate_horizontal_distance(self):
        """
        Negative sample angle, no pitch and roll, heading east.
        Heading inreases: we expect the horizontal distance to decrease.
        """
        first_distance, second_distance = self.setup_move_tests(-1, pi / 2, "heading", 0.1)
        self.assertGreater(first_distance, second_distance)

    
    def test_16_calculate_horizontal_distance(self):
        """
        Positive sample angle, no roll, heading east.
        Pitching decreases: we expect the horizontal distance to decrease.
        """
        first_distance, second_distance = self.setup_move_tests(1, pi / 2, "pitch", -0.1)
        self.assertGreater(first_distance, second_distance)


    def test_17_calculate_horizontal_distance(self):
        """
        Positive sample angle, no roll, heading north.
        Pitching increases: we expect the horizontal distance to increase.
        """
        first_distance, second_distance = self.setup_move_tests(1, pi / 2, "pitch", 0.1)
        self.assertLess(first_distance, second_distance)


    def test_18_calculate_horizontal_distance(self):
        """
        Negative sample angle, no roll, heading north.
        Pitching decreases: we expect the horizontal distance to decrease.
        """
        first_distance, second_distance = self.setup_move_tests(-1, pi / 2, "pitch", -0.1)
        self.assertGreater(first_distance, second_distance)


    def test_19_calculate_horizontal_distance(self):
        """
        Negative sample angle, no roll, heading north.
        Pitching increases: we expect the horizontal distance to increase.
        """
        first_distance, second_distance = self.setup_move_tests(-1, pi / 2, "pitch", 0.1)
        self.assertLess(first_distance, second_distance)


    def test_20_calculate_horizontal_distance(self):
        """
        Positive sample angle, no pitch, heading east.
        Rolling decreases: we expect no changes horizontally.
        """
        first_distance, second_distance = self.setup_move_tests(1, pi / 2, "roll", -0.1)
        self.assertAlmostEqual(first_distance, second_distance)


    def test_21_calculate_horizontal_distance(self):
        """
        Positive sample angle, no pitch, heading east.
        Rolling increases: we expect no changes horizontally.
        """
        first_distance, second_distance = self.setup_move_tests(1, pi / 2, "roll", 0.1)
        self.assertAlmostEqual(first_distance, second_distance)


    def test_22_calculate_horizontal_distance(self):
        """
        Negative sample angle, no pitch, heading east.
        Rolling decreases: we expect no changes horizontally.
        """
        first_distance, second_distance = self.setup_move_tests(-1, pi / 2, "roll", -0.1)
        self.assertAlmostEqual(first_distance, second_distance)


    def test_23_calculate_horizontal_distance(self):
        """
        Negative sample angle, no pitch, heading east.
        Rolling increases: we expect no changes horizontally.
        """
        first_distance, second_distance = self.setup_move_tests(-1, pi / 2, "roll", 0.1)
        self.assertAlmostEqual(first_distance, second_distance)


if __name__ == '__main__':
    unittest.main()
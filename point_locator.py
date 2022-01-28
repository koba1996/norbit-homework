from decimal import Decimal
import data_handler
from math import sin, cos, pi
from pyproj import Proj

def get_sonar_data():
    START_TIME = 0

    GNSS_FREQUENCY = 50
    GNSS_HEADERS = ["roll", "pitch", "heading", "latitude", "longitude", "altitude", "heave"]
    GNSS_FILENAME = "gnss.txt"

    SPEED_OF_SOUND_FREQUENCY = 1
    SPEED_OF_SOUND_HEADERS = ["speed"]
    SPEED_OF_SOUND_FILENAME = "speed_of_sound.txt"

    gnss_data = data_handler.read_data(GNSS_FILENAME, START_TIME, GNSS_FREQUENCY, GNSS_HEADERS)
    speed_of_sound_data = data_handler.read_data(SPEED_OF_SOUND_FILENAME, START_TIME, SPEED_OF_SOUND_FREQUENCY, SPEED_OF_SOUND_HEADERS)
    sonar_data = data_handler.read_sonar_data(START_TIME)
    sonar_data = data_handler.extend_sonar_data(sonar_data, gnss_data, GNSS_HEADERS, GNSS_FREQUENCY)
    sonar_data = data_handler.extend_sonar_data(sonar_data, speed_of_sound_data, SPEED_OF_SOUND_HEADERS, SPEED_OF_SOUND_FREQUENCY)
    return sonar_data


def calculate_distance(sample_index, speed_of_sound):
    SAMPLE_FREQUENCY = 78125
    distance = sample_index / SAMPLE_FREQUENCY * speed_of_sound / 2
    return distance


def calculate_horizontal_distance(distance, sample_angle, dataline):
    heading_angle = dataline["heading"]
    pitching_angle = dataline["pitch"]
    rolling_angle = dataline["roll"]
    horizontal_distance = distance * ((-1) * Decimal(sin(sample_angle + rolling_angle)) * Decimal(cos(heading_angle)) + Decimal(sin(pitching_angle)) * Decimal(sin(heading_angle)))
    return horizontal_distance


def calculate_vertical_distance(distance, sample_angle, dataline):
    heading_angle = dataline["heading"]
    pitching_angle = dataline["pitch"]
    rolling_angle = dataline["roll"]
    vertical_distance = distance * (Decimal(sin(sample_angle + rolling_angle)) * Decimal(sin(heading_angle)) + Decimal(sin(pitching_angle)) * Decimal(cos(heading_angle)))
    return vertical_distance


def calculate_altitude_of_point(distance, sample_angle, sonar_altitude):
    altitude_difference = (-1) * distance * Decimal(cos(sample_angle))
    altitude_of_point = sonar_altitude + altitude_difference
    return altitude_of_point


def transform_coordinates(longitude, latitude):
    convert_rate = Decimal(180 / pi)
    longitude *= convert_rate
    latitude *= convert_rate
    zone = int(divmod(longitude, 6)[0]) + 30
    converter = Proj(proj='utm', zone=zone, ellps='WGS84')
    utmx, utmy = converter(longitude, latitude)
    if latitude < 0:
        utmy= utmy + 10000000
    return [utmx, utmy, zone]


def find_located_points(dataline):
    located_points = []
    angle_index_pairs = dataline["angle_index_pairs"]
    utm_base_coordinates = transform_coordinates(dataline["longitude"], dataline["latitude"])
    print(dataline["time"])
    for angle_index_pair in angle_index_pairs:
        angle = angle_index_pair["angle"]
        sample_index = angle_index_pair["sample_index"]
        distance = calculate_distance(sample_index, dataline["speed"])
        horizontal_distance = calculate_horizontal_distance(distance, angle, dataline)
        vertical_distance = calculate_vertical_distance(distance, angle, dataline)
        utm_x = Decimal(utm_base_coordinates[0]) + horizontal_distance
        utm_y = Decimal(utm_base_coordinates[1]) + vertical_distance
        altitude = calculate_altitude_of_point(distance, angle, dataline["altitude"])
        point = {
            "X": utm_x,
            "Y": utm_y,
            "zone": utm_base_coordinates[2],
            "altitude": altitude
        }
        located_points.append(point)
        data_by_time = {
            "time": dataline["time"],
            "points": located_points
        }
    return data_by_time



def main():
    data = get_sonar_data()
    located_points = []
    for data_line in data:
        located_line = find_located_points(data_line)
        located_points.append(located_line)
    print(located_points[0])

main()

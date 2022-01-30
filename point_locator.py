from decimal import Decimal
import data_handler
from math import sin, cos, pi
from pyproj import Proj


_projections = {}


def get_sonar_data():
    """
    A simple function to read and manage the data contained in the text files.
    The constants are containing information about the current data format and devices.
    If we change these in the future, we only need to manipulate the constants.
    Returns an array of extended sonar data, each element contains:
    the time (compared to the START_TIME reference point), an array of angle/sample index pairs,
    the relevant location and orientation data of that time (roll, pitch, heading, longitude, latitude, altitude, heave),
    and the speed of sound.
    """
    START_TIME = 0

    GNSS_FREQUENCY = 50
    GNSS_HEADERS = ["roll", "pitch", "heading", "latitude", "longitude", "altitude", "heave"]
    GNSS_FILENAME = "gnss.txt"

    SPEED_OF_SOUND_FREQUENCY = 1
    SPEED_OF_SOUND_HEADERS = ["speed"]
    SPEED_OF_SOUND_FILENAME = "speed_of_sound.txt"

    SONAR_FILENAME = "sonar.txt"

    print("Collecting data...")
    sonar_data = data_handler.read_sonar_data(SONAR_FILENAME, START_TIME)
    gnss_data, lines_skipped = data_handler.read_data(GNSS_FILENAME, START_TIME, GNSS_FREQUENCY, GNSS_HEADERS)
    sonar_data = data_handler.extend_sonar_data(sonar_data, gnss_data, GNSS_HEADERS, GNSS_FREQUENCY, lines_skipped)
    speed_of_sound_data, lines_skipped = data_handler.read_data(SPEED_OF_SOUND_FILENAME, START_TIME, SPEED_OF_SOUND_FREQUENCY, SPEED_OF_SOUND_HEADERS)
    sonar_data = data_handler.extend_sonar_data(sonar_data, speed_of_sound_data, SPEED_OF_SOUND_HEADERS, SPEED_OF_SOUND_FREQUENCY, lines_skipped)
    return sonar_data


def calculate_distance(sample_index: Decimal, speed_of_sound: Decimal):
    """
    Calculates the distance between the located point and the sonar,
    using the sample frequency, sample index and the speed of sound.
    Frequency stored in a variable, and later can be changed if a different frequency is used.
    In case of negative sample index or speed an exception is raised. Future idea: depending on the usage of the data 
    this could be handled by a default value instead of an exception.
    """
    if not (sample_index > 0 and speed_of_sound > 0):
        raise ValueError('Cannot calculate distance, invalid data: ', sample_index, ', ', speed_of_sound)
    SAMPLE_FREQUENCY = 78125
    distance = sample_index / SAMPLE_FREQUENCY * speed_of_sound / 2
    return distance


def calculate_horizontal_distance(distance: Decimal, sample_angle: Decimal, dataline):
    """
    Calculates the horizontal distance between the sonar and the located point using trigonatric formula
    based on four angles (heading, pitch, roll, and the sample angle)
    and the distance.
    """
    heading_angle = dataline["heading"]
    pitching_angle = dataline["pitch"]
    rolling_angle = dataline["roll"]
    horizontal_distance = distance * ((-1) * Decimal(sin(sample_angle + rolling_angle)) * Decimal(cos(heading_angle)) + Decimal(sin(pitching_angle)) * Decimal(sin(heading_angle)))
    return horizontal_distance


def calculate_vertical_distance(distance: Decimal, sample_angle: Decimal, dataline):
    """
    Calculates the vertical distance between the sonar and the located point using trigonatric formula
    based on four angles (heading, pitch, roll, and the sample angle)
    and the distance.
    """
    heading_angle = dataline["heading"]
    pitching_angle = dataline["pitch"]
    rolling_angle = dataline["roll"]
    vertical_distance = distance * (Decimal(sin(sample_angle + rolling_angle)) * Decimal(sin(heading_angle)) + Decimal(sin(pitching_angle)) * Decimal(cos(heading_angle)))
    return vertical_distance


def calculate_altitude_of_point(distance: Decimal, sample_angle: Decimal, sonar_altitude: Decimal):
    """
    Calculates the altitude of the located point
    based on the distance, the cosine of the sample angle and the altitude of the sonar.
    It ignores the heave correction for now, but later it can be added easily, if necessary.
    """
    altitude_difference = (-1) * distance * Decimal(cos(sample_angle))
    altitude_of_point = sonar_altitude + altitude_difference
    return altitude_of_point


def get_zone(coordinates):
    UTM_OFFSET = 1
    UTM_ANGLE_DEGREES = 6

    if 56 <= coordinates[1] < 64 and 3 <= coordinates[0] < 12:
        return 32
    if 72 <= coordinates[1] < 84 and 0 <= coordinates[0] < 42:
        if coordinates[0] < 9:
            return 31
        elif coordinates[0] < 21:
            return 33
        elif coordinates[0] < 33:
            return 35
        return 37
    return int((coordinates[0] + 180) / UTM_ANGLE_DEGREES) + UTM_OFFSET


def get_letter(longitude):
    return 'CDEFGHJKLMNPQRSTUVWXX'[int((longitude + 80) / 8)]


def transform_coordinates(longitude, latitude):
    """
    Transforms the longitude and latitude angles into UTM coordinates using third party library.
    The constants are based on conventions, not likely to change in the future.
    The current coordinates are on the northern hemisphere, but in case of other locations in the future
    the code can calculate with the southern hemisphere's offset as well.
    Future idea: should replace this function with a more convinient and more efficient one.
    """
    SOUTHERN_HEMISPHERE_OFFSET = 10000000
    RAD_DEGREE_CONVERT_RATE = Decimal(180 / pi)

    longitude *= RAD_DEGREE_CONVERT_RATE
    latitude *= RAD_DEGREE_CONVERT_RATE

    zone_number = get_zone([longitude, latitude])
    letter = get_letter(longitude)
    if zone_number not in _projections:
        _projections[zone_number] = Proj(proj='utm', zone=zone_number, ellps='WGS84')
    utm_x, utm_y = _projections[zone_number](longitude, latitude)
    if utm_y < 0:
        utm_y += SOUTHERN_HEMISPHERE_OFFSET
    zone = letter + str(zone_number)
    return [utm_x, utm_y, zone]


def calculate_coordinates(angle_index_pair, dataline, utm_base_coordinates):
    """
    Combines the above calculation methods to evaluate the coordinates of a point.
    """
    angle = angle_index_pair["angle"]
    sample_index = angle_index_pair["sample_index"]
    distance = calculate_distance(sample_index, dataline["speed"])
    horizontal_distance = calculate_horizontal_distance(distance, angle, dataline)
    vertical_distance = calculate_vertical_distance(distance, angle, dataline)
    utm_x = Decimal(utm_base_coordinates[0]) + horizontal_distance
    utm_y = Decimal(utm_base_coordinates[1]) + vertical_distance
    altitude = calculate_altitude_of_point(distance, angle, dataline["altitude"])
    return utm_x, utm_y, altitude



def locate_points(dataline):
    """
    Finds the 3D location of every point in one line of data. Data lines are based on time.
    One line of data means all the detected points that can be assigned to the timestamp of the line.
    Returns a dictionary that contains the time (compared to the START_TIME reference point),
    and an array of the points: 3D coordinates and UTM zone for each of them.
    If this structure is too complex, points can be tuples instead of dictionaries.
    If (for some reason in the future) we need to know the position of the sonar 
    in the moment it detected these points, we can store the position data as well.
    """
    located_points = []
    angle_index_pairs = dataline["angle_index_pairs"]
    utm_base_coordinates = transform_coordinates(dataline["longitude"], dataline["latitude"])
    for angle_index_pair in angle_index_pairs:
        utm_x, utm_y, altitude = calculate_coordinates(angle_index_pair, dataline, utm_base_coordinates)
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


def get_located_points(data):
    """
    Collect all the located points from the extended sonar data, and arrange them into an array of dictionaries.
    Each dictionary contains a time field, and the array of points that were located in that time.
    Based on the usage of the points further arrangements are possible, 
    but this data storing model can be a decent base for many future applications of the data.
    """
    print("Calculating coordinates, this might take around half a minute")
    all_located_points = []
    for data_line in data:
        one_line_of_located_points = locate_points(data_line)
        all_located_points.append(one_line_of_located_points)
    return all_located_points


def main():
    data = get_sonar_data()
    located_points = get_located_points(data)
    print("Finished")

if __name__ == '__main__':
    main()

import re
from decimal import *

def format_data(one_line_of_data, time, headers):
    formatted_data = {}
    formatted_data["time"] = time
    for index, data in enumerate(one_line_of_data):
        formatted_data[headers[index]] = Decimal(data)
    return formatted_data



def read_data(filename, start_time, frequency, headers):
    f = open(filename,"r")
    full_data = f.read()
    data_lines = full_data.split('\n')
    data_lines = data_lines[1:]
    converted_data = []
    time = start_time
    for data_line in data_lines:
        if data_line != "":
            split_data = re.split('\t| ', data_line)
            formatted_data = format_data(split_data, time, headers)
            converted_data.append(formatted_data)
            time += Decimal(1/frequency)
    return converted_data


def format_sonar_data(one_line_of_data, time_diff):
    formatted_data = {}
    timestamp = Decimal(one_line_of_data[0])
    formatted_data["time"] = timestamp - time_diff
    angle_index_pairs = []
    for index in range(1, len(one_line_of_data)):
        if one_line_of_data[index] != "":
            angle = Decimal(one_line_of_data[index].split(",")[0])
            sample_index = Decimal(one_line_of_data[index].split(",")[1])
            angle_index_pair = {
                "angle": angle,
                "sample_index": sample_index
            }
            angle_index_pairs.append(angle_index_pair)
    formatted_data["angle_index_pairs"] = angle_index_pairs
    return formatted_data



def read_sonar_data(start_time):
    filename = "sonar.txt"
    f = open(filename,"r")
    full_data = f.read()
    data_lines = full_data.split('\n')
    data_lines = data_lines[1:]
    time_diff = Decimal(re.split('\t| ', data_lines[0])[0]) - start_time
    converted_data = []
    for data_line in data_lines:
        if data_line != "":
            split_data = re.split('\t| ', data_line)
            formatted_data = format_sonar_data(split_data, time_diff)
            converted_data.append(formatted_data)
    return converted_data


def extend_sonar_data(sonar_data, other_data, headers, frequency):
    for sonar_line in sonar_data:
        gnss_index = round(sonar_line["time"] * frequency)
        matching_gnss_line = other_data[gnss_index]
        for header in headers:
            sonar_line[header] = matching_gnss_line[header]
    return sonar_data

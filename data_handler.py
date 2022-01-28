import re
from decimal import Decimal, InvalidOperation

"""
Data handler is a module specified to read the current data type with the current separators.
If (in the future) other data formats will be used, only this module has to be updated,
point locator file do not have to be modified.
For now, exceptions only print an error message, but in the future this can be updated.
"""

def read_from_file(filename):
    """
    A simple function for reading the data from the file. Splits the text afterwards instead of using readline, 
    this way it can be easily updated to work with other separators.
    The header is removed before the return.
    If the provided filename is invalid, it returns empty array, and prints an error message.
    """
    try:
        f = open(filename,"r")
        full_data = f.read()
    except FileNotFoundError:
        print("Invalid filename provided: ", filename)
        return []
    data_lines = full_data.split('\n')
    return data_lines[1:]


def read_data(filename, start_time, frequency, headers):
    """
    Reads data from the files that have no timestamps included.
    It creates an array of dictionaries, each of the elements has their own time value 
    based on the frequency and the starting time.
    If a line is corrupted (has missing or invalid data), an error message is printed, the line is skipped,
    and the next line is getting processed. This way one corrupted line is not ruining the whole process.
    """
    data_lines = read_from_file(filename)
    if data_lines == []:
        return [], True
    converted_data = []
    lines_skipped = False
    time = Decimal(start_time)
    for index, data_line in enumerate(data_lines):
        if data_line != "":
            split_data = re.split('\t| ', data_line)
            formatted_data = format_data(split_data, time, headers)
            if (formatted_data == {}):
                print("Invalid or missing data in ", filename, " at line ", index)
                lines_skipped = True
            else:
                converted_data.append(formatted_data)
            time += Decimal(1) / Decimal(frequency)
    return converted_data, lines_skipped


def format_data(one_line_of_data, time, headers):
    """
    A function for formatting data that has no timestamp included. It creates a dictionary 
    from the input line: an array of strings.
    If there are any missing data or one of the numbers seems to be invalid, it returns an empty dictionary.
    Future plan: an algorythm, that can actually check which data is missing, and replace it with
    some error value, this way one corrupted data will not ruin the whole line.
    """
    formatted_data = {}
    formatted_data["time"] = time
    if len(one_line_of_data) != len(headers):
        return {}
    for index, data in enumerate(one_line_of_data):
        try:
            formatted_data[headers[index]] = Decimal(data)
        except InvalidOperation:
            return {}
    return formatted_data


def read_sonar_data(filename, start_time):
    """
    Reads timestamped data. Operating with the same starting time as the other functions,
    the first timestamp qualifies as the starting time, the others will be measured to the reference point.
    If the timestamp is corrupted, the function throws an error message, skips the current line, 
    and start processing the next one. This way one corrupted line is not ruining the whole file.
    """
    data_lines = read_from_file(filename)
    if data_lines == []:
        return []
    time_diff = Decimal(re.split('\t| ', data_lines[0])[0]) - Decimal(start_time)
    converted_data = []
    for index, data_line in enumerate(data_lines):
        if data_line != "":
            split_data = re.split('\t| ', data_line)
            formatted_data = format_sonar_data(split_data, time_diff)
            if (formatted_data == {}):
                print("Sonar data timestamp corrupted at line ", index)
            else:
                converted_data.append(formatted_data)
    return converted_data


def format_sonar_data(one_line_of_data, time_diff):
    """
    Formats one line of timestamped data, creates a dictionary with 
    the modified time value (compared to the starting time), and an array of dictionaries, each of them contains
    an angle/sample index pair. If this structure is too complex, the dictionaries can be replaced by tuples.
    If the timestamp is invalid, it throws an error message, and returns an empty dictionary.
    In case of one of the angle/sample index pairs are invalid, the program throws an error message, and skips it.
    The valid pairs are still getting processed, so the information loss is as small as it can be.
    """
    formatted_data = {}
    try:
        timestamp = Decimal(one_line_of_data[0])
        formatted_data["time"] = timestamp - time_diff
    except InvalidOperation:
        return {}
    angle_index_pairs = []
    for index in range(1, len(one_line_of_data)):
        if one_line_of_data[index] != "":
            try:
                angle = Decimal(one_line_of_data[index].split(",")[0])
                sample_index = Decimal(one_line_of_data[index].split(",")[1])
            except (IndexError, InvalidOperation):
                print("Invalid data in sonar file: ", one_line_of_data[index])
            else:
                angle_index_pair = {
                    "angle": angle,
                    "sample_index": sample_index
                }
                angle_index_pairs.append(angle_index_pair)
    formatted_data["angle_index_pairs"] = angle_index_pairs
    return formatted_data


def extend_sonar_data(sonar_data, other_data, headers, frequency=0, corrupted_data=False):
    """
    Connects the data from different files based on their time value.
    For performance issues if there was no lines skipped during the reading of the other data
    the program simply uses the frequency to find closest time value in the other dataset.
    This only works when the device has a predefined frequency. 
    In every other case the nearest value found based on the difference between the time values.
    """
    for sonar_line in sonar_data:
        if not corrupted_data and frequency != 0:
            other_data_index = round(sonar_line["time"] * frequency)
            matching_other_data_line = other_data[other_data_index]
        else:
            matching_other_data_line = min(other_data, key=lambda x: abs(sonar_line["time"] - x["time"]))
        for header in headers:
                sonar_line[header] = matching_other_data_line[header]
    return sonar_data

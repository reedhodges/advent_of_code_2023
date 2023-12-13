import numpy as np

# import data from input-test.txt
with open('input-6.txt', 'r') as input_file:
    data = input_file.read().splitlines()

# remove the first 11 characters from each string and separate by spaces
data = [x[12:].split(' ') for x in data]
# remove '' from sublists in data and convert to int
data = [[int(x) for x in y if x != ''] for y in data]
# transpose data
data_transposed = list(map(list, zip(*data)))

# calculate the distance traveled given total time and time button held
def calculate_distance_traveled(time_button_held, total_time):
    if time_button_held > total_time:
        return 'Button held longer than total time'
    speed = time_button_held
    time_moving = total_time - time_button_held
    distance_traveled = speed * time_moving
    return distance_traveled

def is_record_q(race, distance):
    record_distance = race[1]
    if distance > record_distance:
        return True
    else:
        return False

# calculate how many of the times the button is held down break the record for a given race
def calculate_record_breakers(race):
    race_time = race[0]
    # enumerate all possible times to hold the button
    button_times = list(range(race_time + 1))
    # calculate distances traveled for each button time
    distances_traveled = [calculate_distance_traveled(x, race_time) for x in button_times]
    # see which of these break the record
    record_breakers = [is_record_q(race, x) for x in distances_traveled]
    # filter record breakers that are not True
    record_breakers = [x for x in record_breakers if x == True]
    # return how many break the record
    return len(record_breakers)

# calculate for all races
all_races = [calculate_record_breakers(x) for x in data_transposed]
# calculate product of the elements of all_races
part_one = np.prod(all_races)

# now for part two, concatenate the sublists in data
# first convert all elements to strings
data = [[str(x) for x in y] for y in data]
# now concatenate the sublists
data = [''.join(x) for x in data]
# convert back to int
data = [int(x) for x in data]

part_two = calculate_record_breakers(data)

print(part_one)
print(part_two)
from itertools import groupby
from collections import defaultdict

with open('input-3.txt') as f:
    data = f.read().splitlines()

data = list(map(list, data))

characters = ['=', '-', '%', '&', '@', '$', '/', '+', '#']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# make a dictionary of number locations and values
number_locations = {}
for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j] in numbers:
            number_locations[(i, j)] = int(data[i][j])

# make a list of tuples of * locations
asterisk_locations = {}
for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j] == '*':
            asterisk_locations[(i, j)] = []

# for each * location, check the surrounding 8 locations for numbers
# if there are numbers in the surrounding locations, add the numbers' locations to the *'s list
for asterisk_location in asterisk_locations:
    for number_location in number_locations:
        if asterisk_location[0] - 1 <= number_location[0] <= asterisk_location[0] + 1 and asterisk_location[1] - 1 <= number_location[1] <= asterisk_location[1] + 1:
            asterisk_locations[asterisk_location].append(number_location)

# check the locations to the left and right of each number location in the * dictionary
# to see if they are numbers too
for k in range(3):
    for asterisk_location in asterisk_locations:
        for i in range(len(asterisk_locations[asterisk_location])):
            loc = asterisk_locations[asterisk_location][i]
            loc_left = (loc[0], loc[1] - 1)
            loc_right = (loc[0], loc[1] + 1)
            # if loc_left or loc_right is in number_locations, add it to the definition in asterisk_locations
            if loc_left in number_locations:
                asterisk_locations[asterisk_location].append(loc_left)
            if loc_right in number_locations:
                asterisk_locations[asterisk_location].append(loc_right)

# remove duplicates from the lists in asterisk_locations
for asterisk_location in asterisk_locations:
    asterisk_locations[asterisk_location] = list(set(asterisk_locations[asterisk_location]))

# function that takes a list of tuples and returns a 2D list
# where each row has the same x value
def sort_by_x(tuples):
    # sort the list of tuples by x-value
    sorted_tuples = sorted(tuples, key=lambda x: x[0])
    # group tuples by x-value
    grouped = groupby(sorted_tuples, key=lambda x: x[0])
    # create the 2D list
    list_2d = [list(group) for _, group in grouped]
    # sort the rows of list_2d by y-value
    for i in range(len(list_2d)):
        list_2d[i] = sorted(list_2d[i], key=lambda x: x[1])
    return list_2d

# sort the tuples in the definitions in asterisk_locations by x-value, then by y-value
asterisk_locations = {k: sorted(v, key=lambda x: (x[0], x[1])) for k, v in asterisk_locations.items()}

def find_sub_sequences(lst):
    # Find sub-sequences in a list of integers
    sorted_lst = sorted(lst)
    sub_sequences = []
    current_sequence = [sorted_lst[0]]

    for i in range(1, len(sorted_lst)):
        # If the current element is consecutive, add it to the current sequence
        if sorted_lst[i] == current_sequence[-1] + 1:
            current_sequence.append(sorted_lst[i])
        else:
            # Current element is not consecutive, start a new sequence
            sub_sequences.append(current_sequence)
            current_sequence = [sorted_lst[i]]

    # Add the last sequence
    sub_sequences.append(current_sequence)
    return sub_sequences

def sort_tuples(tuples):
    # only execute if all tuples have the same x-value
    if len(set([x for x, y in tuples])) == 1:
        # Group tuples by their x-value
        groups = defaultdict(list)
        for x, y in tuples:
            groups[x].append(y)
        
        # Prepare the 2D array
        sorted_2d_array = []
        for x in sorted(groups):
            sub_sequences = find_sub_sequences(groups[x])
            for seq in sub_sequences:
                sorted_2d_array.append([(x, y) for y in seq])
        
        return sorted_2d_array
    else:
        return tuples
    
# apply sort_tuples to each definition in asterisk_locations
asterisk_locations = {k: sort_tuples(v) for k, v in asterisk_locations.items()}

# function that returns true if the input is a 2d list
def is_2d_list(lst):
    return isinstance(lst[0], list)

# filter the definitions in asterisk_locations to a dictionary where the values
# are 2d lists and a dictionary where the values are 1d lists
# this lets us isolate the cases where the two numbers are on the same row
asterisk_same_x = {k: v for k, v in asterisk_locations.items() if is_2d_list(v)}
asterisk_locations = {k: v for k, v in asterisk_locations.items() if not is_2d_list(v)}

# map sort_by_x to each definition in asterisk_locations
# this sorts the numbers on different rows into a 2d list
asterisk_locations = {k: sort_by_x(v) for k, v in asterisk_locations.items()}

# rejoin the dictionaries
asterisk_locations.update(asterisk_same_x)

# remove keys from asterisk_locations that have values whose length is not 2
asterisk_locations = {k: v for k, v in asterisk_locations.items() if len(v) == 2}

# go through the 2d lists in asterisk_locations and replace the tuples with the definitions in number_locations
for asterisk_location in asterisk_locations:
    for i in range(len(asterisk_locations[asterisk_location])):
        for j in range(len(asterisk_locations[asterisk_location][i])):
            asterisk_locations[asterisk_location][i][j] = number_locations[asterisk_locations[asterisk_location][i][j]]

# concatenate the rows of the 2d lists in asterisk_locations
for asterisk_location in asterisk_locations:
    for i in range(len(asterisk_locations[asterisk_location])):
        # concatenate asterisk_locations[asterisk_location][i]
        asterisk_locations[asterisk_location][i] = ''.join(map(str, asterisk_locations[asterisk_location][i]))

# convert the values in asterisk_locations to integers
asterisk_locations = {k: list(map(int, v)) for k, v in asterisk_locations.items()}

# multiply the two numbers in each definition in asterisk_locations
asterisk_locations = {k: v[0] * v[1] for k, v in asterisk_locations.items()}

# add up all the definitions in asterisk_locations
answer = sum(asterisk_locations.values())

print(answer)

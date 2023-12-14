with open('input-14.txt') as f:
    data = f.read().splitlines()
    # split each line into a list of its characters
data = [list(line) for line in data]
data_len = len(data)
# initialize a dictionary with coordinates
coordinates = {}
# iterate over the data
for y in range(len(data)):
    for x in range(len(data[y])):
        # add the coordinates to the dictionary
        coordinates[(x, y)] = data[y][x]

def move_rock_north(tup, dic):
    '''
    Function that sees what the most northerly unoccupied spot is, then moves the rock
    there.
    '''
    (x, y) = tup
    # if we're at the top row, do nothing
    if y == 0:
        return
    # decrease y until it reaches an occupied spot
    while y > 0 and dic[(x, y-1)] == '.':
        y -= 1
    # if the original spot is as far north as possible, do nothing
    if y == tup[1]:
        return
    else:
        # move the rock to that spot
        dic[(x, y)] = dic[tup]
        # remove the rock from its original spot
        dic[tup] = '.'

def move_rock_south(tup, dic):
    '''
    Function that sees what the most southerly unoccupied spot is, then moves the rock
    there.
    '''
    (x, y) = tup
    # if we're at the bottom row, do nothing
    if y == data_len - 1:
        return
    # increase y until it reaches an occupied spot
    while y < data_len - 1 and dic[(x, y+1)] == '.':
        y += 1
    # if the original spot is as far south as possible, do nothing
    if y == tup[1]:
        return
    else:
        # move the rock to that spot
        dic[(x, y)] = dic[tup]
        # remove the rock from its original spot
        dic[tup] = '.'

def move_rock_east(tup, dic):
    '''
    Function that sees what the most easterly unoccupied spot is, then moves the rock
    there.
    '''
    (x, y) = tup
    # if we're at the rightmost column, do nothing
    if x == data_len - 1:
        return
    # increase x until it reaches an occupied spot
    while x < data_len - 1 and dic[(x+1, y)] == '.':
        x += 1
    # if the original spot is as far east as possible, do nothing
    if x == tup[0]:
        return
    else:
        # move the rock to that spot
        dic[(x, y)] = dic[tup]
        # remove the rock from its original spot
        dic[tup] = '.'

def move_rock_west(tup, dic):
    '''
    Function that sees what the most westerly unoccupied spot is, then moves the rock
    there.
    '''
    (x, y) = tup
    # if we're at the leftmost column, do nothing
    if x == 0:
        return
    # decrease x until it reaches an occupied spot
    while x > 0 and dic[(x-1, y)] == '.':
        x -= 1
    # if the original spot is as far west as possible, do nothing
    if x == tup[0]:
        return
    else:
        # move the rock to that spot
        dic[(x, y)] = dic[tup]
        # remove the rock from its original spot
        dic[tup] = '.'

def tilt_north(dic):
    '''
    Function that tilts the surface, moving all rocks as far north as possible.
    Start with the top row.
    '''
    dic_copy = dic.copy()
    # apply move_rock_north to each rock in dic
    for key in dic_copy:
        if dic_copy[key] == 'O':
            move_rock_north(key, dic_copy)
    return dic_copy

def tilt_south(dic):
    '''
    Function that tilts the surface, moving all rocks as far south as possible.
    Start with the bottom row.
    '''
    dic_copy = dic.copy()
    # apply move_rock_south to each rock in dic, starting with the bottom row
    for y in range(data_len-1, -1, -1):
        for x in range(data_len):
            if dic_copy[(x, y)] == 'O':
                move_rock_south((x, y), dic_copy)
    return dic_copy
    

def tilt_east(dic):
    '''
    Function that tilts the surface, moving all rocks as far east as possible. 
    Start with the rightmost column.
    '''
    dic_copy = dic.copy()
    # apply move_rock_east to each rock in dic, starting with the rightmost column
    for x in range(data_len-1, -1, -1):
        for y in range(data_len):
            if dic_copy[(x, y)] == 'O':
                move_rock_east((x, y), dic_copy)
    return dic_copy

def tilt_west(dic):
    '''
    Function that tilts the surface, moving all rocks as far west as possible.
    Start with the leftmost column.
    '''
    dic_copy = dic.copy()
    # apply move_rock_west to each rock in dic
    for x in range(data_len):
        for y in range(data_len):
            if dic_copy[(x,y)] == 'O':
                move_rock_west((x,y), dic_copy)
    return dic_copy

def cycle(dic):
    '''
    Function that tilts the surface north, then west, then south, then east.
    '''
    dic_copy = tilt_north(dic)
    dic_copy = tilt_west(dic_copy)
    dic_copy = tilt_south(dic_copy)
    dic_copy = tilt_east(dic_copy)
    return dic_copy

def calculate_load_single_rock(tup, dic):
    '''
    Calculates the load for a single rock.
    '''
    if dic[tup] == 'O':
        return data_len - tup[1]
    else:
        return 0

moved_north = tilt_north(coordinates)

# apply calculate_load_single_rock to each key in moved_north
# and sum the results
part_one = sum([calculate_load_single_rock(key, moved_north) for key in moved_north])

print('----')

def detect_cycle(initial_dic, N):
    '''
    Function to look for a repeating loop that occurs sometime in the first N
    applications of cycle() to initial_dic.  This can put an upper bound on 
    how far we need to look for the period of the cycle.
    '''
    # initialize a set to store the dictionaries
    seen = set()
    current_dic = initial_dic

    for _ in range(N): 
        current_dic = cycle(current_dic)
        # convert the dictionary to a frozenset of items for immutability and hashability
        dic_items = frozenset(current_dic.items())
        # look for the dictionary in the set
        if dic_items in seen:
            print("Cycle detected!")
            break
        else:
            seen.add(dic_items)
    else:
        print("No cycle detected in " + str(N) + " iterations.")

def detect_cycle(initial_dic, N):
    '''
    Function to look for a repeating loop that occurs sometime in the first N
    applications of cycle() to initial_dic.  It returns the endpoints of the
    loop.
    '''
    # initialize dictionary to store the occurrences of outputs
    occurrences = {}
    current_dic = initial_dic

    for i in range(N): 
        current_dic = cycle(current_dic)
        # convert the dictionary to a frozenset of items for immutability and hashability
        dic_items = frozenset(current_dic.items())
        # look for the dictionary in occurrences
        if dic_items in occurrences:
            first_occurrence = occurrences[dic_items]
            print(f"Cycle detected! First occurred at iteration {first_occurrence}, and again at iteration {i}.")
            print(f"The cycle has a period of {i - first_occurrence}.")
            # return the first occurrence, the period, and the dictionary at the end of the period
            return (first_occurrence, i-first_occurrence, current_dic)
        else:
            occurrences[dic_items] = i
    else:
        print("No cycle detected in " + str(N) + " iterations.")

# get the first occurrence and the period of the cycle
(first_occ, per, endpoint_dic) = detect_cycle(coordinates, 130)
# calculate the number of times we actually need to apply the cycle
num_applications = (1000000000 - first_occ) % per

# apply cycle() to endpoint_dic num_applications - 1 times
for _ in range(num_applications-1):
    endpoint_dic = cycle(endpoint_dic)

part_two = sum([calculate_load_single_rock(key, endpoint_dic) for key in endpoint_dic])

print('----')
print('Part One:', part_one)
print('Part Two:', part_two)
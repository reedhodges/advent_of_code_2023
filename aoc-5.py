# read 'input-test.txt' and get the lines corresponding to each map
with open('input-5.txt') as f:
    data = f.read().splitlines()
# initialize my_maps
my_maps = [0, 0, 0, 0, 0, 0, 0]
# seed to soil
my_maps[0] = data[data.index('seed-to-soil map:')+1:data.index('soil-to-fertilizer map:')-1]
# soil to fertilizer
my_maps[1] = data[data.index('soil-to-fertilizer map:')+1:data.index('fertilizer-to-water map:')-1]
# fertilizer to water
my_maps[2] = data[data.index('fertilizer-to-water map:')+1:data.index('water-to-light map:')-1]
# water to light
my_maps[3] = data[data.index('water-to-light map:')+1:data.index('light-to-temperature map:')-1]
# light to temperature
my_maps[4] = data[data.index('light-to-temperature map:')+1:data.index('temperature-to-humidity map:')-1]
# temperature to humidity
my_maps[5] = data[data.index('temperature-to-humidity map:')+1:data.index('humidity-to-location map:')-1]
# humidity is from 'humidity-to-location map:' to the end of the file
my_maps[6] = data[data.index('humidity-to-location map:')+1:]
# seeds are on the first line, without the first six characters
# put this in a list with space as the delimiter, convert to int
seeds = data[0][7:].split(' ')
seeds = [int(i) for i in seeds]

# take a list of strings and make each its own list, with space as the delimiter
# then convert the strings to ints
# then sort the sublists by the second element
def split_maps(list_of_strings):
    ans = [string.split(' ') for string in list_of_strings]
    ans = [[int(i) for i in string] for string in ans]
    ans = sorted(ans, key=lambda x: x[1])
    return ans

# apply split_maps to each of the elements of my_maps
my_maps = [split_maps(my_map) for my_map in my_maps]

# function to find the appropriate line in the map for a given source
def find_appr_line_in_map(source, appr_map):
    i = 0
    # find which sublist has the source range start appropriate for the source
    # this is the largest second element which is less than or equal to the source
    while source >= appr_map[i][1]:
        # if we've reached the end of the list, return the last element
        if i == len(appr_map) - 1:
            return i
        i += 1
    # if i is still zero, return source
    if i == 0:
        return 'Seed is below the lowest source range start'
    i -= 1
    return i

# function that checks if a source is actually within the range of the appropriate line
def check_if_in_range(source, appr_map):
    appr_line = find_appr_line_in_map(source, appr_map)
    if appr_line == 'Seed is below the lowest source range start':
        return False
    range_width = appr_map[appr_line][2]
    range_start = appr_map[appr_line][1]
    if source <= range_start + range_width-1:
        return True
    else:
        return False
    
# function that returns the destination for a given source
def get_destination(source, appr_map):
    # check if the source is within the range of the appropriate line
    boo = check_if_in_range(source, appr_map)
    # if not, return source
    if boo == False:
        return source
    # if so, return the destination
    else:
        # find appropriate line
        appr_line = find_appr_line_in_map(source, appr_map)
        # calculate difference between source and range start
        diff = source - appr_map[appr_line][1]
        return appr_map[appr_line][0] + diff
    
# function to go through all the maps in sequence and return the final destination
def get_final_destination(source):
    for i in range(len(my_maps)):
        source = get_destination(source, my_maps[i])
    return source

# apply get_final_destination to each of the seeds
final_destinations = [get_final_destination(seed) for seed in seeds]
# get minimum of final_destinations
part_one = min(final_destinations)
#print(final_destinations)

# then for part two, we have more seeds
# since all the piecewise functions are linear in x, the minimum will be at one of the endpoints
# so I need to enumerate all the domains and find the value of the function at each endpoint
# then find the minimum of those values

# function to identify the critical points of a piecewise function
def find_critical_points(appr_map):
    crit_points = []
    # add the starts of the ranges
    crit_points = [appr_map[i][0] for i in range(len(appr_map))]
    # in case there are gaps: add the starts of the gap ranges
    crit_points = crit_points + [appr_map[i][0] + appr_map[i][2] for i in range(len(appr_map))]
    # sort and remove duplicates
    crit_points = sorted(list(set(crit_points)))
    return crit_points

# function to get the appropriate line for the destination
def find_appr_line_in_map_inv(destination, appr_map):
    # sort the map by the first element
    appr_map = sorted(appr_map, key=lambda x: x[0])
    i = 0
    # find which sublist has the destination range start appropriate for the destination
    # this is the largest second element which is less than or equal to the destination
    while destination >= appr_map[i][0]:
        # if we've reached the end of the list, return the last element
        if i == len(appr_map) - 1:
            return i
        i += 1
    if i == 0:
        return 'You have passed a destination which is invalid'
    return i-1

# function to invert a map.  Given the destination, find the source
def invert_map(destination, appr_map):
    # sort appr_map by the first element
    appr_map = sorted(appr_map, key=lambda x: x[0])
    # find the appropriate line
    appr_line = find_appr_line_in_map_inv(destination, appr_map)
    # return destination if the destination is invalid
    # since this means the destination is less than the first range start
    if appr_line == 'You have passed a destination which is invalid':
        return destination
    if destination > appr_map[appr_line][0] + appr_map[appr_line][2] - 1:
        return destination
    # calculate the difference between the destination and the range start
    diff = destination - appr_map[appr_line][0]
    # return the source
    return appr_map[appr_line][1] + diff

# calculate the critical points of all the functions
crit_pts = [find_critical_points(my_map) for my_map in my_maps]

# now I need to invert these critical points to get the corresponding seeds
inverted_crit_pts = crit_pts
for i in range(len(crit_pts)):
    for j in range(len(crit_pts[i])):
        destination = crit_pts[i][j]
        k = i
        while k >= 0:
            destination = invert_map(destination, my_maps[k])
            k -= 1
        inverted_crit_pts[i][j] = destination

# flatten inverted_crit_pts and sort, removing duplicates
inverted_crit_pts = sorted(list(set([item for sublist in inverted_crit_pts for item in sublist])))

# group the elements in seeds in pairs of two
seeds = [seeds[i:i+2] for i in range(0, len(seeds), 2)]
# add the first element to the second element in each sublist
seeds = [[seed[0],sum(seed)-1] for seed in seeds]

# function to test whether a critical point is in a seed range
def is_in_seed_range(crit_pt):
    for seed in seeds:
        if crit_pt >= seed[0] and crit_pt <= seed[1]:
            return True
    return False

# filter out critical points that are not in a seed range
inverted_crit_pts = [inverted_crit_pt for inverted_crit_pt in inverted_crit_pts if is_in_seed_range(inverted_crit_pt)]

# add to inverted_crit_pts the first elements of each seed range
inverted_crit_pts = inverted_crit_pts + [seed[0] for seed in seeds]

# apply get_final_destination to each of the critical points
final_destinations = [get_final_destination(inverted_crit_pt) for inverted_crit_pt in inverted_crit_pts]
part_two = min(final_destinations)

print(part_one)
print(part_two)
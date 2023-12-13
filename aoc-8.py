import math

# load data from input-test.txt
with open('input-8.txt', 'r') as f:
    data = f.read().splitlines()

# get left-right code
left_right = data[0]
# split into list of characters
left_right = list(left_right)

# get nodes
nodes = data[2:]

# initialize dictionary for the nodes
node_dict = {}
for node in nodes:
    node_dict[node[:3]] = (node[7:10], node[12:15])

# function which outputs the destination given the current node and L or R
def get_destination(current_node, direction): 
    destination = node_dict[current_node][0] if direction == 'L' else node_dict[current_node][1]
    return destination

# function which traverses the nodes until ZZZ is reached
def traverse_nodes(current_node):
    # initialize the iterator for the left-right code
    direction_iterator = 0
    # initialize the number of steps taken
    steps = 0
    while current_node != 'ZZZ':
        # if we've reached the end of the left-right code, reset the iterator
        if direction_iterator == len(left_right):
            direction_iterator = 0
            current_node = get_destination(current_node, left_right[direction_iterator])
            direction_iterator += 1
            steps += 1
        else:
            current_node = get_destination(current_node, left_right[direction_iterator])
            direction_iterator += 1
            steps += 1
    return steps

part_one = traverse_nodes('AAA')

# get all the keys in nodes_dict whose last character is A
starting_nodes = [key for key in node_dict.keys() if key[-1] == 'A']

# function to check whether all the strings in a list end in Z
def all_end_in_z(list_of_strings):
    # if string is empty, return false
    if len(list_of_strings) == 0:
        return False
    else:
        return all([string[-1] == 'Z' for string in list_of_strings])

# function to print the first three times a node ends in Z
# this is just a slight modification of the traverse_nodes function
def print_ends_in_z(current_node):
    # initialize the iterator for the left-right code
    direction_iterator = 0
    # initialize total number of steps taken
    steps = 0
    # initialize the number of times we have ended up at a node ending in Z
    z_counter = 0
    while z_counter < 4:
        # if we've reached the end of the left-right code, reset the iterator
        if direction_iterator == len(left_right):
            direction_iterator = 0
            current_node = get_destination(current_node, left_right[direction_iterator])
            direction_iterator += 1
            steps += 1
        else:
            current_node = get_destination(current_node, left_right[direction_iterator])
            direction_iterator += 1
            steps += 1
        if current_node[-1] == 'Z':
            print(current_node + ' ' + str(steps))
            z_counter += 1
    return steps

# apply print_ends_in_z to all the starting nodes
#for node in starting_nodes:
#    print_ends_in_z(node)

# this tells us that each node in starting_node keeps coming back to the same node ending in Z after a fixed number of steps
# just need to find the least common multiple of these numbers
# can modify to return the number of steps after we reach the first node ending in Z
def traverse_nodes_end_in_z(current_node):
    # initialize the iterator for the left-right code
    direction_iterator = 0
    # initialize the number of steps taken
    steps = 0
    while current_node[-1] != 'Z':
        # if we've reached the end of the left-right code, reset the iterator
        if direction_iterator == len(left_right):
            direction_iterator = 0
            current_node = get_destination(current_node, left_right[direction_iterator])
            direction_iterator += 1
            steps += 1
        else:
            current_node = get_destination(current_node, left_right[direction_iterator])
            direction_iterator += 1
            steps += 1
    return steps

numbers = [traverse_nodes_end_in_z(node) for node in starting_nodes]

part_two = math.lcm(*numbers)

print(part_one)
print(part_two)
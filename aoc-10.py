import math

# load data from input-test.txt
with open('input-10.txt', 'r') as f:
    data = f.read().splitlines()

# split each string in the list into a list of characters
data = [list(string) for string in data]

# initialize a dictionary
# the keys are a tuple of the x,y coordinates of each element of data
# the values are False
path_dict = {}
for i in range(len(data)):
    for j in range(len(data[i])):
        path_dict[(i,j)] = False

# first find the location of the S
for key in path_dict.keys():
    if data[key[0]][key[1]] == 'S':
        path_dict[key] = 'O'
        start = key

# define the first step
if data[start[0]][start[1]+1] in ['-', '7', 'J']:
    first_step = (start[0], start[1]+1)
elif data[start[0]+1][start[1]] in ['|', 'L', 'J']:
    first_step = (start[0]+1, start[1])
elif data[start[0]][start[1]-1] in ['-', 'F', 'L']:
    first_step = (start[0], start[1]-1)
elif data[start[0]-1][start[1]]in ['|', 'F', '7']:
    first_step = (start[0]-1, start[1])

# mark this step as visited in the dictionary
#path_dict[first_step] = True

# function to define which step is next
def find_next_step(previous_step, current_step):
    # define row and col variables for convenience
    row = current_step[0]
    col = current_step[1]
    # get the character at the current step
    current_character = data[row][col]
    # if -, go right or left
    if current_character == '-':
        if previous_step[1] < current_step[1]:
            next_step = (row, col+1)
        else:
            next_step = (row, col-1)
    # if |, go up or down
    elif current_character == '|':
        if previous_step[0] < current_step[0]:
            next_step = (row+1, col)
        else:
            next_step = (row-1, col)
    # if 7, go either left or down
    elif current_character == '7':
        if previous_step[1] < current_step[1]:
            next_step = (row+1, col)
        else:
            next_step = (row, col-1)
    # if J, go either left or up
    elif current_character == 'J':
        if previous_step[1] < current_step[1]:
            next_step = (row-1, col)
        else:
            next_step = (row, col-1)
    # if L, go either right or up
    elif current_character == 'L':
        if previous_step[1] > current_step[1]:
            next_step = (row-1, col)
        else:
            next_step = (row, col+1)
    # if F, go either right or down
    elif current_character == 'F':
        if previous_step[1] > current_step[1]:
            next_step = (row+1, col)
        else:
            next_step = (row, col+1)
    return next_step

# function to calculate number of steps to get back to start
def calculate_steps():
    # initialize step counter
    step_count = 0
    # initialize current step
    current_step = first_step
    # initialize previous step
    previous_step = start
    # continue until we get back to the start
    while current_step != start:
        # mark the current step as visited
        path_dict[current_step] = True
        # find the next step
        next_step = find_next_step(previous_step, current_step)
        # update previous step
        previous_step = current_step
        # update current step
        current_step = next_step
        # increment step counter
        step_count += 1
    return step_count

# the farthest we can be from the start is half the number of steps
part_one = math.ceil(calculate_steps()/2)

# to determine if a point is inside the loop or not:
# if you're inside the loop, if you go to the edge of the space, you'll cross the border an odd number of times
# if you're outside the loop, if you go to the edge of the space, you'll cross the border an even number of times
# will need to be careful about traveling along the border and counting those as crossings
# I mostly avoid that problem if I only count crossings when I move diagonally
# then I have an issue if I cross a corner
def parity(point):
    # count the number of Trues you hit in path_dict
    counter = 0
    # initialize the current point
    row = point[0]
    col = point[1]
    # if the point is on the border, return an error message
    if path_dict[point] == True:
        return 'B'
    # move diagonally to the edge of the space
    # only go until you hit the edge
    while row < len(data) and col < len(data[0]):
        # if you hit a True that is not a corner that doesn't count as a crossing, increment the counter
        if path_dict[(row,col)] == True and is_corner((row,col)) == False:
            counter += 1
        row += 1
        col += 1
    # determine parity of the counter
    if counter % 2 == 0:
        return 'E'
    else:
        return 'O'
    
# function to check if a point is a corner that would not count as a crossing.
# since we are going diagonally down and to the right, these are 
# the 7 and L corners.  The J and F corners are fine and still count as crossings.
def is_corner(point):
    row = point[0]
    col = point[1]
    # 7 corners
    if data[row][col] == '7' and path_dict[point] == True:
        if data[row][col-1] in ['-','F','L'] and data[row+1][col] in ['|','L','J'] and path_dict[(row,col-1)] == True and path_dict[(row+1,col)] == True:
            return True
    # L corners
    elif data[row][col] == 'L' and path_dict[point] == True:
        if data[row][col+1] in ['-','7','J'] and data[row-1][col] in ['|','F','7'] and path_dict[(row,col+1)] == True and path_dict[(row-1,col)] == True:
            return True
    else:
        return False

# apply parity() to every point in path_dict
dict_2 = {key: parity(key) for key in path_dict.keys()}
# convert to an array
array = [[dict_2[(i,j)] for j in range(len(data[0]))] for i in range(len(data))]
# concatenate the rows of array
array = [''.join(row) for row in array]
# print the array for visualization
#for row in array:
#    print(row)
# output array to a txt file
#with open('output.txt', 'w') as f:
#    for row in array:
#        f.write(row)
#        f.write('\n')

# count the number of 'O's in the array
part_two = sum([row.count('O') for row in array])

print(part_one)
print(part_two)
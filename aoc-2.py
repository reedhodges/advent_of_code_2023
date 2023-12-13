with open('input-2.txt') as f:
    data = f.read().splitlines()

# split the string into a list of strings
# [game#, [observation1, observation2, observation3]]
def split_string(string):
    # first split according to each delimiter
    ans = string.split(': ')
    ans[1] = ans[1].split('; ')
    for i in range(len(ans[1])):
        ans[1][i] = ans[1][i].split(', ')
    # replace each observation with a list of the number of each color
    for i in range(len(ans[1])):
        ans[1][i] = get_color_count(ans[1][i])
    # remove the first five characters from the game number
    ans[0] = ans[0][5:]
    # convert all to int   
    ans[0] = int(ans[0])
    for i in range(len(ans[1])):
        for j in range(len(ans[1][i])):
            ans[1][i][j] = int(ans[1][i][j])
    return ans

# given a list, get the number of each color
def get_color_count(observation):
    ans = [0, 0, 0]
    for i in range(len(observation)):
        if observation[i][-4:-1] == ' re':
            ans[0] = observation[i][0:-4]
        elif observation[i][-6:-1] == ' gree':
            ans[1] = observation[i][0:-6]
        elif observation[i][-5:-1] == ' blu':
            ans[2] = observation[i][0:-5]
    return ans

# given a list of ints, return False if any exceed the limits
def check_exceed(list):
    if list[0] > 12 or list[1] > 13 or list[2] > 14:
        return False
    else:
        return True
    
# given a list of lists, return False if any exceed the limits
def check_exceed_list(list):
    for i in range(len(list[1])):
        if check_exceed(list[1][i]) == False:
            return [list[0], False]
    return [list[0], True]

def func(list):
    return check_exceed_list(split_string(list))

# apply split_string to each string in data
part_one = list(map(func, data))
# filter out all False entries
part_one = list(filter(lambda x: x[1] == True, part_one))
# get the first entry of each list
part_one = list(map(lambda x: x[0], part_one))
part_one = sum(part_one)

# given a list of strings, find the max value for each color
def find_max(list):
    ans = [0, 0, 0]
    for i in range(len(list)):
        if list[i][0] > ans[0]:
            ans[0] = list[i][0]
        if list[i][1] > ans[1]:
            ans[1] = list[i][1]
        if list[i][2] > ans[2]:
            ans[2] = list[i][2]
    return ans

part_two = list(map(split_string, data))

# apply find_max to each list 
part_two = list(map(lambda x: find_max(x[1]), part_two))
# for each list, multiply all entries together
part_two = list(map(lambda x: x[0] * x[1] * x[2], part_two))
# sum all entries
part_two = sum(part_two)

print(part_one)
print(part_two)
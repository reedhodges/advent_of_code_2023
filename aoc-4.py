# put data into 2d list
# remove first 10 characters from each line
# separate each row into two strings, using ' | ' as the delimiter
with open('input-4.txt') as f:
    data = [line[10:].split(' | ') for line in f.read().splitlines()]

# replace double spaces with single spaces and remove leading spaces
data = [[item.replace('  ', ' ').lstrip() for item in row] for row in data]

# put each string in its own list
data = [[item.split(' ') for item in row] for row in data]
# convert all to int
data = [[list(map(int, item)) for item in row] for row in data]

# function to calculate the card value
def card_value(lst):
    win_nums = lst[0]
    my_nums = lst[1]
    # check how many of the my_nums are in the win_nums
    # return 2^{n-1} times this
    matches = sum(1 for num in my_nums if num in win_nums)
    if matches == 0:
        return 0
    else:
        return 2 ** (matches - 1)

# map card_value to each row of data and sum
part_one = sum(list(map(card_value, data)))
print(part_one)

# function to calculate the numer of matches
def num_matches(lst):
    win_nums = lst[0]
    my_nums = lst[1]
    # check how many of the my_nums are in the win_nums
    # return 2^{n-1} times this
    return sum(1 for num in my_nums if num in win_nums)

# make a list of the number of matches for each card
number_of_matches = list(map(num_matches, data))

# initialize a an array with the number of copies of the card and the number of matches it has
card_array = [[1,number] for number in number_of_matches]

# now update the values according to the rules
for i in range(len(card_array)):
    matches = card_array[i][1]
    for j in range(matches):
        card_array[i+j+1][0] += card_array[i][0]

# sum the first element of each list
part_two = sum([item[0] for item in card_array])
print(part_two)
# load data from input-test.txt
with open('input-9.txt', 'r') as f:
    data = f.read().splitlines()

# split each string in the list into a list, using spaces as the delimiter
data = [string.split(' ') for string in data]
# convert all to int
data = [[int(num) for num in string] for string in data]

# given a list of numbers, return a list of the differences between successive numbers
def get_differences(list_of_numbers):
    differences = []
    for i in range(1, len(list_of_numbers)):
        differences.append(list_of_numbers[i] - list_of_numbers[i-1])
    return differences

# function to repeatedly apply get_differences until the output is a list of all zeroes
# store each output of get_differences in a list, giving a list of lists
def repeatedly_get_differences(list_of_numbers):
    differences = [list_of_numbers]
    differences.append(get_differences(list_of_numbers))
    while not all([num == 0 for num in differences[-1]]):
        differences.append(get_differences(differences[-1]))
    return differences

# function to extrapolate the next number in the list
def extrapolate_next_number(list_of_numbers):
    differences = repeatedly_get_differences(list_of_numbers)
    # append a zero to the last list in differences
    differences[-1].append(0)
    # iterate backwards through differences, adding the last two numbers in each list
    for i in range(2,len(differences)+1):
        it = -1 * i
        differences[it].append(differences[it+1][-1] + differences[it][-1])
    return differences[0][-1]

extrapolated_values = [extrapolate_next_number(data[i]) for i in range(len(data))]
part_one = sum(extrapolated_values)

# function to extrapolate backwards
def extrapolate_previous_number(list_of_numbers):
    differences = repeatedly_get_differences(list_of_numbers)
    # initialize with a zero
    answer = 0
    # iterate backwards through differences
    for i in range(2,len(differences)+1):
        it = -1 * i
        answer = differences[it][0] - answer
    return answer

extrapolated_values_backwards = [extrapolate_previous_number(data[i]) for i in range(len(data))]
part_two = sum(extrapolated_values_backwards)

print(part_one)
print(part_two)
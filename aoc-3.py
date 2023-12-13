with open('input-3.txt') as f:
    data = f.read().splitlines()


characters = ['*', '=', '-', '%', '&', '@', '$', '/', '+', '#']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# split each string into a list of its characters
data = list(map(list, data))

# go to each element of the sublists of this list and replace it with a list of itself and False
for i in range(len(data)):
    for j in range(len(data[i])):
        data[i][j] = [data[i][j], False]

# go to each element data[i][j][0] and check if it is in characters
# if it does, then replace the following entries with True as long as they are numbers:
# data[i][j-1][1], data[i][j+1][1], data[i-1][j][1], data[i+1][j][1]
# data[i-1][j-1][1], data[i-1][j+1][1], data[i+1][j-1][1], data[i+1][j+1][1]
# but only do this if the indices are valid
for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j][0] in characters:
            if j > 0:
                if data[i][j-1][0] in numbers:
                    data[i][j-1][1] = True
            if j < len(data[i])-1:
                if data[i][j+1][0] in numbers:
                    data[i][j+1][1] = True
            if i > 0:
                if data[i-1][j][0] in numbers:
                    data[i-1][j][1] = True
            if i < len(data)-1:
                if data[i+1][j][0] in numbers:
                    data[i+1][j][1] = True
            if i > 0 and j > 0:
                if data[i-1][j-1][0] in numbers:
                    data[i-1][j-1][1] = True
            if i > 0 and j < len(data[i])-1:
                if data[i-1][j+1][0] in numbers:
                    data[i-1][j+1][1] = True
            if i < len(data)-1 and j > 0:
                if data[i+1][j-1][0] in numbers:
                    data[i+1][j-1][1] = True
            if i < len(data)-1 and j < len(data[i])-1:
                if data[i+1][j+1][0] in numbers:
                    data[i+1][j+1][1] = True

# mark numbers adjacent to True numbers with True as well
# need to do this three times to get all the numbers
for k in range(3):
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j][0] in numbers and data[i][j][1] == True:
                if j == 0:
                    if data[i][j+1][0] in numbers:
                        data[i][j+1][1] = True
                elif j == len(data[i])-1:
                    if data[i][j-1][0] in numbers:
                        data[i][j-1][1] = True
                else:
                    if data[i][j-1][0] in numbers:
                        data[i][j-1][1] = True
                    if data[i][j+1][0] in numbers:
                        data[i][j+1][1] = True

# mark for removal the data[i][j] where data[i][j][0] in numbers and data[i][j][1] == False
for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j][0] in numbers and data[i][j][1] == False:
            data[i][j][1] = 'rem'

# filter out all characters that are marked for removal
for i in range(len(data)):
    data[i] = list(filter(lambda x: x[1] != 'rem', data[i]))

# mark characters that are not adjacent to numbers for removal
for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j][0] in characters or data[i][j][0] == '.':
            if j == 0:
                if data[i][j+1][0] not in numbers: 
                    data[i][j][1] = 'rem'
            elif j == len(data[i])-1:
                if data[i][j-1][0] not in numbers:
                    data[i][j][1] = 'rem'
            else:
                if data[i][j-1][0] not in numbers and data[i][j+1][0] not in numbers:
                    data[i][j][1] = 'rem'

# filter out all characters that are marked for removal
for i in range(len(data)):
    data[i] = list(filter(lambda x: x[1] != 'rem', data[i]))

# make a new list of all the data[i][j][0] entries concatenated
for i in range(len(data)):
    data[i] = ''.join([data[i][j][0] for j in range(len(data[i]))])

# replace instances of the characters with a period
for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j] in characters:
            data[i] = data[i].replace(data[i][j], '.')

# replace double periods with a single period
for i in range(len(data)):
    data[i] = data[i].replace('..', '.')

# remove leading and trailing periods
for i in range(len(data)):
    if data[i][0] == '.':
        data[i] = data[i][1:]
    if data[i][-1] == '.':
        data[i] = data[i][0:-1]

# split each string using periods as the delimiter
data = list(map(lambda x: x.split('.'), data))

# flatten the list
data = [item for sublist in data for item in sublist]
# convert all to int
data = list(map(int, data))

print(sum(data))

import pandas as pd
from itertools import combinations

# load data from input-test.txt as a numpy array
with open('input-11.txt', 'r') as f:
    data = f.read().splitlines()
# split into a list of lists
data = [list(string) for string in data]
# put each character in its own list
data = [[char for char in string] for string in data]

# convert to a pandas dataframe
df = pd.DataFrame(data)
df_copy = df.copy()

# function to identify the empty rows
def empty_rows(dataframe):
    return [i for i in range(len(dataframe)) if all([char == '.' for char in dataframe.iloc[i]])]

# function to identify the empty columns
def empty_cols(dataframe):
    return [i for i in range(len(dataframe.columns)) if all([char == '.' for char in dataframe.iloc[:, i]])]

# function to duplicate a row
def duplicate_row(dataframe, row_index):
    # get the row
    row = dataframe.iloc[row_index]
    # split and concatenate the dataframe
    return pd.concat([dataframe[:row_index+1], pd.DataFrame([row]), dataframe[row_index+1:]]).reset_index(drop=True)

# function to duplicate a column
def duplicate_col(dataframe, col_index):
    # get the column
    col = dataframe.iloc[:, col_index]
    # split and concatenate the dataframe
    return pd.concat([dataframe.iloc[:, :col_index+1], pd.DataFrame(col), dataframe.iloc[:, col_index+1:]], axis=1).reset_index(drop=True)

# apply duplicate_row to the empty rows
# initialize an iterator to keep track of the number of rows added
# because the dataframe is being modified in place, the iterator needs to be updated
# after each row is added
iterator = 0
for row_index in empty_rows(df):
    df = duplicate_row(df, row_index + iterator)
    iterator += 1

# apply duplicate_col to the empty columns
# initialize an iterator to keep track of the number of columns added
iterator = 0
for col_index in empty_cols(df):
    df = duplicate_col(df, col_index + iterator)
    iterator += 1

# rename the columns and rows
df.columns = [i for i in range(len(df.columns))]
df.index = [i for i in range(len(df))]

# search the dataframe for '#' and store the coordinates in a tuple
# append the tuple to a list
galaxies = []
for i in range(len(df)):
    for j in range(len(df.columns)):
        if df.iloc[i, j] == '#':
            galaxies.append((i, j))

# get all possible combinations of two distinct galaxies
combos = list(combinations(galaxies, 2))

# the shortest path on a grid like this is the taxicab distance, i.e.
# just the difference in the x coordinates plus the difference in the y coordinates
# initialize a list to store the distances
distances = []
for tup in combos:
    distance = abs(tup[0][0] - tup[1][0]) + abs(tup[0][1] - tup[1][1])
    distances.append(distance)

part_one = sum(distances)

# for part two, we are now adding 1 million empty rows and columns to the dataframe
# just use the original dataframe, and count the number of empty rows and columns in between the galaxies,
# and then add that number to the distance

# get the galaxies without duplication
galaxies_two = []
for i in range(len(df_copy)):
    for j in range(len(df_copy.columns)):
        if df_copy.iloc[i, j] == '#':
            galaxies_two.append((i, j))

# get all possible combinations of two distinct galaxies
combos_two = list(combinations(galaxies_two, 2))

# get the empty rows and columns for the original dataframe
em_rows = empty_rows(df_copy)
em_cols = empty_cols(df_copy)

# calculate the distance between two galaxies, given the number of times we're supposed to duplicate empty rows and columns
# this will actually work for part 1 too, with num_of_duplicates = 1
def calculate_distance(galaxy_1, galaxy_2, num_of_duplicates):
    # store the row and column numbers for both galaxies
    row_1 = galaxy_1[0]
    col_1 = galaxy_1[1]
    row_2 = galaxy_2[0]
    col_2 = galaxy_2[1]
    # apply row_1 < i < row_2 to the elements of em_rows
    # apply col_1 < i < col_2 to the elements of em_cols
    num_empty_rows_between = len([i for i in em_rows if row_1 < i < row_2 or row_2 < i < row_1])
    num_empty_cols_between = len([i for i in em_cols if col_1 < i < col_2 or col_2 < i < col_1])
    # calculate the distance
    distance = abs(row_1 - row_2) + abs(col_1 - col_2) + (num_of_duplicates*num_empty_rows_between) + (num_of_duplicates*num_empty_cols_between)
    return distance

# apply calculate_distance to the pair in combos_two
distances_two = []
for pair in combos_two:
    distances_two.append(calculate_distance(pair[0], pair[1], 999999))

part_two = sum(distances_two)

print(part_one)
print(part_two)

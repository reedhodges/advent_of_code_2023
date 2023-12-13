import pandas as pd

# data from input-test.txt as a string
with open('input-13.txt', 'r') as f:
    input_data = f.read()

# function to convert grid string to a DataFrame
def grid_to_dataframe(grid_string):
    rows = grid_string.split('\n')
    df = pd.DataFrame([list(row) for row in rows])
    return df

# split the input data into grids
grids = input_data.strip().split('\n\n')

# create a DataFrame for each grid and store in a list
dataframes = [grid_to_dataframe(grid) for grid in grids]

def split_vertically(df, N):
    '''
    Splits a dataframe vertically into two dataframes, after the N-th column.  Removes
    the extra columns and flips the second dataframe.
    '''
    df1 = df.iloc[:, :N]
    df2 = df.iloc[:, N:]
    # number of columns of df1 and df2
    num_cols_1 = df1.shape[1]
    num_cols_2 = df2.shape[1]
    # remove columns according to whether df1 or df2 has more columns
    if num_cols_1 < num_cols_2:
        # remove all but the first num_cols_1 cols of df2
        df2 = df2.iloc[:, :num_cols_1]
    elif num_cols_1 > num_cols_2:
        # remove all but the last num_cols_2 cols of df1
        df1 = df1.iloc[:, -num_cols_2:]
    else:
        # case where num_cols_1 == num_cols_2, do nothing
        pass 
    # reverse the column order in df2
    df2 = df2.iloc[:, ::-1]  
    # give df2 the same index and column names as df1
    # this is necessary for the equals method to work
    df2.index = df1.index
    df2.columns = df1.columns 
    return df1, df2

def split_horizontally(df, N):
    '''
    Splits a dataframe horizontally into two dataframes, after the N-th row.  Removes
    the extra rows and flips the second dataframe.
    '''
    df1 = df.iloc[:N, :]
    df2 = df.iloc[N:, :]
     # number of rows of df1 and df2
    num_rows_1 = df1.shape[0]
    num_rows_2 = df2.shape[0]
    # remove rows according to whether df1 or df2 has more rows
    if num_rows_1 < num_rows_2:
        # remove all but the first num_rows_1 rows of df2
        df2 = df2.iloc[:num_rows_1, :]
    elif num_rows_1 > num_rows_2:
        # remove all but the last num_rows_2 rows of df1
        df1 = df1.iloc[-num_rows_2:, :]
    else:
        # case where num_rows_1 == num_rows_2, do nothing
        pass 
    # reverse the row order in df2
    df2 = df2.iloc[::-1, :]
    # give df2 the same index and column names as df1
    # this is necessary for the equals method to work
    df2.index = df1.index
    df2.columns = df1.columns        
    return df1, df2

def check_mirror_vertical(df, N):
    '''
    Checks whether a dataframe is a mirror image of itself, with the 
    point of reflection after the N-th column.
    '''
    df1, df2 = split_vertically(df, N) 
    # check whether df1 and df2 are equal, this means they are mirror images
    return df1.equals(df2)

def check_mirror_horizontal(df, N):
    '''
    Checks whether a dataframe is a mirror image of itself, with the 
    point of reflection after the N-th row.
    '''
    df1, df2 = split_horizontally(df, N)
    # check whether df1 and df2 are equal, this means they are mirror images
    return df1.equals(df2)

def check_all_mirrors(df):
    '''
    Looks for a number N where either check_mirror_vertical or check_mirror_horizontal
    returns True.  Returns (N,i) if found, where i is the weight for
    the two types of mirrors, otherwise returns None.
    '''
    # check for vertical mirrors
    for N in range(1, df.shape[1]):
        if check_mirror_vertical(df, N):
            return (N,1)
    # check for horizontal mirrors
    for N in range(1, df.shape[0]):
        if check_mirror_horizontal(df, N):
            return (N,100)
    # if no mirrors are found, return None
    return None

# check all grids for mirrors
part_one_list = [check_all_mirrors(df) for df in dataframes]
part_one = sum(x[0]*x[1] for x in part_one_list)

def compare_two_dataframes(df1, df2):
    '''
    Compares two dataframes, and returns the number of cells that are different.
    '''
    # check that the two dataframes have the same shape
    if df1.shape != df2.shape:
        raise ValueError('The two dataframes must have the same shape.')
    else:
        # check which cells are different
        diff = df1 != df2
        # count the number of cells that are different
        return diff.sum().sum()
    
def check_for_smudges(df):
    '''
    Applies split_vertically(df,N) and split_horizontally(df,N) to the dataframe 
    and applies compare_two_dataframes to the resulting dataframes, until the output
    of compare_two_dataframes is 1.  Returns (N,i) where i is the weight for 
    horizontal/vertical.
    '''
    # check for vertical smudges
    for N in range(1, df.shape[1]):
        df1, df2 = split_vertically(df, N)
        if compare_two_dataframes(df1, df2) == 1:
            return (N,1)
    # check for horizontal smudges
    for N in range(1, df.shape[0]):
        df1, df2 = split_horizontally(df, N)
        if compare_two_dataframes(df1, df2) == 1:
            return (N,100)
    # if no smudges are found, return None
    return None

# check all grids for smudges
part_two_list = [check_for_smudges(df) for df in dataframes]
part_two = sum(x[0]*x[1] for x in part_two_list)

print('Part One:', part_one)
print('Part Two:', part_two)


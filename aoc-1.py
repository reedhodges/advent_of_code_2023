# import txt file as a list
with open('input-1.txt') as f:
    data = f.read().splitlines()

integers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
integers_written = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
# list of integers written backwards
integers_reversed = [integer[::-1] for integer in integers_written]

# create a dictionary to map integers to their written form
integer_dict = {word: digit for word, digit in zip(integers_written, integers)}
# add the reverse of each entry to the dictionary
integer_dict.update({word: digit for word, digit in zip(integers_reversed, integers)})

# start with the first character, look at the it and the next four characters;
# check if any substring of it matches any of the keys in the dictionary
# if so, replace it with the corresponding value and stop the loop
# if not, move on to the next character and repeat
# return the resulting string
def func(string):
    ans = string
    for i in range(len(ans)):
        for j in range(6):
            if ans[i:i+j] in integer_dict.keys():
                ans = ans.replace(ans[i:i+j], integer_dict[ans[i:i+j]])
                break
    # reverse the string and do it again, so we can get the last integer written out.
    # creat a new variable so we don't overwrite the original string, which would fail
    # for cases like 'twone' since the first and last written out integers both use "o"
    ans_rev = string[::-1]
    for i in range(len(ans_rev)):
        for j in range(6):
            if ans_rev[i:i+j] in integer_dict.keys():
                ans_rev = ans_rev.replace(ans_rev[i:i+j], integer_dict[ans_rev[i:i+j]])
                break
    # use map() to convert the strings to a list of characters
    ans = list(map(str, ans))
    ans_rev = list(map(str, ans_rev))
    # use filter() to remove all non-integers
    ans = list(filter(lambda x: x in integers, ans))
    ans_rev = list(filter(lambda x: x in integers, ans_rev))
    # concatenate first entries of both, and convert to int
    ans = int(ans[0] + ans_rev[0])
    return ans

print(sum([func(string) for string in data]))
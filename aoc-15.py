with open('input-15.txt') as f:
    data = f.read()

# separate the data into a list of strings using comma as delimiter
data = data.split(',')

def hash_algo(st):
    '''
    Function that applies the HASH algorithm to a string.
    '''
    # split string into a list of characters
    st = list(st)
    # get the ASCII values of each character
    st = [ord(c) for c in st]
    # initialize answer
    ans = 0
    # iterate over the list
    for ch in st:
        ans += ch
        ans = 17 * ans
        ans = ans % 256
    return ans

# apply hash_algo() to each string in data
part_one_list = [hash_algo(st) for st in data]

part_one = sum(part_one_list)
print('Part one:', part_one)

def split_step(st):
    '''
    Function to take a string and split it into the lens label, box id, and focal length (if applicable).
    '''
    operation_chars = ['-', '=']
    # lens label is all the characters in the string up to the first operation character
    lens_label = ''
    for ch in st:
        if ch in operation_chars:
            break
        lens_label += ch
    # box id is the hash algorithm applied to the lens label
    box_id = hash_algo(lens_label)
    # if the string contains an '=', the focal length is the rest of the string after the '='
    if '=' in st:
        focal_length = int(st[st.index('=') + 1:])
        return (lens_label, box_id, focal_length)
    else:
        return (lens_label, box_id)
    
# initialize dictionary with box contents
box_contents = {}
# make the keys of box_contents the integers from 0 to 255 inclusive, and the values empty lists
for i in range(256):
    box_contents[i] = []
    
def remove_lens(st):
    '''
    Function to remove a lens from its box.
    '''
    # split the string into the lens label and the box id
    (lens_label, box_id) = split_step(st)
    # if the box has a value (a,b) with a == lens_label, remove the tuple from the list
    box_contents[box_id] = [tup for tup in box_contents[box_id] if tup[0] != lens_label]
    return

def add_lens(st):
    '''
    Function to add a lens to its box.
    '''
    # split the string into the lens label and the box id
    (lens_label, box_id, focal_length) = split_step(st)
    # if box is empty, append the tuple (lens_label, focal_length) to the list
    if len(box_contents[box_id]) == 0:
        box_contents[box_id].append((lens_label, focal_length))
        return
    # iterate over the list of tuples in the box
    for i in range(len(box_contents[box_id])):
        # if the box has a value (a,b) with a == lens_label, replace that element with
        # (lens_label, focal_length)
        if box_contents[box_id][i][0] == lens_label:
            box_contents[box_id][i] = (lens_label, focal_length)
            return
    # if the box does not have a value (a,b) with a == lens_label, append the tuple
    # (lens_label, focal_length) to the list
    box_contents[box_id].append((lens_label, focal_length))
        
def add_or_remove_lens(st):
    '''
    Function to add or remove a lens from its box.
    '''
    # if the string contains a '-', call remove_lens()
    if '-' in st:
        remove_lens(st)
    # if the string contains a '=', call add_lens()
    elif '=' in st:
        add_lens(st)
    return

def part_two_ans(box, box_id):
    '''
    Function to calculate the contribution from a single box.
    '''
    # if the box is empty, return 0
    if len(box) == 0:
        return 0
    # initialize answer
    ans = 0
    for i in range(len(box)):
        a1 = box_id + 1
        a2 = i + 1
        a3 = box[i][1]
        ans += a1 * a2 * a3
    return ans

# apply add_or_remove_lens() to each string in data
for st in data:
    add_or_remove_lens(st)

# apply part_two_ans() to each box in box_contents
part_two = 0
for box_id in box_contents:
    part_two += part_two_ans(box_contents[box_id], box_id)
    
print('Part two:', part_two)
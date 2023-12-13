from itertools import combinations_with_replacement

# input data from input-test.txt
with open('input-7.txt', 'r') as f:
    hands = f.read().splitlines()

# split each string in the list into two strings, one for each hand
hands = [x.split(' ') for x in hands]

# list of cards without Js
cards_no_J = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']

# dictionary to convert hand classification to a number
card_hand_dict = {
    'high card': 1,
    'one pair': 2,
    'two pairs': 3,
    '3 of a kind': 4,
    'full house': 5,
    '4 of a kind': 6,
    '5 of a kind': 7
}

# dictionary with rankings of card values
card_value_dict = {
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    'T': 9,
    'J': 10,
    'Q': 11,
    'K': 12,
    'A': 13
}

# function to tally the characters in a string
def tally_characters(string):
    tally = {}
    for x in string:
        # if the character is not in the dictionary, add it
        if x not in tally:
            tally[x] = 1
        # if the character is in the dictionary, increment its value
        else:
            tally[x] += 1
    return tally

# function to classify a hand
def classify_hand(hand):
    tally = tally_characters(hand)
    # dictionary length is 1: can only be 5 of a kind
    if len(tally) == 1:
        return 7
    # dictionary length is 2: can only be 4 of a kind or full house
    elif len(tally) == 2:
        # if and of the values are 4, it is 4 of a kind
        if 4 in tally.values():
            return 6
        # otherwise, it is a full house
        else:
            return 5
    # dictionary length is 3: can only be 3 of a kind or two pairs
    elif len(tally) == 3:
        # if any of the values are 3, it is 3 of a kind
        if 3 in tally.values():
            return 4
        # otherwise, it is two pairs
        else:
            return 3
    # dictionary length is 4: can only be one pair
    elif len(tally) == 4:
        return 2
    # dictionary length is 5: can only be high card
    elif len(tally) == 5:
        return 1

# duplicate the first element
hands = [[x[0], x[0], x[1]] for x in hands]

# make a copy for part two
hands_two = hands

# apply classify_hand to sublist[1] for each sublist in hands
# also convert sublist[2] to int
hands = [[x[0], classify_hand(x[1]), int(x[2])] for x in hands]

# split into sublists by hand classification
hands = [[x for x in hands if x[1] == n] for n in range(1, 8)]

# now need to sort the sublists by sublist[0] according to card_value_dict
# first define a function to compare two elements
def is_A_greater_than_B(A, B, dict):
    # split the strings into lists of their characters
    A = list(A)
    B = list(B)
    for i in range(len(A)):
        # if the characters are equal, move on to the next character
        if A[i] == B[i]:
            continue
        # if the characters are not equal, compare their values
        else:
            # if the value of B is greater than the value of A, return False
            if dict[B[i]] > dict[A[i]]:
                return False
            # if the value of B is less than the value of A, return True
            else:
                return True
            
# bubble sort a list by sublist[0] using is_A_greater_than_B
def bubble_sort_by_card_value(list_to_sort, dict):
    n = len(list_to_sort)
    for i in range(n):
        for j in range(0, n - i - 1):
            if is_A_greater_than_B(list_to_sort[j][0], list_to_sort[j + 1][0], dict):
                list_to_sort[j], list_to_sort[j + 1] = list_to_sort[j + 1], list_to_sort[j]
    return list_to_sort

# apply bubble_sort_by_card_value to each sublist in hands
hands = [bubble_sort_by_card_value(x, card_value_dict) for x in hands]

# flatten hands
hands = [x for sublist in hands for x in sublist]

# get the answer for part one
# sum rank*bid
part_one = sum([(i+1) * hands[i][2] for i in range(len(hands))])

# for part two, have a new dictionary with redefined J value
card_value_dict_two = {
    'J': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    'T': 9,
    'Q': 11,
    'K': 12,
    'A': 13
}

# now have a new classify_hand function that takes into account J being a wildcard
def classify_hand_with_wildcard(hand):
    # check if there are any Js in the hand
    if 'J' not in hand:
        # if not, just use regular classify_hand
        return classify_hand(hand)
    else:
        # count the number of Js in the hand
        num_Js = hand.count('J')
        # get the combinations of the elements of cards_no_J
        combos = combinations_with_replacement(cards_no_J, num_Js)
        # replace the Js in hand with each combination
        all_hand_combos = [hand.replace('J', ''.join(x)) for x in combos]
        # return the best classification of the hand
        return max([classify_hand(x) for x in all_hand_combos])

# apply classify_hand_with_wildcard to sublist[1] for each sublist in hands_two
# also convert sublist[2] to int
hands_two = [[x[0], classify_hand_with_wildcard(x[1]), int(x[2])] for x in hands_two]

# split into sublists by hand classification
hands_two = [[x for x in hands_two if x[1] == n] for n in range(1, 8)]

# apply bubble_sort_by_card_value to each sublist in hands_two
hands_two = [bubble_sort_by_card_value(x, card_value_dict_two) for x in hands_two]

# flatten
hands_two = [x for sublist in hands_two for x in sublist]

# get the answer for part two
# sum rank*bid
part_two = sum([(i+1) * hands_two[i][2] for i in range(len(hands_two))])

print(part_one)
print(part_two)
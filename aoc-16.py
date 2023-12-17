from collections import deque

with open('input-16.txt') as f:
    data = f.read().splitlines()
    # split each line into a list of its characters
data = [list(line) for line in data]
# initialize a dictionary with coordinates
coordinates = {}
# iterate over the data
for y in range(len(data)):
    for x in range(len(data[y])):
        # add the coordinates to the dictionary
        coordinates[(x, y)] = data[y][x]

# initialize dictionary of coordinates visited
visited = {keys: '.' for keys in coordinates.keys()}

# initialize a dictionary of coordinates
# values will be the directions we've already headed in
directions = {keys: [] for keys in coordinates.keys()}

class beam:
    def __init__(self, pos, di):
        # position in the grid
        self.pos = pos
        # direction of the beam
        self.di = di
        self.x = pos[0]
        self.y = pos[1]
        self.xdir = di[0]
        self.ydir = di[1]
        # type of obstacle at the beam's location
        self.obstacle = coordinates[(self.x, self.y)]
        # initialize additional beams to be created
        self.new_beams = []
        # mark the beam's initial position as visited
        self.mark_visited()

    def update_direction(self):
        '''
        Function that updates the direction of the beam.  Also creates new beams if 
        the beam splits.
        '''
        if self.obstacle == '.':
            self.di = self.di
        elif self.obstacle == '/':
            self.di = [-self.ydir, -self.xdir]
        elif self.obstacle == '\\':
            self.di = [self.ydir, self.xdir]
        elif self.obstacle == '|':
            if self.ydir == 0:
                # include cases if we are at the top or bottom edge of the grid
                if self.y == 0:
                    self.di = [0, 1]
                if self.y == len(data) - 1:
                    self.di = [0, -1]
                else:
                    self.di = [0, 1]
                    self.new_beams.append(beam([self.x, self.y], [0, -1]))
            else:
                self.di = self.di
        elif self.obstacle == '-':
            if self.xdir == 0:
                # include cases if we are at the left or right edge of the grid
                if self.x == 0:
                    self.di = [1, 0]
                if self.x == len(data[0]) - 1:
                    self.di = [-1, 0]
                else:
                    self.di = [1, 0]
                    self.new_beams.append(beam([self.x, self.y], [-1, 0]))
            else:
                self.di = self.di
        else:
            print('Error: invalid obstacle')
            print(self.obstacle)
            print(self.pos)
            print(self.di)
            exit()

    def move(self):
        '''
        Function that moves the beam, updates the obstacle, and marks the new location as visited.
        '''
        # update the beam's direction
        self.update_direction()
        self.xdir = self.di[0]
        self.ydir = self.di[1]
        # add this direction to the list of directions we've already headed in
        directions[(self.x, self.y)].append((self.xdir, self.ydir))
        # move the beam
        self.x += self.xdir
        self.y += self.ydir
        self.pos = [self.x, self.y]
        # update the obstacle
        self.obstacle = coordinates[(self.x, self.y)]
        # mark new location as visited
        self.mark_visited()

    def is_exited(self):
        '''
        Function that checks whether the beam has exited the grid.
        '''
        # update direction first
        self.update_direction()
        # check if the beam will exit
        if self.x + self.di[0] < 0 or self.x + self.di[0] >= len(data[0]) or self.y + self.di[1] < 0 or self.y + self.di[1] >= len(data):
            return True
        else:
            return False
        
    def is_in_grid(self):
        '''
        Function that checks whether the beam is still in the grid.
        '''
        return 0 <= self.x < len(data[0]) and 0 <= self.y < len(data)
        
    def mark_visited(self):
        '''
        Function that marks the coordinates visited by the beam.
        '''
        visited[(self.x, self.y)] = '#'

    def already_been_there(self):
        '''
        Function that checks whether we have already headed in this direction.
        '''
        self.update_direction()
        proposed_dir = (self.di[0], self.di[1])
        return proposed_dir in directions[(self.x, self.y)]


# initialize a queue for the beams
queue = deque([beam([0, 0], [1, 0])])
# process beams until the queue is empty
while queue:
    current_beam = queue.popleft()

    # as long as the beam will not exit and we haven't been there before, move the beam
    while current_beam.is_in_grid() and not current_beam.is_exited() and not current_beam.already_been_there():
        current_beam.move()
        # add the new beams to the queue
        queue.extend(current_beam.new_beams)
        # clear the new beams
        current_beam.new_beams = []

# print the elements of visited in a grid
#for y in range(len(data)):
#    for x in range(len(data[y])):
#        print(visited[(x, y)], end='')
#    print()

# count the number of '#' in visited
part_one = sum([1 for key in visited.keys() if visited[key] == '#'])
print(f"Part one: {part_one}")

# initialize energized squares
energized = []

# top edge
for x in range(len(data[0])):
    # re-initialize the visited dictionary and directions dictionary
    visited = {keys: '.' for keys in coordinates.keys()}
    directions = {keys: [] for keys in coordinates.keys()}
    # initialize a queue for the beams
    queue = deque([beam([x, 0], [0, 1])])
    # process beams until the queue is empty
    while queue:
        current_beam = queue.popleft()

        # as long as the beam will not exit and we haven't been there before, move the beam
        while current_beam.is_in_grid() and not current_beam.is_exited() and not current_beam.already_been_there():
            current_beam.move()
            # add the new beams to the queue
            queue.extend(current_beam.new_beams)
            # clear the new beams
            current_beam.new_beams = []
    energized.append(sum([1 for key in visited.keys() if visited[key] == '#']))
    

# bottom edge
for x in range(len(data[0])):
    # re-initialize the visited dictionary and directions dictionary
    visited = {keys: '.' for keys in coordinates.keys()}
    directions = {keys: [] for keys in coordinates.keys()}
    # initialize a queue for the beams
    queue = deque([beam([x, len(data)-1], [0, -1])])
    # process beams until the queue is empty
    while queue:
        current_beam = queue.popleft()

        # as long as the beam will not exit and we haven't been there before, move the beam
        while current_beam.is_in_grid() and not current_beam.is_exited() and not current_beam.already_been_there():
            current_beam.move()
            # add the new beams to the queue
            queue.extend(current_beam.new_beams)
            # clear the new beams
            current_beam.new_beams = []
    energized.append(sum([1 for key in visited.keys() if visited[key] == '#']))

# left edge
for y in range(len(data)):
    # re-initialize the visited dictionary and directions dictionary
    visited = {keys: '.' for keys in coordinates.keys()}
    directions = {keys: [] for keys in coordinates.keys()}
    # initialize a queue for the beams
    queue = deque([beam([0, y], [1, 0])])
    # process beams until the queue is empty
    while queue:
        current_beam = queue.popleft()

        # as long as the beam will not exit and we haven't been there before, move the beam
        while current_beam.is_in_grid() and not current_beam.is_exited() and not current_beam.already_been_there():
            current_beam.move()
            # add the new beams to the queue
            queue.extend(current_beam.new_beams)
            # clear the new beams
            current_beam.new_beams = []
    energized.append(sum([1 for key in visited.keys() if visited[key] == '#']))

# right edge
for y in range(len(data)):
    # re-initialize the visited dictionary and directions dictionary
    visited = {keys: '.' for keys in coordinates.keys()}
    directions = {keys: [] for keys in coordinates.keys()}
    # initialize a queue for the beams
    queue = deque([beam([len(data[0])-1, y], [-1, 0])])
    # process beams until the queue is empty
    while queue:
        current_beam = queue.popleft()

        # as long as the beam will not exit and we haven't been there before, move the beam
        while current_beam.is_in_grid() and not current_beam.is_exited() and not current_beam.already_been_there():
            current_beam.move()
            # add the new beams to the queue
            queue.extend(current_beam.new_beams)
            # clear the new beams
            current_beam.new_beams = []
    energized.append(sum([1 for key in visited.keys() if visited[key] == '#']))

part_two = (max(energized))
print(f"Part two: {part_two}")
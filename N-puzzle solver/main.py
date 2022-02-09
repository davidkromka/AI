import datetime


# representation of node
class Node:
    def __init__(self, data, next_node):
        self.data = data
        self.next = next_node


class Game:
    node = None
    last_node = None
    all_nodes = []
    to_do = []
    heuristic = None

    def __init__(self, input_area, goal):
        self.input = input_area
        self.goal = goal

    # count of bad positioned frames
    def heuristic1(self, area):
        bad = 0
        for i in range(len(area)):
            for q in range(len(area[i])):
                if area[i][q] != self.goal[i][q] and area[i][q] != 0:
                    bad += 1
        return bad

    # sum of distances from right position
    def heuristic2(self, area):
        bad = 0
        for i in range(len(area)):
            for q in range(len(area[i])):
                for m in range(len(self.goal)):
                    if area[i][q] in self.goal[m] and area[i][q] != 0:
                        n = self.goal[m].index(area[i][q])
                        bad += abs(i - m) + abs(q - n)
        return bad

    def move(self):
        # moves with empty frame
        def up():
            if y == 0:
                return 0
            cp = [row[:] for row in self.input]
            cp[y][x], cp[y - 1][x] = cp[y - 1][x], cp[y][x]
            return cp

        def down():
            if y == len(self.input) - 1:
                return 0
            cp = [row[:] for row in self.input]
            cp[y][x], cp[y + 1][x] = cp[y + 1][x], cp[y][x]
            return cp

        def right():
            if x == len(self.input[0]) - 1:
                return 0
            cp = [row[:] for row in self.input]
            cp[y][x], cp[y][x + 1] = cp[y][x + 1], cp[y][x]
            return cp

        def left():
            if x == 0:
                return 0
            cp = [row[:] for row in self.input]
            cp[y][x], cp[y][x - 1] = cp[y][x - 1], cp[y][x]
            return cp

        # choosing the best steps according heuristic
        def best_move(steps):
            steps_list = []
            best_value = None
            for order in range(len(steps)):
                if steps[order] == 0:
                    continue
                heuristic_result = self.heuristic(steps[order])
                # we don't want visited nodes again
                if (steps[order] not in self.all_nodes) and (best_value is None or heuristic_result <= best_value):
                    if heuristic_result == best_value:
                        steps_list.append(order)
                    else:
                        steps_list.clear()
                        steps_list.append(order)
                    best_value = heuristic_result
            return steps_list

        # position of empty frame
        for i in range(len(self.input)):
            if 0 in self.input[i]:
                y, x = i, self.input[i].index(0)
                break
        # all possible steps
        up = up()
        down = down()
        right = right()
        left = left()
        result = [up, down, right, left]
        # only the best steps
        steps_list = best_move(result)
        if len(steps_list) == 0:
            return None
        nodes = []
        for item in steps_list:
            nodes.append(result[item])
        return nodes

    def search(self, step_list):
        for item in step_list:
            self.to_do.append(item)  # nodes to explore
        while len(self.to_do) != 0:
            self.input = self.to_do.pop()
            self.node = Node(self.input, self.last_node)
            self.last_node = self.node
            self.all_nodes.append(self.input)  # list of all visited nodes
            if self.heuristic(self.input) != 0:
                step_list = self.move()  # number positions to explore
                if step_list is None:
                    continue
                for step in step_list:
                    self.to_do.append(step)
            # search successful
            else:
                return self.input
            # stop if search is too long
            if len(self.all_nodes) > 25000:
                return 0
        return 0

    def start(self):
        self.all_nodes.clear()
        print('Počiatočné rozloženie: ')
        for row in self.input:
            print(f'{row}')
        # measuring time of function execution
        time_start = datetime.datetime.now()
        result = self.search([self.input])
        time_end = datetime.datetime.now()
        time_result = (time_end - time_start).total_seconds() * 1000
        # printing results and nodes
        if result != 0:
            print('Koncové rozloženie: ')
            for row in self.input:
                print(f'{row}')
        else:
            print('Výsledok nebol nájdený')
        print(f'Čas hľadania: {round(time_result, 3)} ms')
        actual = self.node
        count = 0
        while actual is not None:
            count += 1
            actual = actual.next
        print(f'Počet krokov: {count - 1}')


# starting point of program, UI
if __name__ == '__main__':
    while True:
        print("Rozmer hlavolamu")
        x = int(input("Zadajte horizontálnu dĺžku: "))
        y = int(input("Zadajte vertikálnu dĺžku: "))

        while True:
            values = (input(f'Zadajte {x * y} hodnôt hlavolamu oddelených čiarkou, 0 na prázdne políčko: '))
            values = list(values.split(','))
            values = [int(i) for i in values]
            if len(values) == x * y:
                break
            print('Nesprávny vstup')

        area = []
        index = 0
        for i in range(y):
            area.append([])
            for q in range(x):
                area[i].append(values[index])
                index += 1
        index = 0
        while True:
            values = (input(f'Zadajte {x * y} hodnôt cieľového rozloženia '
                            f'oddelených čiarkou, 0 na prázdne políčko: '))
            values = list(values.split(','))
            values = [int(i) for i in values]
            if len(values) == x * y:
                break
            print('Nesprávny vstup')

        goal = []
        index = 0
        for i in range(y):
            goal.append([])
            for q in range(x):
                goal[i].append(values[index])
                index += 1
        index = 0

        new_game = Game(area, goal)
        while True:
            h = input("Heuristika '1' alebo '2': ")
            if h == '1':
                h = new_game.heuristic1
                break
            if h == '2':
                h = new_game.heuristic2
                break
        new_game.heuristic = h
        new_game.start()
        step = input("Na výpis krokov stlačte 'v' na ukončenie stlačte 'e', na pokračovanie 'p': ")
        if step == 'v':
            actual = new_game.node
            while actual is not None:
                for row in actual.data:
                    print(f'{row}')
                print('')
                actual = actual.next
        elif step == 'e':
            break

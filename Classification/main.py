import random
import math
import matplotlib.pyplot as plt
import time


class Main:

    def __init__(self):
        # starting points
        r = [[-4500, -4400], 'r'], [[-4100, -3000], 'r'], [[-1800, -2400], 'r'], \
            [[-2500, -3400], 'r'], [[-2000, -1400], 'r']
        g = [[+4500, -4400], 'g'], [[+4100, -3000], 'g'], [[+1800, -2400], 'g'], \
            [[+2500, -3400], 'g'], [[+2000, -1400], 'g']
        b = [[-4500, +4400], 'b'], [[-4100, +3000], 'b'], [[-1800, +2400], 'b'], \
            [[-2500, +3400], 'b'], [[-2000, +1400], 'b']
        p = [[+4500, +4400], 'p'], [[+4100, +3000], 'p'], [[+1800, +2400], 'p'], \
            [[+2500, +3400], 'p'], [[+2000, +1400], 'p']
        self.array = []
        self.array.extend(r+g+b+p)

        #  add to visualization
        choose = {'r': 'red', 'g': 'green', 'b': 'blue', 'p': 'purple'}
        for i in range(len(self.array)):
            plt.scatter(self.array[i][0][0], self.array[i][0][1], color=choose[self.array[i][1]])

    def classify(self, array, k):
        x, y = array[0], array[1]
        points = []
        colors = []
        choose = {'r': 'red', 'g': 'green', 'b': 'blue', 'p': 'purple'}
        for element in self.array:
            distance = math.sqrt((x - element[0][0]) ** 2 + (y - element[0][1]) ** 2)
            #  choose k point with shortest distances
            if len(points) < k:
                points.append([element, distance])
                points = sorted(points, key=lambda dst: dst[1])
            elif distance < points[-1][1]:
                points[-1] = [element, distance]
                points = sorted(points, key=lambda dst: dst[1])
        #  choose color
        for element in points:
            colors.append(element[0][1])
        color = max(sorted(set(colors), key=colors.index), key=colors.count)
        self.array.append([[x, y], color])
        plt.scatter(x, y, color=choose[color])
        return color

    def generate(self):
        array = []
        n = 20000
        # creating new points
        for i in range(n):
            prop = random.randint(1, 100)
            if prop == 100:
                while True:
                    x = random.randint(-5000, 5000)
                    y = random.randint(-5000, 5000)
                    # check if duplicity
                    if not [x, y] in array:
                        break
            else:
                turn = i % 4
                colors = {0: [[-5000, 499], [-5000, 499]],
                          1: [[-501, 5000], [-5000, 499]],
                          2: [[-5000, 499], [-501, 5000]],
                          3: [[-501, 5000], [-501, 5000]]}
                color = colors[turn]
                while True:
                    x = random.randint(color[0][0], color[0][1])
                    y = random.randint(color[1][0], color[1][1])
                    if not [x, y] in array:
                        break
            array.append([x, y])
        for k in [1, 3, 7, 15]:
            start = time.time()
            ok = 0
            for i in range(n):
                turn = i % 4
                #  right color
                colors = {0: 'r', 1: 'g', 2: 'b', 3: 'p'}
                color = colors[turn]
                if self.classify(array[i], k) == color:
                    ok += 1
            # print results and visualization
            print(f'k = {k}, {round((ok/n*100), 2)} % úspešnosť.')
            stop = time.time()-start
            print(f'Čas vykonania pre k = {k}: {stop} s')
            plt.title(f'k = {k}, {round((ok/n*100), 2)} % úspešnosť.')
            plt.show()
            self.array = self.array[:20]
        return 0


if __name__ == '__main__':
    program = Main()
    program.generate()

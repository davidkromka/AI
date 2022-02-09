import random
import matplotlib.pyplot as plt
import numpy as np


class Chromosome:

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.treasures_found = 0


class VirtualMachine:
    treasures_found = 0

    # realize virtual machine instructions
    def machine_work(self, surface, draw, chromosome):
        self.treasures_found = 0
        cp_grid = [row[:] for row in surface.grid]
        cp_chromosome = chromosome[:]
        x, y = surface.x, surface.y
        count = 0
        iterate = 0
        all_steps = []

        while count < 500:
            count += 1
            cell = cp_chromosome[iterate]
            # increment
            if cell[:2] == '00':
                if int(cp_chromosome[int(cell[2:], 2)], 2) < 255:
                    cp_chromosome[int(cell[2:], 2)] = format((int(cp_chromosome[int(cell[2:], 2)], 2) + 1), '08b')
                else:
                    cp_chromosome[int(cell[2:], 2)] = format(0, '08b')
            # decrement
            elif cell[:2] == '01':
                if int(cp_chromosome[int(cell[2:], 2)], 2) > 0:
                    cp_chromosome[int(cell[2:], 2)] = format((int(cp_chromosome[int(cell[2:], 2)], 2) - 1), '08b')
                else:
                    cp_chromosome[int(cell[2:], 2)] = format(255, '08b')
            # jump
            elif cell[:2] == '10':
                iterate = int(cell[2:], 2)
                continue
            # write
            elif cell[:2] == '11':
                steps = {'00': 'h', '01': 'd', '10': 'p', '11': 'l'}
                step = steps[cell[6:]]
                all_steps.append(step)
                if cp_grid[y][x] == 1:
                    cp_grid[y][x] = 0
                    # treasure found
                    self.treasures_found += 1
                    if self.treasures_found == tr_count and draw == 1:
                        print('Mriežka po hľadaní:')
                        for row in cp_grid:
                            print(row)
                        print('Postupnosť krokov:')
                        print(all_steps)
                        print('')
                        return self.treasures_found
                if step == 'h' and y != 0:
                    y -= 1
                elif step == 'd' and y != surface.h - 1:
                    y += 1
                elif step == 'p' and x != surface.w - 1:
                    x += 1
                elif step == 'l' and x != 0:
                    x -= 1
                else:
                    if draw == 1:
                        print('Mriežka po hľadaní:')
                        for row in cp_grid:
                            print(row)
                        print('Postupnosť krokov:')
                        print(all_steps)
                        print('')
                    return self.treasures_found

            if iterate < 63:
                iterate += 1
            else:
                iterate = 0
        if draw == 1:
            print('Mriežka po hľadaní:')
            for row in cp_grid:
                print(row)
            print('Postupnosť krokov:')
            print(all_steps)
            print('')

        if cp_grid[y][x] == 1:
            cp_grid[y][x] = 0
            self.treasures_found += 1
        return self.treasures_found


class Area:

    def __init__(self, w, h, x, y, treasures):
        self.grid = [[0] * w for _ in range(h)]
        for treasure in treasures:
            self.grid[treasure[1]][treasure[0]] = 1
        # search position
        self.x, self.y = x, y
        # width, height
        self.w, self.h = w, h
        self.treasures_c = len(treasures)


class Main:
    fitness_chart = []

    def roulette(self, pop):
        parents = []
        parent = []
        pop_sum = 0
        for element in pop:
            pop_sum += element.treasures_found

        for w in range(n):
            r = random.randint(0, pop_sum)
            s = 0
            # s is sum of fitness in loop
            # if r>s, chromosome is selected as a parent
            for chromosome in pop:
                s += chromosome.treasures_found
                if s > r and chromosome not in parent:
                    parent.append(chromosome.chromosome)
                    break
            if len(parent) == 2:
                parents.append([parent.pop(0), parent.pop(0)])
        self.fitness_chart.append(pop_sum)
        return parents

    # select parents chromosomes
    def duel(self, pop):
        parents = []
        parent = []
        pop_sum = 0
        # 2 random chromosomes are selected, the best is selected
        for element in pop:
            pop_sum += element.treasures_found
        for i in range(n):
            fighter1 = random.choice(pop)
            fighter2 = random.choice(pop)
            if fighter1.treasures_found > fighter2.treasures_found:
                parent.append(fighter1.chromosome)
            else:
                parent.append(fighter2.chromosome)
            if len(parent) == 2:
                parents.append([parent.pop(0), parent.pop(0)])
        self.fitness_chart.append(pop_sum)
        return parents

    def cross(self, chromosomes):
        new_pop = []
        for pair in chromosomes:
            div = random.randint(20, 45)
            new_pop.append(pair[0][:div] + pair[1][div:])
            new_pop.append(pair[1][:div] + pair[0][div:])
        # mutation
        for chromosome in new_pop:
            mut = random.randint(0, 5)
            for w in range(mut):
                chromosome[random.randint(0, 63)] = format(random.randint(0, 255), '08b')
        return new_pop

    def main(self):
        # creating are and population of vm
        area = Area(x, y, x_f, y_f, treasures)
        print('Mriežka na začiatku:')
        for row in area.grid:
            print(row)
        population = []
        for q in range(n):
            population.append([format(random.randint(0, 255), '08b') for _ in range(40)])
            for i in range(24):
                population[q].append(format(0, '08b'))
        vm = VirtualMachine()
        iteration = 0
        while iteration < 10000:
            iteration += 1
            population = [Chromosome(chromosome) for chromosome in population]
            for item in population:
                item.treasures_found = vm.machine_work(area, 0, item.chromosome)
                # print results and plot
                if item.treasures_found == tr_count:
                    print('Nájdené poklady, virtuálny stroj:')
                    print(item.treasures_found, item.chromosome)
                    vm.machine_work(area, 1, item.chromosome)
                    plt.plot(np.array(self.fitness_chart))
                    plt.show()
                    self.fitness_chart.clear()
                    return 0
            if selection == 0:
                to_cross = self.roulette(population)
            else:
                to_cross = self.duel(population)
            population = self.cross(to_cross)

        print('Výsledok nenájdený')
        return -1


if __name__ == "__main__":
    while True:
        try:
            size = (input(f'Zadajte x,y veľkosť mriežky, "k" pre skonči: '))
            if size == 'k':
                break
            size = list(size.split(','))
            x = int(size[0])
            y = int(size[1])
            n = int(input('Počet jedincov: '))
            search = (input(f'Zadajte x,y súradnicu hľadača: '))
            search = list(search.split(','))
            x_f = int(search[0])
            y_f = int(search[1])
            treasures = []
            while True:
                treasure_pos = (input(f'Zadajte x,y súradnicu pokladu, "k" pre skonči: '))
                if treasure_pos == 'k':
                    break
                treasure_pos = list(treasure_pos.split(','))
                treasure_pos = [int(i) for i in treasure_pos]
                if treasure_pos not in treasures:
                    treasures.append(treasure_pos)
            selection = int(input(f'0: ruleta, 1: duel: '))
            tr_count = len(treasures)
            start = Main()
            start.main()
        except:
            print('Nesprávny vstup')

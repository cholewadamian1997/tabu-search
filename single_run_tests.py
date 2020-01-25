import matplotlib.pyplot as plt
import argparse
import fun
import copy
import random

from tabu_search import tabu_search
import memory_structures

neighbourhood = memory_structures.Neighborhood()
first_solution = neighbourhood.first_solution
random_solution = copy.copy(first_solution)

random.shuffle(random_solution)
random.shuffle(random_solution)
random.shuffle(random_solution)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('iterations', type=int, help='iterations number')
    parser.add_argument('tabu_list_size', type=int, help='tabu list size')
    parser.add_argument('neighbourhood_size', type=int, help='neighbourhood size')

    # parser.add_argument('-checktime', '--t', type=bool, default=False, help='Measure time of tabu search algorithm')
    # parser.add_argument('-csv', type=bool, default=False, help='save result to csv file')

    parser.add_argument('materials_plot', type=int, help='plot materials chart')
    parser.add_argument('time_plot', type=int, help='plot materials chart')
    parser.add_argument('buildings_plot', type=int, help='plot buildings chart')
    parser.add_argument('random', type=int, help='')

    args = parser.parse_args()

    best_solution, best_time, best_materials_state, time_change_list = tabu_search(solution=first_solution,
                                                                                   neighbourhood=neighbourhood,
                                                                                   iterations=args.iterations,
                                                                                   tabu_list_size=args.tabu_list_size,
                                                                                   neighbourhood_size=args.neighbourhood_size)

    if args.materials_plot == 1:
        plt.plot(range(0, len(best_materials_state[0])), best_materials_state[0])
        plt.title('Aktualna ilość drewna')
        plt.ylabel("Ilość drewna")
        plt.xlabel("Numer decyzji")
        plt.show()
        plt.plot(range(0, len(best_materials_state[1])), best_materials_state[1])
        plt.title('Aktualna ilość cegieł')
        plt.ylabel("Ilość cegieł")
        plt.xlabel("Numer decyzji")
        plt.show()
        plt.plot(range(0, len(best_materials_state[2])), best_materials_state[2])
        plt.title('Aktualna ilość żelaza')
        plt.ylabel("Ilość żelaza")
        plt.xlabel("Numer decyzji")
        plt.show()

    if args.time_plot == 1:
        plt.plot(range(0, len(time_change_list)), time_change_list)
        plt.title('Funkcja celu od iteracji')
        plt.ylabel("Czas [min]")
        plt.xlabel("Numer iteracji")
        plt.show()

    if args.buildings_plot == 1:
        plot_list_0 = fun.generate_buildings_levels_plot(best_solution, 0)
        plot_list_1 = fun.generate_buildings_levels_plot(best_solution, 1)
        plot_list_2 = fun.generate_buildings_levels_plot(best_solution, 2)
        plot_list_3 = fun.generate_buildings_levels_plot(best_solution, 3)
        plot_list_4 = fun.generate_buildings_levels_plot(best_solution, 4)
        plot_list_5 = fun.generate_buildings_levels_plot(best_solution, 5)

        plt.plot(range(0, len(plot_list_0)), plot_list_0, label='Ratusz')
        plt.plot(range(0, len(plot_list_0)), plot_list_1, label='Spichlerz')
        plt.plot(range(0, len(plot_list_0)), plot_list_2, label='Tartak')
        plt.plot(range(0, len(plot_list_0)), plot_list_3, label='Cegielnia')
        plt.plot(range(0, len(plot_list_0)), plot_list_4, label='Huta')
        plt.plot(range(0, len(plot_list_0)), plot_list_5, label='Zagroda')

        plt.title('Przebieg rozbudowy mista w danej iteracji')
        plt.ylabel("Poziom rozwoju")
        plt.xlabel("Numer decyzji")
        plt.legend()
        plt.show()

    if args.random == 1:
        plot_list_0 = fun.generate_buildings_levels_plot(random_solution, 0)
        plot_list_1 = fun.generate_buildings_levels_plot(random_solution, 1)
        plot_list_2 = fun.generate_buildings_levels_plot(random_solution, 2)
        plot_list_3 = fun.generate_buildings_levels_plot(random_solution, 3)
        plot_list_4 = fun.generate_buildings_levels_plot(random_solution, 4)
        plot_list_5 = fun.generate_buildings_levels_plot(random_solution, 5)

        plt.plot(range(0, len(plot_list_0)), plot_list_0)
        plt.plot(range(0, len(plot_list_0)), plot_list_1)
        plt.plot(range(0, len(plot_list_0)), plot_list_2)
        plt.plot(range(0, len(plot_list_0)), plot_list_3)
        plt.plot(range(0, len(plot_list_0)), plot_list_4)
        plt.plot(range(0, len(plot_list_0)), plot_list_5)

        plt.show()

    else:
        raise argparse.ArgumentError

import matplotlib.pyplot as plt

from tabu_search import tabu_search
import memory_structures

neighbourhood_size_list = [i*2 for i in range(2, 30)]
tabu_list_size_list = [i*2 for i in range(1, 25)]
algorithm_iteration_list = [i*4 for i in range(1, 10)]


neighbourhood = memory_structures.Neighborhood()
first_solution = neighbourhood.first_solution

# Testing how numbers of iterations affects the result
iterations_y_lim = list()
for iteration in algorithm_iteration_list:
    best_solution, best_time = tabu_search(solution=first_solution, neighbourhood=neighbourhood, iterations=iteration,
                                           tabu_list_size=5, neighbourhood_size=5)
    print("iterations number:", iteration, "time:", best_time, "solution:", best_solution)
    iterations_y_lim.append(int(best_time))


plt.plot(algorithm_iteration_list, iterations_y_lim, color='red')
plt.title("time dependence on the number of algorithm iterations")
plt.ylabel("time [s]")
plt.xlabel("iterations")
plt.show()


# Testing how tabu list size affects the result
tabu_size_y_lim = list()
for tabu_size in tabu_list_size_list:
    best_solution, best_time = tabu_search(solution=first_solution, neighbourhood=neighbourhood, iterations=10,
                                           tabu_list_size=tabu_size, neighbourhood_size=5)
    print("tabu list size:", tabu_size, "time:", best_time, "solution:", best_solution)
    tabu_size_y_lim.append(int(best_time))

plt.plot(tabu_list_size_list, tabu_size_y_lim, color='blue')
plt.title("time dependence on the size of tabu table")
plt.ylabel("time [s]")
plt.xlabel("tabu table size")
plt.show()


# Testing how neighbourhood size affects the result
neighbourhood_size_y_lim = list()
for neighbourhood_size in neighbourhood_size_list:
    best_solution, best_time = tabu_search(solution=first_solution, neighbourhood=neighbourhood, iterations=10,
                                           tabu_list_size=5, neighbourhood_size=neighbourhood_size)
    print("iterations number:", neighbourhood_size, "time:", best_time, "solution:", best_solution)
    neighbourhood_size_y_lim.append(int(best_time))

plt.plot(neighbourhood_size_list, neighbourhood_size_y_lim, color='black')
plt.title("time dependence on the size of neighbourhood")
plt.ylabel("time [s]")
plt.xlabel("neighbourhood size")
plt.show()

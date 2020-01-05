import memory_structures
import copy
from fun import generate_solution_time


def tabu_search(solution, neighbourhood, iterations, tabu_list_size, neighbourhood_size):
    """Tabu search algorithm implementation

    :param iterations:
    :param tabu_list_size:
    :param neigbourhood:
    :return:
    """

    recent_bests_time = memory_structures.BestSolutionsTime()

    final_best_time = generate_solution_time(solution)
    final_best_solution = solution
    tabu_list = list()
    forbidden_solution_list = list()

    count = 0
    while count <= iterations:
        available_solutions, changing_pairs_list = neighbourhood.generate_new_neighbourhood(solution=final_best_solution, neighbourhood_size=neighbourhood_size)
        if len(available_solutions) < 1:
            continue

        best_solution_index = 0
        best_solution = available_solutions[0]
        best_solution_time = generate_solution_time(best_solution)

        # checking if next solution form neighbourhood is better than current best solution
        # starting from index=1 because index=0 is our first solution by default
        for i in range(1, len(available_solutions)):
            current_solution = available_solutions[i]
            current_solution_time = generate_solution_time(current_solution)
            if current_solution_time < best_solution_time:
                best_solution = current_solution
                best_solution_time = current_solution_time
                best_solution_index = i

        found = False
        while not found:

            if changing_pairs_list[best_solution_index] not in tabu_list:
                tabu_list.append(changing_pairs_list[best_solution_index])
                found = True
                if best_solution_time < final_best_time:
                    if recent_bests_time.check_progress(best_solution_time):
                        final_best_time = best_solution_time
                        final_best_solution = best_solution
                        recent_bests_time.add(copy.copy(final_best_time))

            # todo Ask about it
            else:
                forbidden_solution_list.append(best_solution)
                for i in range(1, len(available_solutions)):
                    current_solution = available_solutions[i]
                    if generate_solution_time(current_solution) < best_solution_time and current_solution not in forbidden_solution_list:
                        best_solution = current_solution
                        best_solution_time = generate_solution_time(current_solution)
                        best_solution_index = i

        if len(tabu_list) >= tabu_list_size:
            tabu_list.pop(0)
        count = count + 1

    return final_best_solution, final_best_time


if __name__ == "__main__":
    neighbourhood = memory_structures.Neighborhood()
    first_solution = neighbourhood.first_solution

    best_solution, best_time = tabu_search(solution=first_solution, neighbourhood=neighbourhood, iterations=20, tabu_list_size=5, neighbourhood_size=5)
    print("best solution: ", best_solution)
    print("best time after all: ", best_time)









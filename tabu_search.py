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

    final_best_time = generate_solution_time(solution)[0]
    final_best_solution = solution
    tabu_list = list()
    time_change_list = list()

    count = 0
    while count <= iterations:
        available_solutions, changing_pairs_list = neighbourhood.generate_new_neighbourhood(solution=final_best_solution, neighbourhood_size=neighbourhood_size)
        if len(available_solutions) < 1:
            continue

        best_solution_index = 0
        best_solution = available_solutions[0]
        best_solution_time = generate_solution_time(best_solution)[0]

        # checking if next solution form neighbourhood is better than current best solution
        # starting from index=1 because index=0 is our first solution by default
        for i in range(1, len(available_solutions)):
            current_solution = available_solutions[i]
            current_solution_time = generate_solution_time(current_solution)[0]
            if current_solution_time < best_solution_time and (current_solution[changing_pairs_list[i][0]],current_solution[changing_pairs_list[i][1]] == [5, 2] or current_solution[changing_pairs_list[i][0]],current_solution[changing_pairs_list[i][1]] == [5, 3] or current_solution[changing_pairs_list[i][0]],current_solution[changing_pairs_list[i][1]] == [5, 4]):
                #if not (changing_pairs_list[i] == [2, 5] or changing_pairs_list[i] == [3, 5] or changing_pairs_list[i] == [4, 5]) or ((changing_pairs_list[i] == [2, 5] or changing_pairs_list[i] == [3, 5] or changing_pairs_list[i] == [4, 5]) and recent_bests_time.check_progress(best_solution_time, time_const=50)):
                best_solution = current_solution
                best_solution_time = current_solution_time
                best_solution_index = i

        if changing_pairs_list[best_solution_index] not in tabu_list:
            tabu_list.append(changing_pairs_list[best_solution_index])
            if best_solution_time < final_best_time:
                if recent_bests_time.check_progress(best_solution_time, time_const=50):
                    final_best_time = best_solution_time
                    final_best_solution = best_solution
                    recent_bests_time.add(copy.copy(final_best_time))

        time_change_list.append(generate_solution_time(best_solution)[0])

        if len(tabu_list) >= tabu_list_size:
            tabu_list.pop(0)
        count = count + 1


    best_materials_state = generate_solution_time(final_best_solution)[1]

    return final_best_solution, final_best_time, best_materials_state, time_change_list


if __name__ == "__main__":
    neighbourhood = memory_structures.Neighborhood()
    first_solution = neighbourhood.first_solution

    best_solution, best_time, best_materials_state, time_change_list = tabu_search(solution=first_solution,
                                                                                   neighbourhood=neighbourhood,
                                                                                   iterations=400,
                                                                                   tabu_list_size=10,
                                                                                   neighbourhood_size=10)
    print("best solution: ", best_solution)
    print("best time after all: ", best_time)








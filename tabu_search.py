import numpy as np

def generete_solution_time(solution): pass



def generate_first_solution():

    first_solution = np.array([0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5])
    return first_solution


def create_new__rand_solutionsList(solution, amount_of_solutions):

    new_solution_List = np.array([])
    for x in range(0, amount_of_solutions):
        first = np.random.random_integers(np.len(solution))
        second = np.random.random_integers(np.len(solution))
        while first == second:
            first = np.random.random_integers(np.len(solution))

        new_solution = solution
        new_solution[first], new_solution[second] = new_solution[second], new_solution[first]
        if np.isin(new_solution_List, new_solution):
            new_solution_List.append(new_solution)

    return new_solution_List

def tabu_search(first_solution, iterations, tabu_list_size):


    solution = first_solution
    tabu_list = np.array([])
    best_time_ever = generete_solution_time(solution)
    best_solution_ever = solution

    while count <= iterations:

        available_solutions, changing_pairs_list = create_new__rand_solutionsList()
        best_solution_index = 0
        best_solution = available_solutions[0]
        best_solution_time = generete_solution_time(best_solution)
        forbidden_solution_list = None

        for i in range(1, len(available_solutions)): # zaczynamy od 1 bo rozwiazanie z indexem zerowym jest punktem wyjscia
            current_solution = available_solutions[i]
            if generete_solution_time(current_solution) < best_solution_time:
                best_solution = current_solution
                best_solution_time = generete_solution_time(current_solution)
                best_solution_index = i

        found = False
        while found == False:

            if changing_pairs_list[best_solution_index] not in tabu_list:
                tabu_list.append(changing_pairs_list[best_solution_index])
                found = True
                if best_solution_time < best_time_ever:
                    best_time_ever = best_solution_time
                    best_solution_ever = best_solution

            else:
                forbidden_solution_list.append(best_solution)
                for i in range(1, len(available_solutions)):
                    current_solution = available_solutions[i]
                    if generete_solution_time(current_solution) < best_solution_time and current_solution not in forbidden_solution_list:
                        best_solution = current_solution
                        best_solution_time = generete_solution_time(current_solution)
                        best_solution_index = i

        if len(tabu_list) >= tabu_list_size:
            tabu_list.pop(0)

        count = count + 1

    return best_solution_ever, best_time_ever





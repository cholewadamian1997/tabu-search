
import random

def generete_time_of_solution(solution): pass



def generate_first_solution():
    """generuje pierwsze rozwiązanie, taka forma żeby było że ten ratusz jest pierwszy zawsze """

    first_solution = [0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5]
    return first_solution


def create_new__rand_solutionsList(solution, amount_of_solutions):
    "generuje liste rozwiązań w każdym jest jedna zmiana w stosunku do podanego wszystkie są od siebie różne "

    new_solution_List = []
    changed_elem_List = []

    for x in range(0, amount_of_solutions):
        first = random.randrange(len(solution))
        second = random.randrange(len(solution))
        while first == second:
            first = random.randrange(len(solution))

        new_solution = solution
        new_solution[first], new_solution[second] = new_solution[second], new_solution[first]
        changed_elem = [first, second]

        if new_solution not in new_solution_List:
            new_solution_List.append(new_solution)
        if changed_elem not in changed_elem_List:
            changed_elem_List.append(changed_elem)
    new_solution_tuple = (new_solution_List, changed_elem_List)
    return new_solution_tuple

def tabu_search(first_solution, iterations, tabu_list_size):


    solution = first_solution
    tabu_list = []
    best_time = generete_time_of_solution(solution)
    best_solution_ever = solution

    while count <= iterations:

        """tu kuba możesz wsadzić tą logike """

        if len(tabu_list) >= tabu_list_size:
            tabu_list.pop(0)

        count = count + 1

    return best_solution_ever, best_time

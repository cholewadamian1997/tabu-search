port random
import copy
import numpy as np
from pprint import pprint
from data import materials_requirements, max_population, time_requirements


def calculate_filling_time(vector_of_materials, vector_of_requirements, state_of_buildings):

    final_time = 0
    for i in range(len(vector_of_materials)):
        if vector_of_requirements[i] > vector_of_materials[i]:
            temp_time = (vector_of_requirements[i] - vector_of_materials[i]) / (materials_requirements[i + 2][state_of_buildings[i + 2]][4] / 30)
            if temp_time > final_time:
                final_time = temp_time
    return final_time


def generate_time_of_solution(solution) -> int:

    current_state_of_buildings = [1, 1, 1, 1, 1, 1]
    current_state_of_materials = [100, 100, 100]
    time = 0
    for step in solution: #step to liczba odpowiadająca jakiemuś budynkowi (np 3) (index wektora stanu)

        current_number_of_workers = 0
        for i in range(len(current_state_of_buildings)):
            current_number_of_workers = current_number_of_workers + materials_requirements[i][current_state_of_buildings[i]][3]

        "---------------------------------------------"
        if current_number_of_workers > max_population[current_state_of_buildings[5]]:
            return 1000000000000000
        #Jeśli jest za mało ludzi to skończ i odrzuć rozwiązanie

        materials_check = True #Czy jest wystarczająco surowców
        if min(np.subtract(current_state_of_materials, materials_requirements[step][current_state_of_buildings[step]][:3])) < 0:
            materials_check = False

        #print(materials_check)

        if not materials_check:
            filling_time = calculate_filling_time(current_state_of_materials, materials_requirements[step][current_state_of_buildings[step]], current_state_of_buildings)

            #print(filling_time)
            #print("---")

            for i in range(len(current_state_of_materials)):
                current_state_of_materials[i] = current_state_of_materials[i] + (materials_requirements[i + 2][current_state_of_buildings[i + 2]][4] / 30) * filling_time
                #Dlatego i + 2 bo w wektorze stanu budynki z surowcami są na miejscu 3 - 6, a stanu surowców 1 - 4

            time = time + filling_time

        current_state_of_materials = np.subtract(current_state_of_materials, materials_requirements[step][current_state_of_buildings[step]][:3])

        for i in range(len(current_state_of_materials)): #Dodawanie materiałów
            current_state_of_materials[i] = current_state_of_materials[i] + (materials_requirements[i + 2][current_state_of_buildings[i + 2]][4] / 30) * time_requirements[current_state_of_buildings[step]][step]
            #nie wiem w jakiej formie mamy zapisane dane dot czasu budowy więc jest na razie roboczo


        current_state_of_buildings[step] = current_state_of_buildings[step] + 1

    return time


def generate_first_solution():
    """generuje pierwsze rozwiązanie, taka forma żeby było że ten ratusz jest pierwszy zawsze """

    first_solution = [0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5]
    return first_solution


def is_solution_acceptable(new_solution):
    levelList = [0,0,0,0,0,0]
    for x in new_solution:
        levelList[x] += 1
        if levelList[0] < levelList[1] or levelList[0] < levelList[2] or levelList[0] < levelList[3]or levelList[0] < levelList[4]or levelList[0] < levelList[5]:
            return False
    return True


def create_new__rand_solutionsList(solution, amount_of_solutions):
    "generuje liste rozwiązań w każdym jest jedna zmiana w stosunku do podanego wszystkie są od siebie różne "

    new_solution_List = []
    changed_elem_List = []
    i = 0
    for x in range(0, amount_of_solutions):
        i += 1
        first = random.randrange(len(solution))
        second = random.randrange(len(solution))
        while first == second:
            first = random.randrange(len(solution))

        temp_solution = copy.copy(solution)
        temp_solution[first], temp_solution[second] = temp_solution[second], temp_solution[first]
        changed_elem = [first, second]

        "sprawdzam czy nowe rozw spełnia ograniczenia(ratusz)"
        if is_solution_acceptable(temp_solution):
            new_solution = copy.copy(temp_solution)
            if new_solution not in new_solution_List:
                new_solution_List.append(new_solution)
            else:
                x -= 1
            if changed_elem not in changed_elem_List:
                changed_elem_List.append(changed_elem)
            else:
                x -= 1

        else:
            x -= 1
        if i >= 2 * amount_of_solutions:
            break

    return new_solution_List, changed_elem_List


def tabu_search(first_solution, iterations, tabu_list_size):

    solution = first_solution
    print("first solution: ", solution)
    tabu_list = list()
    best_time_ever = generate_time_of_solution(solution)
    print("best_time_ever: ", best_time_ever)
    best_solution_ever = solution

    count = 0
    while count <= iterations:

        available_solutions, changing_pairs_list = create_new__rand_solutionsList(first_solution, 40)
        best_solution_index = 0
        best_solution = available_solutions[0]
        best_solution_time = generate_time_of_solution(best_solution)
        forbidden_solution_list = list()

        for i in range(1, len(available_solutions)): # zaczynamy od 1 bo rozwiazanie z indexem zerowym jest punktem wyjscia
            current_solution = available_solutions[i]
            if generate_time_of_solution(current_solution) < best_solution_time:
                best_solution = current_solution
                best_solution_time = generate_time_of_solution(current_solution)
                best_solution_index = i

        found = False
        while not found:

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
                    if generate_time_of_solution(current_solution) < best_solution_time and current_solution not in forbidden_solution_list:
                        best_solution = current_solution
                        best_solution_time = generate_time_of_solution(current_solution)
                        best_solution_index = i

        if len(tabu_list) >= tabu_list_size:
            tabu_list.pop(0)

        count = count + 1
        print("current best solution: ", best_solution_ever, "time: ", best_time_ever)

    return best_solution_ever, best_time_ever


class RecentlyUsedSolution:
    """Class used for storing previous solutions

    attributes
    -------
    _recent_solution : list
        list of recent solution

    """
    def __init__(self):
        self._recent_solution = list()

    def check_if_used(self, solution, generations=3):
        """Method used for checking if given solution was found before

        Parameters
        ----------
        solution : list
            list representing solution

        generations: int
            number of how many previous solutions will be consider

        Returns
        -------
        bool
            True if solution was found before, False otherwise
        """

        if len(self._recent_solution) < generations:
            pass    # Error codes ???

        if solution in self._recent_solution[-generations:]:
            return True
        else:
            return False

    def add(self, solution):
        """ Appending solution to list

        Parameters
        ---------
        solution: list
            list representing solution
        """
        self._recent_solution.append(solution)

    def check_progress(self, time_const, generations):
        """ Checking if solutions were decreasing in given generations more than given time_const
        Parameters
        ----------
        time_const: float
            value of time needed to be consider if solutions are decreasing

        generations: int
            number of how many previous solution will be consider

        Returns
        -------
        bool
            True if progress exist, False otherwise
        """

        if len(self._recent_solution) < generations:
            pass    # Error codes ???
        used = self._recent_solution[-generations:]

        progress = True
        for i in range(len(used)-1):
            if used[i] - time_const < used[i+1]:
                progress = False
            else:
                continue

        # ToDO: other rules to check progress ?
        return progress

    def check_diversity(self, generations):
        """
        Check if diversity is present in search process

        Parameters
         ---------
        generations: int
            number of how many previous solutions will be consider

        Return:
        --------
        bool
            True if diversity is present in search process, False otherwise
        """
        if len(self._recent_solution) < generations:
            pass    # Error codes ???
        used = self._recent_solution[-generations:]

        diversity = True
        changes_list = list()
        for i in range(len(used[0])):
            changes_counter = 0
            for j in range(len(used)-1):
                if used[j][i] != used[j+1][i]:
                    changes_counter += 1

            changes_list.append(changes_counter)

        # ToDO: if statement for checking changes list and setting diversity variable

        return diversity


if __name__ == '__main__':

    # first solution - OK! :
    first_solution = generate_first_solution()
    # print(first_solution)

    # create list of neighbours
    # neighbours = create_new__rand_solutionsList(first_solution, 100)
    # for neighbour in neighbours[0]:
    #     print(neighbour)

    best_solution, best_time = tabu_search(first_solution, 40, 40)
    print("best solution: ", best_solution)
    print("best time after all: ", best_time)









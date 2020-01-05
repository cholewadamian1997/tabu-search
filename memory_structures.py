import random
import copy


def is_solution_acceptable(new_solution):
    """

    :param new_solution:
    :return:
    """
    levelList = [0, 0, 0, 0, 0, 0]
    for x in new_solution:
        levelList[x] += 1
        if levelList[0] < levelList[1] or levelList[0] < levelList[2] or levelList[0] < levelList[3]or levelList[0] < levelList[4]or levelList[0] < levelList[5]:
            return False
    return True


class Neighborhood:
    """Class used for storing previous solutions

    attributes
    -------
    neighborhood : list
        list of recent solution

    """
    def __init__(self):
        self.first_solution = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5]
        self.neighborhood = list()
        self.changed_elements = list()

    def generate_new_neighbourhood(self, solution, neighbourhood_size=20):
        self.clear_neighbourhood()

        # until size of neighbourhood is reached
        while len(self.neighborhood) < neighbourhood_size:

            # draw an indexes for swapping
            first = random.randrange(len(solution))
            second = random.randrange(len(solution))
            while first == second:
                first = random.randrange(len(solution))

            # swapping two elem
            temp_solution = copy.copy(solution)
            temp_solution[first], temp_solution[second] = temp_solution[second], temp_solution[first]
            changed_elem = [first, second]

            if is_solution_acceptable(temp_solution):
                if not self.check_if_used(solution=temp_solution):
                    self.add_solution(temp_solution)
                    self.changed_elements.append(changed_elem)

        return self.neighborhood, self.changed_elements

    def clear_neighbourhood(self):
        self.neighborhood = list()
        self.changed_elements = list()

    def check_if_used(self, solution, generations=10):
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

        if len(self.neighborhood) < generations:
            pass    # Error codes ???

        if solution in self.neighborhood[-generations:]:
            return True
        else:
            return False

    def add_solution(self, solution):
        """ Appending solution to list

        Parameters
        ---------
        solution: list
            list representing solution
        """
        self.neighborhood.append(solution)


class BestSolutionsTime:
    def __init__(self):
        self.best_solutions = list()

    def add(self, solution):
        self.best_solutions.append(solution)

    def check_progress(self, solution, time_const=5):
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

        if len(self.best_solutions) == 0:
            return True
        elif solution + time_const <= self.best_solutions[-1]:
            return True
        else:
            return False

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
        if len(self.neighborhood) < generations:
            pass    # Error codes ???
        used = self.neighborhood[-generations:]

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

    neighbourhood_instance = Neighborhood()
    first_solution = neighbourhood_instance.first_solution
    neighbourhood = neighbourhood_instance.generate_new_neighbourhood(first_solution)

    for neighbour in neighbourhood[0]:
        print(neighbour)

    for swap in neighbourhood[1]:
        print(swap)

    print(len(neighbourhood[0]))
    print(len(neighbourhood[1]))

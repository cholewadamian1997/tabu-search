import numpy as np

import data


# tmp
def do_reset():
    pass


# tmp
def time(solution):
    pass


class RecentlyUsedSolution:
    """Class used for storing previous solution

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

        used = self._recent_solution[-generations:]
        if solution in used:
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









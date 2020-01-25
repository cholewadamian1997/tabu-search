import numpy as np
from data import ratusz, spichlerz, tartak, cegielnia, huta, zagroda, maximum_population
from data import calculate_time_requirements
import copy

# importing game rules
materials_requirements = np.array([ratusz, spichlerz, tartak, cegielnia, huta, zagroda])
max_population = maximum_population
time_requirements = calculate_time_requirements()


def calculate_filling_time(vector_of_materials, vector_of_requirements, state_of_buildings):
    """

    :param vector_of_materials:
    :param vector_of_requirements:
    :param state_of_buildings:
    :return:
    """

    final_time = 0
    for i in range(len(vector_of_materials)):
        if vector_of_requirements[i] > vector_of_materials[i]:
            temp_time = (vector_of_requirements[i] - vector_of_materials[i]) / (materials_requirements[i + 2][state_of_buildings[i + 2]][4] / 30)
            if temp_time > final_time:
                final_time = temp_time
    return final_time


def generate_solution_time(solution) -> int:

    current_state_of_buildings = [1, 1, 1, 1, 1, 1]
    current_state_of_materials = [100, 100, 100]
    time = 0

    final_list_of_wood = []
    final_list_of_brick = []
    final_list_of_iron = []
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

        temp_materials = copy.copy(current_state_of_materials)
        final_list_of_wood.append(temp_materials[0])
        final_list_of_brick.append(temp_materials[1])
        final_list_of_iron.append(temp_materials[2])

        current_state_of_materials = np.subtract(current_state_of_materials, materials_requirements[step][current_state_of_buildings[step]][:3])

        for i in range(len(current_state_of_materials)): #Dodawanie materiałów
            current_state_of_materials[i] = current_state_of_materials[i] + (materials_requirements[i + 2][current_state_of_buildings[i + 2]][4] / 30) * time_requirements[current_state_of_buildings[step]][step]
            #nie wiem w jakiej formie mamy zapisane dane dot czasu budowy więc jest na razie roboczo



        current_state_of_buildings[step] = current_state_of_buildings[step] + 1
    final_list_of_materials = [final_list_of_wood, final_list_of_brick, final_list_of_iron]

    return time, final_list_of_materials


def generate_buildings_levels_plot(solution, building: int):
    plot_list = []
    current_level = 1
    for elem in solution:
        plot_list.append(current_level)
        if elem == building:
            current_level += 1

    return plot_list



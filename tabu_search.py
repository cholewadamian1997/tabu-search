import numpy as np

import random
import copy


from data import materials_requirements, max_population, time_requirements


def calculate_filling_time(vector_of_materials, vector_of_requirements, state_of_buildings):

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

    first_solution = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5]
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
    while len(new_solution_List) < amount_of_solutions or i > 100 * amount_of_solutions:

        first = random.randrange(len(solution))
        second = random.randrange(len(solution))
        while first == second:
            first = random.randrange(len(solution))

        temp_solution = copy.copy(solution)
        temp_solution[first], temp_solution[second] = temp_solution[second], temp_solution[first]
        changed_elem = [first, second]
        #print(is_solution_acceptable(temp_solution))
        "sprawdzam czy nowe rozw spełnia ograniczenia(ratusz)"
        if is_solution_acceptable(temp_solution):
            new_solution = copy.copy(temp_solution)
            if new_solution not in new_solution_List:
                new_solution_List.append(new_solution)
                changed_elem_List.append(changed_elem)

    new_solution_tuple = (new_solution_List, changed_elem_List)

    return new_solution_tuple

    new_solution_tuple = (new_solution_List, changed_elem_List)

    return new_solution_tuple


def tabu_search(first_solution, iterations, tabu_list_size):

    solution = first_solution
    tabu_list = []
    best_time_ever = generate_solution_time(solution)
    best_solution_ever = solution
    count = 0

    while count <= iterations:

        #print(str(count) + "---")
        available_solutions, changing_pairs_list = create_new__rand_solutionsList(best_solution_ever, 5)
        best_solution_index = 0
        #print(available_solutions)
        if len(available_solutions) < 1:
            print("bum")
            continue
        #print(available_solutions)
        best_solution = available_solutions[0]
        best_solution_time = generate_solution_time(best_solution)
        forbidden_solution_list = []

        for i in range(1, len(available_solutions)): # zaczynamy od 1 bo rozwiazanie z indexem zerowym jest punktem wyjscia
            current_solution = available_solutions[i]
            if generate_solution_time(current_solution) < best_solution_time:
                best_solution = current_solution
                best_solution_time = generate_solution_time(current_solution)
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
                    if generate_solution_time(current_solution) < best_solution_time and current_solution not in forbidden_solution_list:
                        best_solution = current_solution
                        best_solution_time = generate_solution_time(current_solution)
                        best_solution_index = i

        if len(tabu_list) >= tabu_list_size:
            tabu_list.pop(0)

        count = count + 1

        print(best_time_ever)
        print(count)

    return best_solution_ever, best_time_ever

"----------------------------------------------------------------------------------------------"

import numpy as np

ratusz = np.array([[90,	80,	70,	5],
[113,	102,	88,	    6],
[143,	130,	111,	7],
[180,	166,	140,    8],
[227,	211,	176,    9],
[286,	270,	222,	11],
[360,	344,	280,	13],
[454,	438,	353,	15],
[572,	559,	445,	18],
[720,	712,	560,	21],
[908,	908,	706,	24],
[1144,	1158,	890,	28],
[1441,	1476,	1121,	33],
[1816,	1882,	1412,	38],
[2288,	2400,	1779,	45],
[2883,	3060,	2242,	53],
[3632,	3902,	2825,	62],
[4577,	4975,	3560,	72],
[5767,	6343,	4485,	84],
[7266,	8087,	5651,	99],
[9155,	10311,	7120,	116],
[11535,	13146,	8972,	135],
[14534,	16762,	11304,	158],
[18313,	21371,	14244,	185],
[23075,	27248,	17947,	216],
[29074,	34741,	22613,	253],
[36633,	44295,	38493,	296],
[46158,	56476,	35901,	347],
[58159,	72007,	45235,	406],
[73280,	91809,	56996,	475]])

spichlerz = np.array([[76,	    64,		50,		0],
                      [96,	    81,		62,		0],
                      [121,	    102, 	77,		0],
                      [154,	    130, 	96,		0],
                      [194,	    165, 	120,	0],
                      [246,	    210, 	149,	0],
                      [311,	    266, 	185,	0],
                      [393,	    338, 	231,	0],
                      [498,	    430, 	287,	0],
                      [630,	    546, 	358,	0],
                      [796,	    693, 	446,	0],
                      [1007,	880, 	555,	0],
                      [1274,	1180,	691,	0],
                      [1612,	1420,	860,	0],
                      [2039,	1803,	1071,	0],
                      [2580,	2290,	1333,	0],
                      [3264,	2908,	1659,	0],
                      [4128,	3693,	2066,	0],
                      [5222,	4691,	2572,	0],
                      [6606,	5957,	3202,	0],
                      [8357,	7599,	3987,	0],
                      [10572,	9608,	4963,	0],
                      [13373,	12203,	6180,	0],
                      [16917,	15497,	7694,	0]])

tartak = np.array([[50,		60,	    40,	   	5,		15],
                   [63,		77,	    50,	   	6,		17],
                   [78,		98,	    63,	   	7,		20],
                   [98,		124,	77,	   	8,		23],
                   [122,	159,    96,	   	9,		27],
                   [153,	202,	120,	10,		32],
                   [191,	258,	149,	12,		37],
                   [238,	329,	185,	14,		43],
                   [298,	419,	231,	16,		50],
                   [373,	534,	287,	18,		58],
                   [466,	681,	358,	21,		68],
                   [582,	868,	446,	24,		79],
                   [728,	1107,	555,    28,		92],
                   [909,	1412,	691,    33,		107],
                   [1137,	1800,	860,    38,		124],
                   [1421,	2295,	1071,   43,		144],
                   [1776,	2926,	1333,   50,		168],
                   [2220,	3731,	1659,   58,		145],
                   [2776,	4757,	2066,   67,		227],
                   [3469,	6065,	2572,   77,		265],
                   [4337,	7733,	3202,   89,		308],
                   [5421,	9860,	3987,   103,	358],
                   [6776,	12571,	4963,   119,	416],
                   [8470,	16028,	6180,   138,	484],
                   [10588,	20436,	7694,   159,	563]])

"drew, cegł, żel, ludzie_zap, ludzie_ogr"
zagroda = np.array([[45,	40,		30, 0,	240],
                    [59,	53,		39, 0,  281],
                    [76,	70,		50,	0,	329],
                    [99,	92,		64,	0,	386],
                    [129,	12,		183,0,	452],
                    [167,	16,		107,0,	530],
                    [217,	21,		138,0,	622],
                    [282,	27,		178,0,	729],
                    [367,	36,		230,0,	854],
                    [477,	48,		297,0,	1002],
                    [620,	64,		383,0,	1174],
                    [806,	84,		494,0,	1376],
                    [1048,	1119,	637,0,	1613],
                    [1363,	1477,	822,0,	1891],
                    [1772,	1950,	1060,0,	2216],
                    [2303,	2574,	1368,0,	2598],
                    [2994,	3398,	1764,0,	3045],
                    [3893,	4486,	2276,0,	3569],
                    [5060,	5921,	2936,0,	4183],
                    [6579,	7816,	3787,0,	4904],
                    [8525,	10317,	4886,0,	5748],
                    [11118,	13618,	6302,0,	6737],
                    [14453,	17976,	8130,0,	7896],
                    [18789,	23728,	10488,0,9255],
                    [24426,	31321,	13529,0,10848]])

"drew, cegł, żel, ludzie_zap, surkinagodz*0.5"
cegielnia = np.array([[65,	    50,		40,		10,		15],
                     [83,	    63,		50,		11,		17],
                     [105,	    80,		62,		13,		20],
                     [133,	    101,	76,		15,		23],
                     [169,	    128,	95,		17,		27],
                     [215,	    162,	117,	19,		32],
                     [273,	    205,	145,	22,		37],
                     [346,	    259,	180,	25,		43],
                     [440,	    328,	224,	29,		50],
                 [559,	    415,	277,	33,		58],
                 [709,	    525,	344,	37,		68],
                 [901,	    664,	426,	42,		79],
                 [1144,	    840,	529,	48,		92],
                 [1453,	    1062,	655,	55,		107],
                 [1846,	    1343,	813,	63,		124],
                 [2344,	    1700,	1008,	71,		144],
                 [2977,	    2150,	1250,	81,		168],
                 [3781,	    2720,	1550,	93,		195],
                 [4802,	    3440,	1922,	103,	227],
                 [6098,	    4352,	2383,	121,	265],
                 [7744,	    5505,	2955,	137,	308],
                 [9835,	    6964,	3664,	157,	358],
                 [12491,	8810,	4543,	179,	416],
                 [15863,	11144,	5633,	204,	484],
                 [20147,    140089, 6985, 232, 563]])

"drew, cegł, żel, ludzie_zap, surkinagodz*0.5"
huta = np.array([[75,65,	70,	10,	15],
[94,	83,	87,	12,	17],
[118,	106,	108,	14,	20],
[147,	135,	133,	16,	23],
[184,	172,165,	19,	27],
[231,	219,205,	22,	32],
[289,	279,	254,	26,	37],
[362,	352,	316	,30,43],
[453,	454,	391,	35,	50],
[567,	579,	485,	41,	58],
[710,	738,	602,	48,	78],
[889,	941,	746,	56,	89],
[1113,	1200,	925,	66,	92],
[1393,	1529,	1147,	77,	107],
[1744,	1950,	1422,	90,	124],
[2183,	2486,	1764,	105,144],
[2734,	3170,	2187,	123,	168],
[3422,	4042,	2712,	144,	195],
[4285,	5153,	3363,	169,	227],
[5365,	6571,	4170,	197,	265],
[6717,	8378,	5170,	231,	308],
[8409,	10681,	6411,	270	,358],
[10528	,13619,	7950,	316	,416],
[13181,	17364,	9858,	370	,484],
[15503,	22139,	12224,	433,	563]
])


materials_requirements = np.array([ratusz, spichlerz, tartak, cegielnia, huta, zagroda])

max_population = np.array([240,	281, 329, 386, 452, 530, 622, 729, 854, 1002, 1174, 1376, 1613, 1891, 2216, 2598, 3045, 3569, 4183, 4904, 5748, 6737, 7896, 9255, 10848, 12715, 14904, 17469, 20476, 24000])

temp_time_requirements = [[7.5, 8.5, 7.5, 7.5, 9, 10]]
for i in range(30):
    temp_list = []
    for j in range(len(temp_time_requirements[0])):
        temp_list.append(temp_time_requirements[i][j] * 1.2)
    temp_time_requirements.append(temp_list)

time_requirements = np.array(temp_time_requirements)






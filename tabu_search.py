import numpy as np

"""
x-  6 elementowy wektor  stanu reprezentujący poziomy poszczególnych budynków
x0 - poziom ratusza
x1 - poziom tartaku
x2 - poziom ciegielni
x3 - poziom huty żelaza
x4 - poziom zagrody
x5 - poziom spichlerza
"""
x = np.array([0, 0, 0, 0, 0, 0])

"""
x0_demand  - macierz określa zapotrzebowanie  do budowy kolejnych poziomów ratusza
stopien | drewno | cegła | żelazo | pracownicy
   1    |        |       |        | 
   2    |        |       |        |  
  ...   |        |       |        |  
   25   |        |       |        |                
"""

x0_demand = np.array([[90, 80, 70, 5],
                     [113, 102, 88, 6, 91],
                     [143, 130, 111, 7, 86],
                     [180, 166, 140, 8, 82],
                     [227, 211, 176, 9, 78],
                     [286, 270, 222, 11, 75],
                     [360, 344, 280, 13, 71],
                     [454, 438, 353, 15, 68],
                     [572, 559, 445, 18, 64],
                     [720, 712, 560, 21, 61],
                     [908, 908, 706, 24, 58],
                     [1144, 1158, 890, 28, 56],
                     [1441, 1476, 1121, 33, 53],
                     [1816, 1882, 1412, 38, 51],
                     [2288, 2400, 1779, 45, 48],
                     [2883, 3060, 2242, 53, 46],
                     [3632, 3902, 2825, 62, 44],
                     [4577, 4975, 3560, 72, 42],
                     [5767, 6343, 4485, 84, 40],
                     [7266, 8087, 5651, 99, 38],
                     [9155, 10311, 7120, 116, 36],
                     [11535, 13146, 8972, 135, 34],
                     [14534, 16762, 11304, 158, 33],
                     [18313, 21371, 14244, 185, 31],
                     [23075, 27248, 17947, 216, 30]])










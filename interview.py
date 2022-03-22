# Author: Cole Haraga
# Date: March 21, 2022
# AAFC Nano technical Interview 1

# using the Pandas data science library
# panda has some memory leaks but for this problem it is unessecary to fix these
import pandas as pd
#numpy for numpy array types for the excel sheet to array
import numpy as np
# openpyxl for coordinates of excel sheets
from openpyxl import Workbook

# global constants
rows = 12
columns = 8

# read excel files into a variable
# excel and .py files must be in the same directory(folder) for this method
control1 = pd.read_excel(r'./../AAFC-interview/Exam_control_measurements1.xlsx', header=None)
control2 = pd.read_excel(r'./../AAFC-interview/Exam_control_measurements2.xlsx', header=None)
experimental1 = pd.read_excel(r'./../AAFC-interview/Exam_experimental_measurements1.xlsx', header=None)
experimental2 = pd.read_excel(r'./../AAFC-interview/Exam_experimental_measurements2.xlsx', header=None)

# put values into list
# values are 2d list for each row into inner list i.e. [row][column]
control1_list = control1.values.tolist()
control2_list = control2.values.tolist()
experimental1_list = experimental1.values.tolist()
experimental2_list = experimental2.values.tolist()

# need mean values of each control group
mean_control1 = np.mean(control1_list)
mean_control2 = np.mean(control2_list)

# iterate through 2d experimental data set 1
for i in range(rows):
    for j in range(columns):
        normalize1 = experimental1_list / mean_control1

# iterate through 2d experimental data set 2
for i in range(rows):
    for j in range(columns):
        normalize2 = experimental2_list /  mean_control2


result = pd.DataFrame(normalize1) 
result.to_excel('find_thresh_data1.xlsx')

result = pd.DataFrame(normalize2) 
result.to_excel('find_thresh_data2.xlsx')


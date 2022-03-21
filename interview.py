# Author: Cole Haraga
# Date: March 21, 2022
# AAFC Nano technical Interview 1

# using the Pandas data science library
# panda has some memory leaks but for this problem it is unessecary to fix these
import pandas as pd
#numpy for numpy array types for the excel sheet to array
import numpy as np

# read excel files into a variable
# excel and .py files must be in the same directory(folder) for this method
control1 = pd.read_excel(r'./../AAFC-interview/Exam_control_measurements1.xlsx', header=None)
control2 = pd.read_excel(r'./../AAFC-interview/Exam_control_measurements2.xlsx', header=None)
experimental1 = pd.read_excel(r'./../AAFC-interview/Exam_experimental_measurements1.xlsx', header=None)
experimental2 = pd.read_excel(r'./../AAFC-interview/Exam_experimental_measurements2.xlsx', header=None)

# put values into list
# values are double array for each row into array
control1_list = control1.values.tolist()
control2_list = control2.values.tolist()
experimental1_list = experimental1.values.tolist()
experimental2_list = experimental2.values.tolist()


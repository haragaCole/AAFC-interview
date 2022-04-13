# -----------------------------------------------------------------
# Author: Cole Haraga
# Date: March 21, 2022
# AAFC Nano technical Interview 1
# -----------------------------------------------------------------

# using the Pandas data science library
# panda has some memory leaks and is slow but for this problem it is unessecary to fix these
# for this data set size the time complexity will not affect much
import pandas as pd
#numpy for numpy array types for the excel sheet to array and resizing lists
import numpy as np
# import csv
import csv

# global constants
rows = 8
columns = 12

# read excel files into a variable
# excel and .py files must be in the same directory(folder) for this method
control1 = pd.read_excel(r'Exam_control_measurements1.xlsx', header=None)
control2 = pd.read_excel(r'Exam_control_measurements2.xlsx', header=None)
experimental1 = pd.read_excel(r'Exam_experimental_measurements1.xlsx', header=None)
experimental2 = pd.read_excel(r'Exam_experimental_measurements2.xlsx', header=None)

# put values into list
# values are 2D list for each row into inner list i.e. rows of columns [rows[columns]]
control1_list = control1.values.tolist()
control2_list = control2.values.tolist()
experimental1_list = experimental1.values.tolist()
experimental2_list = experimental2.values.tolist()

# need mean values of each control group to normalize the experimental data points
mean_control1 = np.mean(control1_list)
mean_control2 = np.mean(control2_list)

# normalize experimental and create a 2D list in order from excel that has None type for values under threshold
# also define the threshold and single out those points using IQR
# Arguments: experimental data of list type, mean of control data float type
# return: list of either None type elements or data element if extraneous.
def flag_outliers(experimental_list, mean_control):
    # iterate through 2d experimental data and normalize by dividing each value by the control mean
    # then compare to the threshold of those normalized data points and find spots that exceed it
    flag_points = []
    for i in range(rows):
        for j in range(columns):
            # normalize is 1D list
            normalize = experimental_list / mean_control
            # use IQR method for finding threshold because it is easily adjustable, fast and reliable
            # can adjust upper and lower bounds
            # [upper, lower] percentile of normalize data which is a 1D list
            Q3, Q1 = np.percentile(normalize, [50, 30])
            iqr = Q3 - Q1
            if ((normalize[i][j] >= (Q3 + (1.5*iqr))) or (normalize[i][j] <= (Q1 - (1.5*iqr)))):
                flag_points.append(normalize[i][j])
            else:
                flag_points.append(None)

     # put back into 2D shape of rows and columns
    flag_fixed = np.array(flag_points).reshape(8,12)
    flag_fixed_list = flag_fixed.tolist()
    return(flag_fixed_list)

# iterate through 2d experimental data and normalize by dividing each value by the control mean
# then compare to the threshold of those normalized data points and find spots that exceed it
flag1_fixed_list = flag_outliers(experimental1_list, mean_control1)

# iterate through 2d experimental data and normalize by dividing each value by the control mean
# then compare to the threshold of those normalized data points and find spots that exceed it
flag2_fixed_list = flag_outliers(experimental2_list, mean_control2)

# create excel sheets to visually represent the normalized data and use it to create Box chart
# then use box chart and normalized data to find a pattern of extraneous values
# need normalized data to find extraneous values or clusters
# can comment out if checking box plots isnt needed and personally check for threshold values
normalize1 = []
for i in range(rows):
        for j in range(columns):
            normalize1 = experimental1_list / mean_control1

result1 = pd.DataFrame(normalize1) 
result1.to_excel('TEST_normalized_data1.xlsx', header=False, index=False)

# need normalized data to find extraneous values or clusters
normalize2 = []
for i in range(rows):
        for j in range(columns):
            normalize2 = experimental2_list / mean_control2

result2 = pd.DataFrame(normalize2) 
result2.to_excel('TEST_normalized_data2.xlsx', header=False, index=False)
# end of test files to check normalized data


# use DataFrame of flag_fixed_list to find points that need a coordinate inserted to that value
# use these .csv files to see spreadsheet with extraneous values only shown
# csv file will give the arbitrary header and row index's
# can also test check these files for correct outlier coordinates
to_csv1 = pd.DataFrame(flag1_fixed_list)
to_csv1.to_csv('Experiment1_spreadsheet_with_NoneType.csv', header=False, index=False)
to_csv2 = pd.DataFrame(flag2_fixed_list)
to_csv2.to_csv('Experiment2_spreadsheet_with_NoneType.csv', header=False, index=False)

# For Experiment1
# need to read from file to assign header and row index
# create column names because no headers given, first 12 letter of alphabet
# 12 garunteed columns defined by question
col_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
csv_file1 = pd.read_csv ('Experiment1_spreadsheet_with_NoneType.csv', names=col_names, header=None)
# create index for how many rows there are in file starting at 1
csv_file1.index = np.arange(1, len(csv_file1)+1)

# open spreadsheet that only includes flagged values and NoneType cells
with open('Experiment1_spreadsheet_with_NoneType.csv', newline='') as f:
    reader = csv.reader(f)
    data1 = list(reader)

# For Experiment2
# do the same as for Experiment1 but using data from Experiment2
# to give coordinates make a key for columns (data given always has 2 columns)
col_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
csv_file2 = pd.read_csv ('Experiment2_spreadsheet_with_NoneType.csv', names=col_names, header=None)
# start rows = 1 to end of rows+1 where rows are list locations
csv_file2.index = np.arange(1, len(csv_file2)+1)

with open('Experiment2_spreadsheet_with_NoneType.csv', newline='') as f2:
    reader2 = csv.reader(f2)
    data2 = list(reader2)

# if not NoneType then its a value we want to save into a new list
# want to save outliers along with their column and row keys
#[(column, row, value)...]
def data_wanted(csv_file, data):
    data_wanted = []
    for i in range(rows):
        for j in range(columns):
            if data[i][j] != '':
                loop = col_names[j],csv_file.index[i],data[i][j]
                data_wanted.append(loop)
    return(data_wanted)

# Outliers alone, comma seperated and no cells filled with NoneType in form of tuples
tuple_outliers1 = data_wanted(csv_file1, data1)
tuple_outliers2 = data_wanted(csv_file2, data2)

# convert back to dataframe to be able to become .csv (prework for conversion)
to_csv1 = pd.DataFrame(tuple_outliers1)
to_csv2 = pd.DataFrame(tuple_outliers2)

# convert to .csv file as per requested in tuple form
to_csv1.to_csv('Experiment1_tuple.csv', header=False, index=False)
to_csv2.to_csv('Experiment2_tuple.csv', header=False, index=False)

# strip the comma from the tuple data set between the column and row keys into string value
# return ex. list([A1,1,...])
def stripping(strip):
    strip_list_final = []
    temp = ""
    final_values = []
    #only need first comma in each row of data so single for loop
    # natural algorithm for removing first comma in data sets
    for i in strip:
        for j in range(len(i)):
            if j <= 1:
                temp += str(i[j])
            if j == 1:
                strip_list_final.append(temp)
            if j > 1:
                strip_list_final.append(i[j])
        final_values.append(strip_list_final)
        strip_list_final = []
        temp = ""
    return(final_values)

# strip tuples of their first comma
final_values1 = stripping(tuple_outliers1)
final_values2 = stripping(tuple_outliers2)

# stdout to csv file of stripped tuple outliers to [coordinate, value]*rows
to_csv4 = pd.DataFrame(final_values1)
to_csv4.to_csv('FINAL_Experiment1.csv', header=False, index=False)
to_csv3 = pd.DataFrame(final_values2)
to_csv3.to_csv('FINAL_Experiment2.csv', header=False, index=False)

# time complexity O(2(rows*columns)) + whatever pandas read and write algorithms are 
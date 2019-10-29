import argparse
import os.path
import csv 
import matplotlib.pyplot as plt
import numpy as np

def generate_points(coefs, min_val, max_val):
    xs = np.arange(min_val, max_val, (max_val-min_val)/100)
    return xs, np.polyval(coefs, xs)
def convert_type(element):    
    if element == "":
        return None
    try:
        return int(element)
    except ValueError:
        try:
            return float(element)
        except ValueError:
            return element
def plot_data(dd):
    f,axes = plt.subplots(len(dd.keys()),len(dd.keys()),figsize=(25,25))
    for i, column1 in enumerate(dd.keys()):
        for j, column2 in enumerate(dd.keys()):
                x = dd[column1]
                y = dd[column2]
                axes[i,j].scatter(x, y, c='pink', label='real data' )
                axes[i,j].set_xlabel(column1)
                axes[i,j].set_ylabel(column2)
                axes[i,j].set_title("{0} x {1}".format(column1, column2))
                for m in range(1,5):
                    coefs = np.polyfit(x, y, m)
                    xs, new_line = generate_points(coefs, min(x), max(x))
                    axes[i,j].plot(xs, new_line, label=str(m) + '.order')
    plt.legend(loc='upper left', fontsize='small')
    plt.tight_layout()
    #plt.savefig('homework6ozge.png')
    plt.show()
    

parser = argparse.ArgumentParser()
def exist_file(parser,arg):
    exists = os.path.isfile(arg)
    if exists :
        return open(arg,'r')
    else:
        return parser.error("The file doesn`t exist")

parser.add_argument('file', type=lambda x: exist_file(parser,x))
args = parser.parse_args()
my_read_data = csv.reader(args.file)

outer_list = []
for row in my_read_data:
    row_list = []
    if len(row) == 1:
        row = row[0].split()
    for element in row:
        new_element = convert_type(element)
        if new_element is not "":
            row_list.append(new_element)
    if len(row_list) > 0:
        outer_list += [row_list]
#print(outer_list)
our_dictionary = {}
if type(convert_type(outer_list[0][0])) == str:
    for location, column_headings in enumerate(outer_list[0]):
        our_dictionary[column_headings] = list() 
        for row in outer_list[1:]:
            our_dictionary[column_headings] += [row[location]]
else:
    for i in range(len(outer_list[0])):
        our_dictionary[i] = list()
        for row in outer_list:
            our_dictionary[i] += [row[i]]
#print(our_dictionary)                

plot_data(our_dictionary)

#import pandas as pd
#import seaborn as sns
#df = pd.DataFrame(our_dictionary)
#sns.pairplot(df, height=0.75, aspect=1.5)
#plt.show()
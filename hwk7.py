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
def plot_data(dd, plot=False):
    if plot:
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
        plt.savefig('homework7ozge.png')
        plt.show()

def exist_file(data_file, delimiter):
    exists = os.path.isfile(data_file)
    if exists :
        with open(data_file,'r') as fhandle:
            my_read_data = csv.reader(fhandle, delimiter=delimiter)
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
        return outer_list     
def lines_to_dict(outer_list):
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
    return our_dictionary

def col_name(col_head,summary=False):
    if summary:
        assert summary in col_head.keys() , 'column name does not exist'
        for k in col_head.keys():
            if k == summary:
               yep = col_head[k]
        if len(np.unique(yep))/len(yep) <  0.1:
            print('Column is categorical/discrete')
        else:
            print('Column is continuous')      
        print('min is '+ str(min(yep)))
        print('max is ' + str(max(yep)))
        print('mean is ' + str(np.mean(yep)))
        print('std is ' + str(np.std(yep)))
    
    
def interp_f(funct,interpolate=False):
    if interpolate:
        assert interpolate[0] in funct.keys() , 'column name does not exist for interpolate'
        assert interpolate[1] in funct.keys() , 'column name does not exist for interpolate'
        assert len(np.unique(funct[interpolate[0]]))/len(funct[interpolate[0]]) >  0.1 , 'first column is discrete'
        assert len(np.unique(funct[interpolate[1]]))/len(funct[interpolate[1]]) >  0.1 , 'second column is discrete'
        assert min(funct[interpolate[0]]) <= convert_type(interpolate[2]) <= max(funct[interpolate[0]]), 'use --summary to find the value'
        for m in range(1,4):
            number = convert_type(interpolate[2])
            coef1 = np.polyfit(funct[interpolate[0]],funct[interpolate[1]],m)
            y = np.polyval(coef1, number)
            print(str(y) + ' ' + str(m) + '.order')
            plt.scatter(funct[interpolate[0]],funct[interpolate[1]], c='pink')
            xs, new_line = generate_points(coef1, min(funct[interpolate[0]]), max(funct[interpolate[0]]))
            plt.plot(xs, new_line, label=str(m) + '.order')   
        plt.xlabel(interpolate[0])
        plt.ylabel(interpolate[1])
        plt.legend(loc='lower right', fontsize='x-small')
        plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", type=str,
                        help="Input CSV data file for plotting")
    parser.add_argument("delimiter", type=str,
                        help="the delimiter used in your file")                       
    #parser.add_argument('-H', '--header', action="store_true",
    #                    help="determines if a header is present")
    parser.add_argument('-p', '--plot', action='store_true',
                        help='plot dictionary')
    parser.add_argument('-s', '--summary',type=str,
                        help= "accept column name")
    parser.add_argument('-i', '--interpolate', nargs=3, type=str,
                        help="two column names and a value")
    args = parser.parse_args()
    my_data = exist_file(args.data_file, args.delimiter)
    data_dictionary = lines_to_dict(my_data) #header=args.header)
    plot_data(data_dictionary, plot=args.plot)
    col_name(data_dictionary,summary=args.summary)
    interp_f(data_dictionary,interpolate=args.interpolate)
    #print(data_dictionary)
if __name__ == "__main__":
    main()

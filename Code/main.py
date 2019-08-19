# importing libraries numpy and pandas for data storage and processing
import pandas as pd
import argparse
from pruning import prune
import pruning
import Making_the_tree
from Making_the_tree import make_tree
from prediction import prediction
from datetime import datetime

# initiate the parser
parser = argparse.ArgumentParser()

# add long and short argument
parser.add_argument("--train_data", "-t", help="Specify training csv file")
parser.add_argument("--test_data", "-e", help="Specify testing csv file")
parser.add_argument("--min_leaf_size", "-m", help="Specify minimum leaf size")
parser.add_argument("--absolute", "-a", help="Specify if we take absolute error", action="store_true")
parser.add_argument("--mean_squared", "-s", help="Specify if we take mean squared error", default=True, action="store_true")

# read arguments from the command line
args = parser.parse_args()

# Getting the command line arguments
file_to_train_from = args.train_data
file_to_test = args.test_data

Making_the_tree.min_leaf_size = int(args.min_leaf_size)

if args.absolute is True:
    Making_the_tree.error_function = Making_the_tree.abs_error_of_data
    pruning.error_function = pruning.abs_error_of_data
else:
    Making_the_tree.error_function = Making_the_tree.mean_squared_error_of_data
    pruning.error_function = pruning.mean_squared_error_of_data

# Reading the data
train_data = pd.read_csv(file_to_train_from)
test_data = pd.read_csv(file_to_test)
output = test_data.columns.values[-1]

# Separating data for training ,and pruning
a, b = train_data.shape

tree_making_data = train_data.loc[:int(2*a/3), :]
pruning_data = train_data.loc[int(2*a/3):, :]

tree = make_tree(train_data)
pruned_tree = prune(tree, pruning_data)

time_mean_square_error_df = 'min_leaf_size delta_t mean_squared_error'.split()

out_df = prediction(test_data, tree)[["index", "prediction"]]

out_df.columns = ["Id", "output"]
out_df.to_csv('unpruned_mean_squared_wine.csv', index=False)
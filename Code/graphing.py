import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os

training_file = "wine_train_train.csv"
testing_file = "wine_train_test.csv"

for min_leaf_size in range(25, 50):
    print(min_leaf_size)
    command = "graphing_main.py --train_data " + training_file + " --test_data " + testing_file + " --min_leaf_size " + str(min_leaf_size) + " --absolute"
    os.system(command)

df = pd.read_csv("data_to_make_graph.csv")
plt.plot(df['min_leaf_size'], df['mean_squared_error'])
plt.show()
#plt.savefig("Absolute error vs number of leaves for wine quality.png")

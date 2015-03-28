# Why I made this code
This code was written because of the need to count groupings of a large number of user events generated by a web app. See the section "What it is and isn't" before trying to use this code.

# Quickstart
Assuming you have MongoDB, you need to set the addresses, database names, and collection names in both `common_multicore.py` and `common_item_analysis_agg.py`

Running `./run_it_all.sh` from the root folder of this repo will run the complete workflow on test data located in the `/test/input` directory. In that folder is also a script to generate the test data in case you want to vary the parameters used to generate the test data. Outputs of the workflow will be generated in `/test/output`.

# What it is and isn't
This repo uses python multiprocessing and MongoDB to accomplish a (local) MapReduce job in which the frequency of items and sets of items in a list of transactions are counted. This code can be easily modified to accomplish a number of MapReduce type jobs including word count, large data-set filtering, and joining a large dataset with one or multiple small datasets.

This code is not meant to provide a generalized framework for parellel processing or MapReduce. Instead it is meant to provide a starting place for accomplishing such tasks when complete code transparency and accessibility is necessary. I recommend you try using a library like mrjob or a framework like Spark before trying to write your own parallelization code. Asking questions of data is typically most successful when done quickly, and relying on libraries and frameworks to deal with as much of the complexity as possible typically facilitates this speed.

# Code structure
The core of this code lives in two files: `common_multicore.py` and `common_item_analysis_agg.py`

There is some information that is necessarily redundant in these two files that if changed will break things. Ideally this redundency will be removed in the future for robustness, but currently the redundancy is present to keep things simple.

In both of the two files mentioned at the beginning of this section a Mongo database name, and set of collection names is specified. These must agree for common_item_analysis_agg.py to continue working on the data loaded by common_multicore.py.

# Future and contributions

1. Use Apriori algorithm to prune higher-order combinations
2. Benchmark (single vs multiple processes)
3. Allow for arbitrary jobs (seperate job code .py file? Is this too much like a framework?)
4. Use a common config file to specify Mongo database name and collection names

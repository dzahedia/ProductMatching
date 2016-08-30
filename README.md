# ProductMatching
A text crunching app

In short, it first takes a list of products, over 700, and trains a model. Then, it takes a listings of over 20000 products and finds their match in the original products list.

The products and listings files are in the data directory and the produced matches are in the result/results.txt; also, there is a short summary file in the result/summary.txt.

This application is specific for json formatted files; however, it can easily be generalized for other formats.

Also, it can be used for batch processing as well as stream processing, and its API can be easily enriched.

Just clone and run go.sh
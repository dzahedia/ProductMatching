#! /bin/bash
echo
echo "----------------------------------------------"
echo "-------------    David Zahedi    -------------"
echo "----------------------------------------------"
echo
echo "Before we go:"
echo "This program assumes that Python3, Spark and NumPy are installed in your system."
echo "If your Spark is tied to a Hadoop Cluster; you need to uncomment/comment two lines in the entrypoint.py"
echo
echo "Good to know"
echo "The results file location: results/results.txt"
echo "The summary file location: results/summary.txt"
echo "If you want, you can easily change those locations at entrypoint.py"
echo
echo "Do you want to continue? (y/n)"
read req
if [ "$req" == "y" ]
  then
  echo "It won't take more than 2 minutes!"
  python3 entrypoint.py
fi
echo "Done"


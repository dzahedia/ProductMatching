#! /bin/bash
echo "----------------------------------------------"
echo "Some setting info before we run the program"
echo "The results file location: results/results.txt"
echo "The summary file location: results/summary.txt"
echo "If you want, you can easily change those locations at entrypoint.py"
echo
echo "More importantly, this program assumes that Python3, Spark and NumPy are installed in your system."
echo
echo "Do you want to continue? (y/n)"
read req
if [ "$req" == "y" ]
  then
  echo "It won't take more than 2 minutes!"
  python3 entrypoint.py
fi
echo "Done"


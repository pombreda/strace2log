strace2log
==========

First get a strace.out file

    $ strace -f -o strace.out ./sysbench ...
  
And then run, full path of the strace.out file is a parameter
  
    $ ./analysis.py /home/jchoi/tracefiles/strace.out

import subprocess

def draw_graph(_log_file_name):
    proc = subprocess.Popen(['gnuplot', '-p'],
                            shell=True,
                            stdin=subprocess.PIPE,)
    proc.stdin.write('set terminal png\n')
    proc.stdin.write('set datafile separator ","\n')
    proc.stdin.write('set output "' + _log_file_name + '.png"\n')
    proc.stdin.write('set title "' + _log_file_name + '"\n')
    proc.stdin.write('set ylabel "File Offset"\n')
    proc.stdin.write('set xlabel "Sequential Runs"\n')
    #proc.stdin.write('set size 2, 2\n')
    #proc.stdin.write('set linetype 1 lc rgb "blue"\n')
    #proc.stdin.write('set linetype 2 lc rgb "red"\n')
    proc.stdin.write('plot "' + _log_file_name + '" u 1:2:2:3:3 t "read" with candlesticks, ')
    proc.stdin.write('"' + _log_file_name + '" u 1:4:4:5:5 t "write" with candlesticks\n')
    proc.stdin.write('quit\n')

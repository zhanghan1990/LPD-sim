set terminal postscript eps color
set size 0.5,0.5
set output  "queue_eps"
set xlabel  "time(s)"
set ylabel  "queue length(pkts)"
set xrange[0.4:2]
set yrange[0:600]
plot  "queue" using 1:202 w l   title "queue"

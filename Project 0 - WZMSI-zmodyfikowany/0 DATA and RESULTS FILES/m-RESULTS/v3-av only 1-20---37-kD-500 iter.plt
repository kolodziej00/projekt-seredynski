set style data lines
set xrange [0:500]
set yrange [0:1.0]
set xlabel "iteration"
set ylabel "kD freq"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
#set label "num of experiments=50" at 200,110
#set label "b=1.4" at 200,105
plot 'std_results.txt' using 1:20 with lines lc 7 lw 3 title "av 0-D",\
'std_results.txt' using 1:22 with lines lc 3 lw 3 title "av 1-D",\
'std_results.txt' using 1:24 with lines lc 8 lw 3 title "av 2-D",\
'std_results.txt' using 1:26 with lines lc 2 lw 3 title "av 3-D",\
'std_results.txt' using 1:28 with lines lc 4 lw 3 title "av 4-D",\
'std_results.txt' using 1:30 with lines lc 5 lw 3 title "av 5-D",\
'std_results.txt' using 1:32 with lines lc 6 lw 3 title "av 6-D",\
'std_results.txt' using 1:34 with lines lc 9 lw 3 title "av 7-D",\
'std_results.txt' using 1:36 with lines lc 4 lw 3 title "av 8-D"





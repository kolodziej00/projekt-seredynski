set style data lines
set xrange [0:1000]
set yrange [0:1.1]
set xlabel "iteration"
set ylabel "agents [%]"
#set key at 475,80
#set label "b=1.4, k=3" at 5,110
#set label "num of experiments=50" at 200,110
#set label "50 single runs" at 200,110
#set label "b=1.6" at 40,80
plot 'results.txt' using 1:2 with lines lc 7 lw 3 title "av num of C",\
'results.txt' using 1:3 with lines lc 3 lw 3 title "av num of C correct",\
'results.txt' using 1:4 with lines lc 4 lw 3 title "av payoff",\
'results.txt' using 1:10 with lines lc 2 lw 3 title "av num of strat change"


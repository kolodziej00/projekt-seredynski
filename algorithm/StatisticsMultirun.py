import numpy as np
from math import sqrt
class StatisticsMultirun:
    def __init__(self, statistics, num_of_iter, num_of_exp):
            self.statistics = statistics
            self.num_of_iter = num_of_iter
            self.num_of_exp = num_of_exp

            self.avg_f_C = np.zeros(self.num_of_iter)
            self.std_f_C = np.zeros(self.num_of_iter)
            self.avg_f_C_corr = np.zeros(self.num_of_iter)
            self.std_f_C_corr = np.zeros(self.num_of_iter)
            self.avg_av_pay = np.zeros(self.num_of_iter)
            self.std_av_pay = np.zeros(self.num_of_iter)
            self.avg_f_cr_0s = np.zeros(self.num_of_iter)
            self.std_f_cr_0s = np.zeros(self.num_of_iter)
            self.avg_f_cr_1s = np.zeros(self.num_of_iter)
            self.std_f_cr_1s = np.zeros(self.num_of_iter)
            self.avg_f_allC = np.zeros(self.num_of_iter)
            self.std_f_allC = np.zeros(self.num_of_iter)
            self.avg_f_allD = np.zeros(self.num_of_iter)
            self.std_f_allD = np.zeros(self.num_of_iter)
            self.avg_f_kD = np.zeros(self.num_of_iter)
            self.std_f_kD = np.zeros(self.num_of_iter)
            self.avg_f_kC = np.zeros(self.num_of_iter)
            self.std_f_kC = np.zeros(self.num_of_iter)
            self.avg_f_kDC = np.zeros(self.num_of_iter)
            self.std_f_kDC = np.zeros(self.num_of_iter)
            self.avg_f_strat_ch = np.zeros(self.num_of_iter)
            self.std_f_strat_ch = np.zeros(self.num_of_iter)
            self.avg_f_strat_ch_final = np.zeros(self.num_of_iter)
            self.std_f_strat_ch_final = np.zeros(self.num_of_iter)

            self.calculate_stats()

    def calculate_stats(self):
        # sum values for each iter in all experiments
        for experiment, statistics in self.statistics:
            for statistic in statistics:
                self.avg_f_C[statistic.iter] += statistic.f_C
                self.avg_f_C_corr[statistic.iter] += statistic.f_C_corr
                self.avg_av_pay[statistic.iter] += statistic.av_sum
                self.avg_f_cr_0s[statistic.iter] += statistic.f_cr_0s
                self.avg_f_cr_1s[statistic.iter] += statistic.f_cr_1s
                self.avg_f_allC[statistic.iter] += statistic.f_allC
                self.avg_f_allD[statistic.iter] += statistic.f_allD
                self.avg_f_kC[statistic.iter] += statistic.f_kC
                self.avg_f_kD[statistic.iter] += statistic.f_kD
                self.avg_f_kDC[statistic.iter] += statistic.f_kDC
                self.avg_f_strat_ch[statistic.iter] += statistic.f_strat_ch
                self.avg_f_strat_ch_final[statistic.iter] += statistic.f_strat_ch_final

        # divide sums by number of experiments to get average value
        for i in range(0, self.num_of_iter):
            self.avg_f_C[i] /= self.num_of_exp
            self.avg_f_C_corr[i] /= self.num_of_exp
            self.avg_av_pay[i] /= self.num_of_exp
            self.avg_f_cr_0s[i] /= self.num_of_exp
            self.avg_f_cr_1s[i] /= self.num_of_exp
            self.avg_f_allC[i] /= self.num_of_exp
            self.avg_f_allD[i] /= self.num_of_exp
            self.avg_f_kC[i] /= self.num_of_exp
            self.avg_f_kD[i] /= self.num_of_exp
            self.avg_f_kDC[i] /= self.num_of_exp
            self.avg_f_strat_ch[i] /= self.num_of_exp
            self.avg_f_strat_ch_final[i] /= self.num_of_exp

        # calculate sum of difference between value and average raised to power of 2
        for experiment, statistics in self.statistics:
            for statistic in statistics:
                self.std_f_C[statistic.iter] += pow(statistic.f_C - self.avg_f_C[statistic.iter], 2)
                self.std_f_C_corr[statistic.iter] += pow(statistic.f_C_corr - self.avg_f_C_corr[statistic.iter],2)
                self.std_av_pay[statistic.iter] += pow(statistic.av_sum - self.avg_av_pay[statistic.iter], 2)
                self.std_f_cr_0s[statistic.iter] += pow(statistic.f_cr_0s - self.avg_f_cr_0s[statistic.iter], 2)
                self.std_f_cr_1s[statistic.iter] += pow(statistic.f_cr_1s - self.avg_f_cr_1s[statistic.iter], 2)
                self.std_f_allC[statistic.iter] += pow(statistic.f_allC - self.avg_f_allC[statistic.iter], 2)
                self.std_f_allD[statistic.iter] += pow(statistic.f_allD - self.avg_f_allD[statistic.iter], 2)
                self.std_f_kC[statistic.iter] += pow(statistic.f_kC - self.avg_f_kC[statistic.iter], 2)
                self.std_f_kD[statistic.iter] += pow(statistic.f_kD - self.avg_f_kD[statistic.iter], 2)
                self.std_f_kDC[statistic.iter] += pow(statistic.f_kDC - self.avg_f_kDC[statistic.iter], 2)
                self.std_f_strat_ch[statistic.iter] += pow(statistic.f_strat_ch - self.avg_f_strat_ch[statistic.iter], 2)
                self.std_f_strat_ch_final[statistic.iter] += pow(statistic.f_strat_ch_final - self.avg_f_strat_ch_final[statistic.iter], 2)

        for i in range(0, self.num_of_iter):
            self.std_f_C[i] /= self.num_of_exp
            self.std_f_C_corr[i] /= self.num_of_exp
            self.std_av_pay[i] /= self.num_of_exp
            self.std_f_cr_0s[i] /= self.num_of_exp
            self.std_f_cr_1s[i] /= self.num_of_exp
            self.std_f_allC[i] /= self.num_of_exp
            self.std_f_allD[i] /= self.num_of_exp
            self.std_f_kC[i] /= self.num_of_exp
            self.std_f_kD[i] /= self.num_of_exp
            self.std_f_kDC[i] /= self.num_of_exp
            self.std_f_strat_ch[i] /= self.num_of_exp
            self.std_f_strat_ch_final[i] /= self.num_of_exp

            self.std_f_C[i] = sqrt(self.std_f_C[i])
            self.std_f_C_corr[i] = sqrt(self.std_f_C_corr[i])
            self.std_av_pay[i] = sqrt(self.std_av_pay[i])
            self.std_f_cr_0s[i] = sqrt(self.std_f_cr_0s[i])
            self.std_f_cr_1s[i] = sqrt(self.std_f_cr_1s[i])
            self.std_f_allC[i] = sqrt(self.std_f_allC[i])
            self.std_f_allD[i] = sqrt(self.std_f_allD[i])
            self.std_f_kC[i] = sqrt(self.std_f_kC[i])
            self.std_f_kD[i] = sqrt(self.std_f_kD[i])
            self.std_f_kDC[i] = sqrt(self.std_f_kDC[i])
            self.std_f_strat_ch[i] = sqrt(self.std_f_strat_ch[i])
            self.std_f_strat_ch_final[i] = sqrt(self.std_f_strat_ch_final[i])

    def write_to_file(self, f):
        for i in range(self.num_of_iter):
            f.write("{0:<10.0f}{1:<16.4f}{2:<17.4f}{3:<20.4f}{4:<21.4f}{5:<19.4f}".format(i, self.avg_f_C[i], self.std_f_C[i], self.avg_f_C_corr[i],
                                                                                        self.std_f_C_corr[i], self.avg_av_pay[i]))
            f.write("{0:<20.4f}{1:<20.4f}{2:<21.4f}{3:<20.4f}{4:<21.4f}".format(self.std_av_pay[i], self.avg_f_cr_0s[i], self.std_f_cr_0s[i], self.avg_f_cr_1s[i],
                                                                           self.std_f_cr_1s[i]))
            f.write("{0:<19.4f}{1:<20.4f}{2:<19.4f}{3:<20.4f}{4:<18.4f}".format(self.avg_f_allC[i], self.std_f_allC[i], self.avg_f_allD[i], self.std_f_allD[i],
                                                                           self.avg_f_kD[i]))
            f.write("{0:<19.4f}{1:<18.4f}{2:<19.4f}{3:<19.4f}{4:<20.4f}".format(self.std_f_kD[i], self.avg_f_kC[i], self.std_f_kC[i], self.avg_f_kDC[i],
                                                            self.std_f_kDC[i]))
            f.write("{0:<23.4f}{1:<24.4f}{2:<29.4f}{3:<30.4f}\n".format(self.avg_f_strat_ch[i], self.std_f_strat_ch[i], self.avg_f_strat_ch_final[i],
                                                        self.std_f_strat_ch_final[i]))





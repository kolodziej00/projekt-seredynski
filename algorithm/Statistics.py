class Statistics:
    def __init__(self, iter, f_C, f_C_corr, av_sum, f_allC, f_allD, f_kD, f_kC,
                 f_kDC, f_strat_ch, f_0D, f_1D, f_2D, f_3D, f_4D, f_5D, f_6D,
                 f_7D, f_8D, f_0C, f_1C, f_2C, f_3C, f_4C, f_5C, f_6C, f_7C, f_8C,
                 f_0DC, f_1DC, f_2DC, f_3DC, f_4DC, f_5DC, f_6DC, f_7DC, f_8DC, f_strat_change_final, f_cr_0s, f_cr_1s):
        self.iter = iter
        self.f_C = f_C
        self.f_C_corr = f_C_corr
        self.av_sum = av_sum
        self.f_allC = f_allC
        self.f_allD = f_allD
        self.f_kD = f_kD
        self.f_kC = f_kC
        self.f_kDC = f_kDC
        self.f_strat_ch = f_strat_ch
        self.f_0D = f_0D
        self.f_1D = f_1D
        self.f_2D = f_2D
        self.f_3D = f_3D
        self.f_4D = f_4D
        self.f_5D = f_5D
        self.f_6D = f_6D
        self.f_7D = f_7D
        self.f_8D = f_8D
        self.f_0C = f_0C
        self.f_1C = f_1C
        self.f_2C = f_2C
        self.f_3C = f_3C
        self.f_4C = f_4C
        self.f_5C = f_5C
        self.f_6C = f_6C
        self.f_7C = f_7C
        self.f_8C = f_8C
        self.f_0DC = f_0DC
        self.f_1DC = f_1DC
        self.f_2DC = f_2DC
        self.f_3DC = f_3DC
        self.f_4DC = f_4DC
        self.f_5DC = f_5DC
        self.f_6DC = f_6DC
        self.f_7DC = f_7DC
        self.f_8DC = f_8DC
        self.f_strat_ch_final = f_strat_change_final
        # cr - counter -_-
        self.f_cr_0s = f_cr_0s
        self.f_cr_1s = f_cr_1s


    def write_stats_to_file(self, f, f2):
        f.write("{0:<10.0f}{1:<13.4f}{2:<18.4f}{3:<16.4f}".format(self.iter, self.f_C, self.f_C_corr, self.av_sum))
        f.write("{0:<16.4f}{1:<16.4f}{2:<14.4f}".format(self.f_allC, self.f_allD, self.f_kD))
        f.write("{0:<14.4f}{1:<15.4f}{2:<20.4f}".format(self.f_kC, self.f_kDC,self.f_strat_ch))
        f.write("{0:<26.4f}{1:<17.4f}{2:<17.4f}\n".format(self.f_strat_ch_final, self.f_cr_0s, self.f_cr_1s))
        f2.write("{0:<10.0f}".format(self.iter))
        f2.write("{0:<14.4f}{1:<14.4f}{2:<14.4f}{3:<14.4f}{4:<14.4f}".format(self.f_0D, self.f_1D, self.f_2D, self.f_3D, self.f_4D))
        f2.write("{0:<14.4f}{1:<14.4f}{2:<14.4f}{3:<14.4f}".format(self.f_5D, self.f_6D, self.f_7D, self.f_8D))
        f2.write("{0:<14.4f}{1:<14.4f}{2:<14.4f}{3:<14.4f}".format(self.f_0C, self.f_1C, self.f_2C, self.f_3C))
        f2.write("{0:<14.4f}{1:<14.4f}{2:<14.4f}{3:<14.4f}".format(self.f_4C, self.f_5C, self.f_6C, self.f_7C))
        f2.write("{0:<14.4f}{1:<15.4f}{2:<15.4f}{3:<15.4f}".format(self.f_8C, self.f_0DC, self.f_1DC, self.f_2DC))
        f2.write("{0:<15.4f}{1:<15.4f}{2:<15.4f}{3:<15.4f}".format(self.f_3DC, self.f_4DC, self.f_5DC, self.f_6DC))
        f2.write("{0:<15.4f}{1:<15.4f}\n".format(self.f_7DC, self.f_8DC))


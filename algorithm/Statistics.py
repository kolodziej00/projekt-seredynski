class Statistics:
    def __init__(self, iter, f_C, f_C_corr, av_sum, f_allC, f_allD, f_kD, f_kC,
                 f_kDC, f_strat_ch, f_0D, f_1D, f_2D, f_3D, f_4D, f_5D, f_6D,
                 f_7D, f_8D, f_0C, f_1C, f_2C, f_3C, f_4C, f_5C, f_6C, f_7C, f_8C,
                 f_0DC, f_1DC, f_2DC, f_3DC, f_4DC, f_5DC, f_6DC, f_7DC, f_8DC):
        self.iter = iter
        self.f_C = round(f_C, 4)
        self.f_C_corr = round(f_C_corr, 4)
        self.av_sum = round(av_sum, 4)
        self.f_allC = round(f_allC, 4)
        self.f_allD = round(f_allD, 4)
        self.f_kD = round(f_kD, 4)
        self.f_kC = round(f_kC, 4)
        self.f_kDC = round(f_kDC, 4)
        self.f_strat_ch = round(f_strat_ch, 4)
        self.f_0D = round(f_0D, 4)
        self.f_1D = round(f_1D, 4)
        self.f_2D = round(f_2D, 4)
        self.f_3D = round(f_3D, 4)
        self.f_4D = round(f_4D, 4)
        self.f_5D = round(f_5D, 4)
        self.f_6D = round(f_6D, 4)
        self.f_7D = round(f_7D, 4)
        self.f_8D = round(f_8D, 4)
        self.f_0C = round(f_0C, 4)
        self.f_1C = round(f_1C, 4)
        self.f_2C = round(f_2C, 4)
        self.f_3C = round(f_3C, 4)
        self.f_4C = round(f_4C, 4)
        self.f_5C = round(f_5C, 4)
        self.f_6C = round(f_6C, 4)
        self.f_7C = round(f_7C, 4)
        self.f_8C = round(f_8C, 4)
        self.f_0DC = round(f_0DC, 4)
        self.f_1DC = round(f_1DC, 4)
        self.f_2DC = round(f_2DC, 4)
        self.f_3DC = round(f_3DC, 4)
        self.f_4DC = round(f_4DC, 4)
        self.f_5DC = round(f_5DC, 4)
        self.f_6DC = round(f_6DC, 4)
        self.f_7DC = round(f_7DC, 4)
        self.f_8DC = round(f_8DC, 4)






    def write_stats_to_file(self, f):
        f.write(str(self.iter) + "             " + str(self.f_C) + "        " + str(self.f_C_corr)  + "          "  + str(self.av_sum))
        f.write("           " + str(self.f_allC) + "      " + str(self.f_allD) + "        "  + str(self.f_kD) + "      ")
        f.write(str(self.f_kC) + "      " + str(self.f_kDC)  + "      "  + str(self.f_strat_ch)  + "             "  + str(self.f_0D))
        f.write("      " + str(self.f_1D)  + "      " + str(self.f_2D)  + "      " + str(self.f_3D)  + "      "  + str(self.f_4D))
        f.write("      " + str(self.f_5D)  + "      "  + str(self.f_6D)  + "      "  + str(self.f_7D)  + "       "  + str(self.f_8D))
        f.write("      " + str(self.f_0C)  + "      " + str(self.f_1C)  + "      " + str(self.f_2C)  + "      "  + str(self.f_3C))
        f.write("       " + str(self.f_4C)  + "      "  + str(self.f_5C)  + "      "  + str(self.f_6C)  + "      "  + str(self.f_7C))
        f.write("      " + str(self.f_8C)  + "      " + str(self.f_0DC)  + "      " + str(self.f_1DC)  + "      "  + str(self.f_2DC))
        f.write("      " + str(self.f_3DC)  + "      "  + str(self.f_4DC)  + "       "  + str(self.f_5DC)  + "      "  + str(self.f_6DC))
        f.write("      " + str(self.f_7DC)  + "      " + str(self.f_8DC) + "\n")


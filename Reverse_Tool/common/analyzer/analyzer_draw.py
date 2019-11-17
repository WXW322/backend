import matplotlib.pyplot as  plt
import numpy as np

class drawer:
    def draw_line(self, X, Y):
        plt.plot(X, Y)

    def plot_linefigureone(file_to, x_lable, y_lable, datas_X, datas_Y, colors, labels, makers, xranges=None, yranges=None):
        plt.xlabel(x_lable)
        plt.ylabel(y_lable)
        t_len = len(datas_X)
        i = 0
        while (i < t_len):
            plt.plot(datas_X[i], datas_Y[i], colors[i], label=labels[i], marker=makers[i])
            i = i + 1
        plt.show()

    def draw_hist(self, data):
        t_min = min(data)
        t_max = max(data)
        t_start = int(t_min / 10)
        t_end = int(t_max / 10)
        a = np.array(data)
        plt.hist(data, bins = [i*10 for i in range(t_start,t_end + 1)])
        plt.show()

if __name__ == '__main__':
    dd = drawer()
    dd.draw_hist([22,87,5,43,56,73,55,54,11,20,51,5,79,31,27])
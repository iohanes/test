#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from ROOT import TCanvas

from Models import NBDAnalyticRetreiver, BinMoment
from Utilities import draw_and_save


def main():
    c1 = TCanvas('c1', 'Test', 800, 800)
    # hists = [gen_histogram('normal', 'Strange distribution; x; counts', 100)]
    # readers = [DataRetreiver('normal', 'Strange distribution; x; counts')]
    # readers = [GaussLikeRetreiver('norm1', 'Random Nev=1e8; x; counts', (1, 60)), GaussLikeAnalyticRetreiver('norm2', 'Analytic; x; counts', (1, 60)) ]
    readers = [NBDAnalyticRetreiver('norm1', 'Nbd ; counts') ]
    # hists = [r.get_hist(59, (1, 70), gamma=0.5, sigma=10, ssize=10000000, n=10, p= 100) for r in readers]
    n , p = 70, 0.5
    hists = [r.get_hist(95, (30, 125), start=30, stop=125, n=n, p=p) for r in readers]
    # hists = [gen_function('normal', 'NBD analytic; x; counts')]
    # hists = [gen_histogram('normal', 'Smaller statistics NBD; x; counts', int(1e07)), gen_histogram('golden', 'Bigger statistics NBD; x; counts', int(1e8))]
    # hists = [gen_histogram('normal', 'Smaller statistics NBD; x; counts'), gen_histogram('golden', 'Golden Ratio; x; counts', ( (5 ** 0.5) - 1 ) / 2.)]
    # readers = [RWalkRetreiver('random_walks_data', 'Golden'), RWalkRetreiver('random_walks_data_nongold', 'Simple')][::-1]
    # hists = [r.get_hist(100, (1, 65), gamma=0.5, sigma=10, ssize=1000000) for r in readers]

    colors = [38]#, 46]

    for h, c in zip(hists, colors):
        binner = BinMoment(h)
        coef = binner.get_moments()
        # print 'coefs', coef
        j = np.arange(coef.size) + 1
        # plt.plot(j, coef , label = h.GetTitle())
        plt.plot(j[0:60], coef[0:60], 'o-',label = h.GetTitle() + ' n =  %d, p = %.2g' % (n, p))
        plt.legend(loc='lower center')
        plt.xlabel('j -- bin number')
        plt.ylabel('C_{j}')
        # plt.yscale('log')
        h.SetLineColor(c)
        h.Scale(1. / h.Integral())
        h.Draw('hist same')

    name = hists[0].GetName()
    draw_and_save('jhist_' + name, True, True)
    plt.savefig('jc_' + name + '.png')
    plt.show()



if __name__ == '__main__':
    main(       )
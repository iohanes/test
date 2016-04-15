#!/usr/bin/env python2

import numpy as np
from ROOT import TH1D
from Utilities import draw_and_save
import matplotlib.pyplot as plt

class BinMoment(object):
    def __init__(self, histogram):
        super(BinMoment, self).__init__()
        self.histogram = histogram

    def get_bins(self):
        N = self.histogram.GetNbinsX()
        bins = np.array([self.histogram.GetBinContent(i) for i in range(1, N + 1)])
        return bins, N

    def get_moments(self):
        bins, N = self.get_bins()
        A = np.repeat(bins[::-1], N, axis =0) # Duplicate N times original array 
        A = np.reshape(A, (N, N)).T           # Create NxN dimensional matrix from 
        A = np.tril(A)                        # Lower tirangular matrix as required by equation
        b = bins * np.array([i for i in range(1, N + 1)])

        print 'bins', bins
        print 'args', b
        print 'matrix:\n', A

        return np.linalg.solve(A, b)

class TH1R(TH1D):
    def __init__(self, *arg):
        super(TH1R, self).__init__(*arg)

    @staticmethod
    def FromNpArray(data, edges, name='mDistr', title="Some title"):
        hist = TH1R(name, title, data.size, edges.min(), edges.max())
        for i, p in enumerate(data): hist.SetBinContent(i + 1, p)
        return hist

    def Draw(self, options="hist"):
        xaxis  = self.GetXaxis()
        xtitle = xaxis.GetTitle().split("#Delta")[0] + ", #Delta = " + str(self.GetBinWidth(1))
        xaxis.SetTitle(xtitle)
        super(TH1R, self).Draw(options)
  

class RandomWalker:
    def __init__(self, steps):
        self.nsteps = steps
        self.random_step = lambda lamda, x, eps: eps * lamda  ** x
        self.random_walk = lambda n, l: np.array([self.random_path(l) for i in range(n)])


    def random_path(self, lamda):
        powers, epsilon = np.arange(self.nsteps), np.random.choice([-1, 1], self.nsteps)
        result = map(lambda x, eps : self.random_step(lamda, x, eps), powers, epsilon)
        return np.sum(result)

def get_histogram(name, title, lamda = 0.74):
    walker = RandomWalker(30)
    data  = walker.random_walk(10000, lamda)
    data, edges = np.histogram(data, 100)

    hist = TH1R.FromNpArray(data, edges, name, title)
    return hist


def main():
    hists = [get_histogram('normal', '#lambda = 0.74; x; counts'), get_histogram('golden', 'Golden Ratio; x; counts', ( (5 ** 0.5) - 1 ) / 2.)]
    colors = [38, 46]

    for h, c in zip(hists, colors):
        binner = BinMoment(h)
        coef = binner.get_moments()
        plt.plot(np.arange(coef.size), coef, label = h.GetTitle())
        plt.legend()
        plt.xlabel('j -- bin number')
        plt.ylabel('C_{j}')
        h.SetLineColor(c)
        h.Draw('hist same')

    plt.savefig('res.png')
    plt.show()

    draw_and_save('test', True, True)


if __name__ == '__main__':
    main()
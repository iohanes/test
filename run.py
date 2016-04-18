#!/usr/bin/env python2

import numpy as np
from ROOT import TH1D, TFile, gROOT, TCanvas, TF1
from Utilities import draw_and_save
from scipy import stats
import matplotlib.pyplot as plt

class BinMoment(object):
    def __init__(self, histogram):
        super(BinMoment, self).__init__()
        self.histogram = histogram

    def get_bins(self):
        N = self.histogram.GetNbinsX()
        # print 'Warning manually deleting zero bins'
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
        gROOT.cd()
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

def gen_histogram(name, title, lamda = 0.74):
    # walker = RandomWalker(30)
    # data  = walker.random_walk(int(1e5), lamda)

    # data = np.random.negative_binomial(29000, 0.9, lamda)
    # print '>>>>>> ', min(data), max(data)
    # data, edges = np.histogram(data, -2971 + 3452, (2971, 3452))


    a, b = -1, 1
    func = TF1('f1', 'TMath::Power(x,[0]) * TMath::Exp(- x * x / ([1] * [1]))', a, b)
    func.SetParameter(0, 1)
    func.SetParameter(1, 0.5)

    data = [func.GetRandom() for i in range(10000) ]
    func.Draw()
    draw_and_save('test', True, True)
    data, edges = np.histogram(data, 100)

    hist = TH1R.FromNpArray(data, edges, name, title)
    return hist

def gen_function(name, title, lamda = 0.74):
    # walker = RandomWalker(30)
    # data  = walker.random_walk(int(1e5), lamda)

    gROOT.cd()

    x = np.arange(3000, 3452, 1)
    nbd = lambda x: stats.nbinom.pmf(x, 29000, 0.9) 
    data = nbd(x)
    print data
    dat1, edges = np.histogram(data, -3000 + 3452, (3000, 3452))
    print data.size, len(edges)
    # plt.plot(x, data)

    hist = TH1R.FromNpArray(data, edges, name, title)
    hist.Draw()
    return hist

def read_histos():
    def process_hist(fname, title, Nbins = 10000):
        data = TFile.Open(fname + '.root')
        fname = fname + '_' + str(Nbins) 
        a, b = data.random_walks.GetMinimum('gratio'), data.random_walks.GetMaximum('gratio')
        hist = TH1R(fname, 'nbins = %d, ' % Nbins + title, Nbins, a, b)
        data.random_walks.Draw('gratio >> ' + fname) 
        return hist

    a = process_hist('random_walks_data', 'Golden Ratio; x; counts')
    b = process_hist('random_walks_data_nongold', '#lambda = 0.74; x; counts')
    return a, b

    # draw_and_save('test', True, True)


def main():
    c1 = TCanvas('c1', 'Test', 800, 800)
    hists = [gen_histogram('normal', 'Strange distribution; x; counts', 100)]
    # hists = [gen_function('normal', 'NBD analytic; x; counts')]
    # hists = [gen_histogram('normal', 'Smaller statistics NBD; x; counts', int(1e07)), gen_histogram('golden', 'Bigger statistics NBD; x; counts', int(1e8))]
    # hists = [gen_histogram('normal', 'Smaller statistics NBD; x; counts'), gen_histogram('golden', 'Golden Ratio; x; counts', ( (5 ** 0.5) - 1 ) / 2.)]
    # hists = read_histos()
    colors = [38]#, 46]

    for h, c in zip(hists, colors):
        binner = BinMoment(h)
        coef = binner.get_moments()
        plt.plot(np.arange(coef.size), coef, label = h.GetTitle())
        plt.legend(loc='lower center')
        plt.xlabel('j -- bin number')
        plt.ylabel('C_{j}')
        h.SetLineColor(c)
        h.Draw('hist same')

    name = hists[0].GetName()
    draw_and_save('hist_' + name, True, True)
    plt.savefig('c_' + name + '.png')
    plt.show()



if __name__ == '__main__':
    main(       )
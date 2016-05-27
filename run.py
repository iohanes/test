#!/usr/bin/env python2

import numpy as np
from ROOT import TH1D, TFile, gROOT, TCanvas, TF1
from Utilities import draw_and_save
from scipy import stats
import matplotlib.pyplot as plt

class DataRetreiver(object):
    def __init__(self, name, title):
        super(DataRetreiver, self).__init__()
        self.name = name
        self.title = title

    def get_data(self, *args, **kwargs):
        pass

    def get_hist(self, *args, **kwargs):
        data = self.get_data(*args, **kwargs)
        data, edges = np.histogram(data, *args)
        hist = TH1R.FromNpArray(data, edges, self.name, self.title)
        return hist

class GaussLikeRetreiver(DataRetreiver):
    def __init__(self, name, title, mrange):
        super(GaussLikeRetreiver, self).__init__(name, title)
        self.mrange = mrange

    def get_func(self, *args, **kwargs):
        a, b = self.mrange 
        func = TF1('f1', 'TMath::Power(x,[0]) * TMath::Exp(- x * x / ([1] * [1]))', a, b)
        func.SetParameter(0, kwargs['gamma'])
        func.SetParameter(1, kwargs['sigma'])
        return func

    def get_data(self, *args, **kwargs):
        func = self.get_func(*args, **kwargs)
        data = [func.GetRandom() for i in range(kwargs['ssize']) ]
        # func.Draw()
        # draw_and_save('test', True, True)
        return data

class GaussLikeAnalyticRetreiver(GaussLikeRetreiver):
    def __init__(self, name, title, mrange):
        super(GaussLikeAnalyticRetreiver, self).__init__(name, title, mrange)

    def get_hist(self, *args, **kwargs):
        func = self.get_func(*args, **kwargs)
        data = np.array([func.Eval(i) for i in range(*self.mrange)])
        x, edges = np.histogram(data, *args)
        hist =  TH1R.FromNpArray(data, edges, self.name, self.title)
        print '>>>>>>>>', len(data), len(edges)
        print data
        return hist


class NBDRetreiver(DataRetreiver):
    def __init__(self, name, title):
        super(NBDRetreiver, self).__init__(name, title)

    def get_data(self, *args, **kwargs):
        # data = np.random.negative_binomial(29000, 0.9, lamda)
        data = np.random.negative_binomial(**kwargs)
        print '>>>>>> ', min(data), max(data)
        return data
        # possibly one needs to overload get_hist
        # data, edges = np.histogram(data, -2971 + 3452, (2971, 3452))

class NBDAnalyticRetreiver(DataRetreiver):
    def __init__(self, name, title):
        super(NBDRetreiver, self).__init__(name, title)

    def get_data(self, *args, **kwargs):
        x = np.arange(kwargs['start'], kwargs['stop'], 1)
        nbd = lambda x: stats.nbinom.pmf(x, kwargs[n], kwargs[p]) 
        data = nbd(x)
        return data
        # dat1, edges = np.histogram(data, -kwargs['start'] + kwargs['stop'], (kwargs['start'], kwargs['stop']))
        # print data.size, len(edges)
      
class RWalkRetreiver(DataRetreiver):
    def __init__(self, name, title):
        super(RWalkRetreiver, self).__init__(name, title)

    def get_hist(self, *args, **kwargs):
        data, nbins = TFile.Open(self.name + '.root'), args[0]
        self.name = self.name + '_' + str(nbins) 
        a, b = data.random_walks.GetMinimum('gratio'), data.random_walks.GetMaximum('gratio')
        hist = TH1R(self.name, 'nbins = %d, ' % nbins + self.title, nbins, a, b)
        data.random_walks.Draw('gratio >> ' + self.name) 
        return hist



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
        A = np.array([np.append(bins[::-1][i:], np.zeros(i)) for i in range(len(bins))])[::-1]
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

  
def main():
    c1 = TCanvas('c1', 'Test', 800, 800)
    # hists = [gen_histogram('normal', 'Strange distribution; x; counts', 100)]
    # readers = [DataRetreiver('normal', 'Strange distribution; x; counts')]
    # readers = [GaussLikeRetreiver('norm1', 'Random Nev=1e8; x; counts', (1, 60)), GaussLikeAnalyticRetreiver('norm2', 'Analytic; x; counts', (1, 60)) ]
    # hists = [r.get_hist(59, (1, 60), gamma=0.5, sigma=10, ssize=100000000) for r in readers]
    # hists = [gen_function('normal', 'NBD analytic; x; counts')]
    # hists = [gen_histogram('normal', 'Smaller statistics NBD; x; counts', int(1e07)), gen_histogram('golden', 'Bigger statistics NBD; x; counts', int(1e8))]
    # hists = [gen_histogram('normal', 'Smaller statistics NBD; x; counts'), gen_histogram('golden', 'Golden Ratio; x; counts', ( (5 ** 0.5) - 1 ) / 2.)]
    readers = [RWalkRetreiver('random_walks_data', 'Golden'), RWalkRetreiver('random_walks_data_nongold', 'Simple')]
    hists = [r.get_hist(100, (1, 60), gamma=0.5, sigma=10, ssize=100000000) for r in readers]

    colors = [38, 46]

    for h, c in zip(hists, colors):
        binner = BinMoment(h)
        coef = binner.get_moments()
        # print 'coefs', coef
        j = np.arange(coef.size) + 1
        # plt.plot(j, coef , label = h.GetTitle())
        plt.plot(j, (j** 4 ) * coef / 1000. , 'o-',label = h.GetTitle())
        plt.legend(loc='lower center')
        plt.xlabel('j -- bin number')
        plt.ylabel('C_{j}  ')
        h.SetLineColor(c)
        h.Scale(1. / h.Integral())
        h.Draw('hist same')

    name = hists[0].GetName()
    draw_and_save('jhist_' + name, True, True)
    plt.savefig('jc_' + name + '.png')
    plt.show()



if __name__ == '__main__':
    main(       )
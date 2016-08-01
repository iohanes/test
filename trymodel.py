#!/usr/bin/python

import numpy as np
from ROOT import TCanvas, TGraph

from Models import NBDAnalyticRetreiver, BinMoment
from Utilities import draw_and_save

def draw_my_plot(start_bin, stop_bin, nbins,  n=70, p=0.5, jpower = 0):
    if n < 0: 
        print 'Parameter "n" should be > 0 !!!\n Aborting...'
        return

    if p < 0 or p > 1 : 
        print 'Parameter "p" should be 0 < p < 1 !!!\n Aborting...'
        return

    c1 = TCanvas('c1', 'Test', 1200, 800)
    c1.Divide(2, 1)

    reader = NBDAnalyticRetreiver('norm1', 'NBD ; counts') 
    h = reader.get_hist(nbins, (start_bin, stop_bin), start=start_bin, stop=stop_bin, n=n, p=p)

    binner = BinMoment(h)
    coef = binner.get_moments()
    j = np.arange(coef.size) + 1

    g = create_graph(j, coef * j ** jpower, 'Analytic NBD n = %0.2g, p = %0.2g; j ; c_{j} j^{%d}' % (n, p, jpower))
    c1.cd(1).SetGrid()
    g.Draw()

    c1.cd(2).SetGrid()
    h.SetLineColor(38)
    h.Scale(1. / h.Integral())
    h.Draw()

    ROOT.enableJSVis()
    c.Draw()
    # draw_and_save('test', draw=True, save=False)

def draw_all():
    from ipywidgets import FloatSlider, IntSlider, interactive
    xstart_slider = IntSlider(value = 30, min=0, max=100, step=1)
    xstop_slider = IntSlider(value = 90, min=0, max=200, step=1)
    nbins_slider = IntSlider(value = 60, min=0, max=200, step=1)
    n_slider = FloatSlider(value = 70, min=0, max=100, step=0.1)
    p_slider = FloatSlider(value = 0.5, min=0, max=1, step=0.01)
    j_slider = IntSlider(value = 0, min = -6, max = 6, step = 1)
    w = interactive(draw_my_plot, start_bin=xstart_slider, stop_bin=xstop_slider, nbins=nbins_slider, n=n_slider, p=p_slider, jpower=j_slider)
    return w

def main():
    draw_my_plot(30, 125, 95, 25.5, 0.45, 5)



def create_graph(x, y, title):
    graph = TGraph()
    for i, (px, py) in enumerate(zip(x,y)):
        graph.SetPoint(i, px, py)
    graph.SetTitle(title)
    graph.SetMarkerStyle(20)
    graph.SetMarkerColor(38)
    graph.SetLineColor(38)

    return graph





if __name__ == '__main__':
    main(       )
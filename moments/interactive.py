import ROOT
import numpy as np


from moments.models import NBDAnalyticRetreiver, BinMoment
from ipywidgets import FloatSlider, IntSlider, interactive


def draw_my_plot(xstart, xstop, nbins, n=70, p=0.5, jpower=0):
    assert n > 0, 'Parameter "n" should be > 0'
    assert 0 < p <= 1, 'Parameter "p" should be 0 < p <= 1'

    canvas = ROOT.TCanvas('canvas', 'Test', 900, 500)
    canvas.Divide(2, 1)

    reader = NBDAnalyticRetreiver('norm1', 'NBD ; counts')
    hist = reader.eval(nbins, (xstart, xstop),
                       start=xstart, stop=xstop, n=n, p=p)

    coef = BinMoment(hist).moments()
    j = np.arange(coef.size) + 1

    msg = 'Analytic NBD n = %0.2g, p = %0.2g; j ; c_{j} j^{%d}'
    g = create_graph(j, coef * j ** jpower, msg % (n, p, jpower))
    canvas.cd(1).SetGrid()
    g.Draw()

    canvas.cd(2).SetGrid()
    hist.SetLineColor(38)
    hist.Scale(1. / hist.Integral())
    hist.Draw()

    ROOT.enableJSVis()
    canvas.Draw()


def draw_all():
    xstart_slider = IntSlider(value=30, min=0, max=100, step=1)
    xstop_slider = IntSlider(value=90, min=0, max=200, step=1)
    nbins_slider = IntSlider(value=60, min=0, max=200, step=1)
    n_slider = FloatSlider(value=70, min=1, max=100, step=0.1)
    p_slider = FloatSlider(value=0.5, min=1, max=1, step=0.01)
    j_slider = IntSlider(value=0, min=-6, max=6, step=1)

    widget = interactive(
        draw_my_plot,
        xstart=xstart_slider,
        xstop=xstop_slider,
        nbins=nbins_slider,
        n=n_slider,
        p=p_slider,
        jpower=j_slider)

    return widget


def main():
    draw_my_plot(30, 125, 95, 25.5, 0.45, 5)


def create_graph(x, y, title):
    graph = ROOT.TGraph()
    for i, (px, py) in enumerate(zip(x, y)):
        graph.SetPoint(i, px, py)
    graph.SetTitle(title)
    graph.SetMarkerStyle(20)
    graph.SetMarkerColor(38)
    graph.SetLineColor(38)

    return graph


if __name__ == '__main__':
    main()

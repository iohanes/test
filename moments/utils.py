import ROOT


class TH1R(ROOT.TH1D):
    def __init__(self, *arg):
        ROOT.gROOT.cd()
        super(TH1R, self).__init__(*arg)

    @staticmethod
    def form(data, edges, name='mDistr', title="Some title"):
        hist = TH1R(name, title, data.size, edges.min(), edges.max())
        for i, p in enumerate(data):
            hist.SetBinContent(i + 1, p)
        return hist

    def Draw(self, options="hist"):
        xaxis = self.GetXaxis()
        xtitle = xaxis.GetTitle().split(
            "#Delta")[0] + ", #Delta = " + str(self.GetBinWidth(1))
        xaxis.SetTitle(xtitle)
        super(TH1R, self).Draw(options)


def save_histogram(h, filename='default'):
    ofile = ROOT.TFile.Open(filename + '.root', 'recreate')
    h.Write()
    ofile.Write()


def draw_and_save(name, draw=True, save=False):
    canvas = ROOT.gROOT.FindObject('c1')
    if not canvas:
        return
    canvas.Update()

    if save:
        canvas.SaveAs("{}.pdf".format(name))

    if draw:
        raw_input('Press enter to continue...')

#!/usr/bin/env python2

import ROOT
import subprocess


class TH1DM(ROOT.TH1D):
    def __init__(self, hist):
        super(TH1DM, self).__init__(hist)

    def Draw(self, options="hist"):
        xaxis  = self.GetXaxis()
        xtitle = xaxis.GetTitle().split("#Delta")[0] + ", #Delta = " + str(self.GetBinWidth(1))
        xaxis.SetTitle(xtitle)
        super(TH1DM, self).Draw(options)
    


def merge_files(files, ofile, directory='pictures/'):
    ifiles  = '.png '.join(files) + '.png'
    command = 'convert ' + ifiles + ' -append ' + ofile + '.png'
    subprocess.Popen('cd %s; pwd; ' % directory + command, shell=True).wait()
    command = 'rm ' + ifiles
    subprocess.Popen('cd %s; ' % directory + command, shell=True)
    # subprocess.Popen('cd %s; ' % directory + command, shell=True)


def save_histogram(h, filename='default'):
    ofile = ROOT.TFile.Open(filename + '.root', 'recreate')
    h.Write()
    ofile.Write()


def draw_and_save(name, draw=True, save=False):
    canvas = ROOT.gROOT.FindObject('c1')
    if not canvas: return
    canvas.Update()
    if save: canvas.SaveAs( name + '.png')
    canvas.Connect("Closed()", "TApplication", ROOT.gApplication, "Terminate()")
    if draw: ROOT.gApplication.Run(True)


def get_my_list(fname='result.ESD.root'):
    mfile = ROOT.TFile(fname)
    mlist = mfile.Data
    return mlist
    
def hist_cut(h, namecut):
    return namecut( h.GetName() ) and h.GetEntries() > 0



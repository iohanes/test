#!/usr/bin/env python2

import ROOT
import subprocess


def save_histogram(h, filename='default'):
    ofile = ROOT.TFile.Open(filename + '.root', 'recreate')
    h.Write()
    ofile.Write()

def draw_and_save(name, draw=True, save=False):
    canvas = ROOT.gROOT.FindObject('c1')
    if not canvas: return
    canvas.Update()
    if save: canvas.SaveAs( name + '.png')
    # canvas.Connect("Closed()", "TApplication", ROOT.gApplication, "Terminate()")
    # if draw: ROOT.gApplication.Run(True)
    if draw: raw_input('Press enter to continue...')


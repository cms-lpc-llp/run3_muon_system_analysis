import numpy as np
import math
from ROOT import ROOT, gROOT, gStyle, gRandom, TSystemDirectory, gPad
from ROOT import TFile, TChain, TTree, TCut, TH1, TH1F, TH1D, TH2F, THStack, TGraph, TGraphAsymmErrors
from ROOT import TStyle, TCanvas, TPad
from ROOT import TLegend, TLatex, TText, TLine, TBox, TGaxis, TAxis
from decimal import Decimal, ROUND_UP, ROUND_HALF_UP

def getRecoTime(algorithm,rechit_cut, rechit_time,rechit_energy):
    # 0 is energy weighted, 1 is energy squared weighted, 2 is median
    rechit_energy = rechit_energy[np.logical_not(rechit_time == -666)]
    rechit_time = rechit_time[np.logical_not(rechit_time == -666)]
    rechit_time = rechit_time[rechit_energy > rechit_cut]
    rechit_energy = rechit_energy[rechit_energy > rechit_cut]
    assert(len(rechit_time) == len(rechit_energy))
    if np.sum(rechit_energy) > 0.0 and len(rechit_time) > 0:
        if algorithm == 0:
            return np.sum(np.multiply(rechit_time,rechit_energy)/np.sum(rechit_energy))
        elif algorithm == 1:
            return np.sum(np.multiply(rechit_time,rechit_energy*rechit_energy)/np.sum(rechit_energy*rechit_energy))
        elif algorithm == 2:
            return np.median(rechit_time)
    else:
        return None


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]

def deltaPhi( p1, p2):
    '''Computes delta phi, handling periodic limit conditions.'''
    #res = abs(p1 - p2)
    #if res > np.pi:
    #    res -= 2*np.pi
    #return res
    return (p1 - p2 + np.pi) % (2 * np.pi) - np.pi

def deltaR( e1, p1, e2, p2):
    de = e1 - e2
    dp = deltaPhi(p1, p2)
    #return math.sqrt(de*de + dp*dp)
    return np.sqrt(de*de + dp*dp)

def drawCMS(LUMI, text, ERA="",onTop=False, left_marg_CMS=0.20,left_marg_LUMI=0.95,text_size=0.045,cms_text_size=0.06,lumi_text_size=0.04,custom_spacing=0,draw_s_only=False, top_marg_cms = 0.98, top_marg_lumi = 0.985):
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(lumi_text_size)
    latex.SetTextColor(1)
    latex.SetTextFont(42)
    latex.SetTextAlign(33)
    era_str = ""
    if ERA!="":
        era_str = ", "+ERA
    if (type(LUMI) is float or type(LUMI) is int) and float(LUMI) > 0:
        lumi_digit = Decimal( str(LUMI/1000.) ).quantize(Decimal('1.0'), rounding=ROUND_HALF_UP) if LUMI/1000.<100. else Decimal( str(LUMI/1000.) ).quantize(Decimal('1.'), rounding=ROUND_UP)
        latex.DrawLatex(left_marg_LUMI, top_marg_lumi, ("%s fb^{-1}  (13.6 TeV%s)") % ( lumi_digit ,era_str ) )#( round(float(LUMI)/1000.,0),era_str) )
    elif type(LUMI) is str:
        latex.DrawLatex(left_marg_LUMI, top_marg_lumi, ("%s fb^{-1}  (13.6 TeV%s)" % (LUMI,era_str)) )
    if draw_s_only:
        latex.DrawLatex(left_marg_LUMI, top_marg_lumi, "#sqrt{s} = 13.6 TeV")
    if not onTop: latex.SetTextAlign(11)
    latex.SetTextFont(62)
    #latex.SetTextSize(0.05 if len(text)>0 else 0.06)
    latex.SetTextSize(cms_text_size)
    latex.DrawLatex(left_marg_CMS, top_marg_cms, "CMS")
    latex.SetTextFont(52)#times 12.5
    spacing = left_marg_CMS+0.3*(cms_text_size/0.06)
    if len(text)>11:
        spacing+=(len(text)/100.)
    if custom_spacing!=0:
        spacing = left_marg_CMS+custom_spacing
    latex.DrawLatex(spacing, top_marg_cms, text)
    return None

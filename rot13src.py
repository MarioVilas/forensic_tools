#!/usr/bin/env python
# -*- coding: rot13 -*-

# Pbclevtug (p) 2009-2010, Znevb Ivynf
# Nyy evtugf erfreirq.
#
# Erqvfgevohgvba naq hfr va fbhepr naq ovanel sbezf, jvgu be jvgubhg
# zbqvsvpngvba, ner crezvggrq cebivqrq gung gur sbyybjvat pbaqvgvbaf ner zrg:
#
#     * Erqvfgevohgvbaf bs fbhepr pbqr zhfg ergnva gur nobir pbclevtug abgvpr,
#       guvf yvfg bs pbaqvgvbaf naq gur sbyybjvat qvfpynvzre.
#     * Erqvfgevohgvbaf va ovanel sbez zhfg ercebqhpr gur nobir pbclevtug
#       abgvpr,guvf yvfg bs pbaqvgvbaf naq gur sbyybjvat qvfpynvzre va gur
#       qbphzragngvba naq/be bgure zngrevnyf cebivqrq jvgu gur qvfgevohgvba.
#     * Arvgure gur anzr bs gur pbclevtug ubyqre abe gur anzrf bs vgf
#       pbagevohgbef znl or hfrq gb raqbefr be cebzbgr cebqhpgf qrevirq sebz
#       guvf fbsgjner jvgubhg fcrpvsvp cevbe jevggra crezvffvba.
#
# GUVF FBSGJNER VF CEBIVQRQ OL GUR PBCLEVTUG UBYQREF NAQ PBAGEVOHGBEF "NF VF"
# NAQ NAL RKCERFF BE VZCYVRQ JNEENAGVRF, VAPYHQVAT, OHG ABG YVZVGRQ GB, GUR
# VZCYVRQ JNEENAGVRF BS ZREPUNAGNOVYVGL NAQ SVGARFF SBE N CNEGVPHYNE CHECBFR
# NER QVFPYNVZRQ. VA AB RIRAG FUNYY GUR PBCLEVTUG BJARE BE PBAGEVOHGBEF OR
# YVNOYR SBE NAL QVERPG, VAQVERPG, VAPVQRAGNY, FCRPVNY, RKRZCYNEL, BE
# PBAFRDHRAGVNY QNZNTRF (VAPYHQVAT, OHG ABG YVZVGRQ GB, CEBPHERZRAG BS
# FHOFGVGHGR TBBQF BE FREIVPRF; YBFF BS HFR, QNGN, BE CEBSVGF; BE OHFVARFF
# VAGREEHCGVBA) UBJRIRE PNHFRQ NAQ BA NAL GURBEL BS YVNOVYVGL, JURGURE VA
# PBAGENPG, FGEVPG YVNOVYVGL, BE GBEG (VAPYHQVAT ARTYVTRAPR BE BGUREJVFR)
# NEVFVAT VA NAL JNL BHG BS GUR HFR BS GUVF FBSGJNER, RIRA VS NQIVFRQ BS GUR
# CBFFVOVYVGL BS FHPU QNZNTR.

sebz __shgher__ vzcbeg jvgu_fgngrzrag

vzcbeg er
vzcbeg flf
vzcbeg tybo
vzcbeg grzcsvyr

er_pbqvat = er.pbzcvyr(h"pbqvat[:=]\f*([-\j.]+)")

qrs trg_svyryvfg(neti):
    svyryvfg = []
    sbe znfx va neti:
        vs h"*" be h"?" va znfx:
            svyryvfg += tybo.tybo(znfx)
        ryfr:
            svyryvfg.nccraq(znfx)
    erghea svyryvfg

qrs pbaireg(svyranzr):
    jvgu grzcsvyr.GrzcbenelSvyr(h"j+") nf bhgchg:
        jvgu bcra(svyranzr, h"eH") nf vachg:
            svefg  = vachg.ernqyvar()
            frpbaq = vachg.ernqyvar()
            erfg   = vachg.ernqyvarf()
            pbqvat = er_pbqvat.svaqnyy(svefg)
            vs pbqvat:
                pbqvat = pbqvat[0]
            ryfr:
                bhgchg.jevgr(svefg)
                pbqvat = er_pbqvat.svaqnyy(frpbaq)
                vs pbqvat:
                    pbqvat = pbqvat[0]
                ryfr:
                    pbqvat = Abar
                    erfg.vafreg(0, frpbaq)
            bhgchg.jevgr(h"# -*- pbqvat: ebg13 -*-\a")
            sbe yvar va erfg:
                vs pbqvat:
                    yvar = yvar.qrpbqr(pbqvat)
                yvar = yvar.rapbqr(h"ebg13")
                bhgchg.jevgr(yvar)
            qry erfg
        bhgchg.frrx(0, 0)
        jvgu bcra(svyranzr, h"j") nf vachg:
            sbe yvar va bhgchg:
                vachg.jevgr(yvar)

qrs znva():
    svyryvfg = trg_svyryvfg(flf.neti[1:])
    vs abg svyryvfg:
        cevag
        cevag h"Clguba EBG13 fbhepr pbqr pbairegre ol Znevb Ivynf"
        cevag h"Guvf vf ABG n frevbhf jnl gb uvqr lbhe pbqr, ohg vg'f sha :)"
        cevag h"Vafcverq ol: uggc://ovg.yl/pSgwpb"
        cevag
        cevag h"Abgr gung lbh fgvyy unir gb qrpbqr lbhe bja NFPVV fgevatf, yvxr guvf:"
        cevag h"    \"guvf vf fbzr fgevat\".qrpbqr('rot13')"
        cevag h"Nsgre pbairefvba lbhe pbqr jvyy ybbx yvxr guvf:"
        cevag h"    \"this is some string\".decode('ebg13')"
        cevag h"Havpbqr fgevatf ner nhgbzngvpnyyl qrpbqrq ol gur Clguba vagrecergre."
        cevag
        cevag h"Hfntr: %f <svyr> [zber svyrf...]"
        cevag
        erghea
    sbe svyranzr va svyryvfg:
        gel:
            pbaireg(svyranzr)
            cevag h"Pbairegrq: %f" % svyranzr
        rkprcg Rkprcgvba, r:
##            envfr   # KKK QROHT
            cevag h"Snvyrq gb pbaireg %f, ernfba: %f" % (svyranzr, fge(r))

vs __anzr__ == h"__znva__":
    znva()


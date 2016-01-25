#!/usr/bin/env python
# -*- coding: utf-8 -*-

import alertprocess
import conf as cf

from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm


doc = SimpleDocTemplate("form_letter.pdf",pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)

story = []

canvas.setLineWidth(.3)
canvas.setFont('Helvetica', 12)

canvas.drawString(30,750,'Report for sky alert from aLIGO')
canvas.drawString(30,735,'catalog for optical follow-up')
canvas.drawString(480,750, cf.obs_date)
canvas.line(480,747,580,747)

canvas.drawString(275,725,'Report for Observatory {}'.format(cf.obs_name))
canvas.line(275,723,400,723)

canvas.save()

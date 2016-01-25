#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import alertprocess
from . import conf as cf

from reportlab.pdfgen import canvas

canvas = canvas.Canvas('AlertReport.pdf', pagesize=cf.docsize)
width, height = cf.docsize



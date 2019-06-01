#!/usr/bin/python3
# Copyright (c) 2019 Bart Massey
# 
# Python reimplementation of http://www.nicholson.com/rhn/dsp.html#3
# BSD Licensed per author.
# Please see comment at end of file for original source and
# licensing information.

from math import pi, sin, cos

def resamp(x, indat, fmax, fsr, wnwdth):
    """
    QDSS Windowed-Sinc ReSampling

    x      = new sample point location (relative to old indexes)
             (e.g. every other integer for 0.5x decimation)
    indat  = original data array
    fmax   = low pass filter cutoff frequency
    fsr    = sample rate
    wnwdth = width of windowed Sinc used as the low pass filter

    Returns a filtered new sample point.
    """
    
    alim = len(indat)
    r_g = 2 * fmax / fsr   # Calc gain correction factor
    r_y = 0
    for i in range(-wnwdth//2, wnwdth//2-1):
        j = int(x + i)   # Calc input sample index
        # calculate von Hann Window. Scale and calculate Sinc
        r_w = 0.5 - 0.5 * cos(2 * pi * (0.5 + (j - x) / wnwdth))
        r_a = 2 * pi * (j - x) * fmax / fsr
        r_snc = 1
        if r_a != 0:
            r_snc = sin(r_a) / r_a
        if j >= 0 and j < alim:
            r_y   = r_y + r_g * r_w * r_snc * indat[j]
    return r_y

# rem - QDSS Windowed-Sinc ReSampling subroutine in Basic
# rem
# rem - This function can also be used for interpolation of FFT results
# rem
# rem function parameters
# rem : x      = new sample point location (relative to old indexes)
# rem            (e.g. every other integer for 0.5x decimation)
# rem : indat  = original data array
# rem : alim   = size of data array
# rem : fmax   = low pass filter cutoff frequency
# rem : fsr    = sample rate
# rem : wnwdth = width of windowed Sinc used as the low pass filter
# rem
# rem resamp() returns a filtered new sample point
# 
# sub resamp(x, indat, alim, fmax, fsr, wnwdth)
#   local i,j, r_g,r_w,r_a,r_snc,r_y	: rem some local variables
#   r_g = 2 * fmax / fsr           : rem Calc gain correction factor
#   r_y = 0
#   for i = -wnwdth/2 to (wnwdth/2)-1 : rem For 1 window width
#     j       = int(x + i)          : rem Calc input sample index
#         : rem calculate von Hann Window. Scale and calculate Sinc
#     r_w     = 0.5 - 0.5 * cos(2*pi*(0.5 + (j - x)/wnwdth))
#     r_a     = 2*pi*(j - x)*fmax/fsr
#     r_snc   = 1  : if (r_a <> 0) then r_snc = sin(r_a)/r_a
#     if (j >= 0) and (j < alim) then
#       r_y   = r_y + r_g * r_w * r_snc * indat(j)
#     endif
#   next i
#   resamp = r_y                  : rem Return new filtered sample
# end sub
# 
# rem  - Ron Nicholson's QDSS ReSampler cookbook recipe
# rem                 QDSS = Quick, Dirty, Simple and Short
# rem  Version 0.1b - 2007-Aug-01
# rem  Copyright 2007 Ronald H. Nicholson Jr.
# rem  No warranties implied.  Error checking, optimization, and
# rem    quality assessment of the "results" is left as an exercise
# rem    for the student.
# rem  (consider this code Open Source under a BSD style license)
# rem  IMHO. YMMV.  http://www.nicholson.com/rhn/dsp.html

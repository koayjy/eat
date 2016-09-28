"""EHT tables
"""

from pkg_resources import parse_version
import pandas as pd
if parse_version(pd.__version__) < parse_version('0.15.1dev'):
    print "pandas version too old and buggy, please update"
import datetime
import numpy as np
import os


# CNS Clock II GPS time interval log with chosen datetime format
CNS2LOG_FIELDS = (
    ('timestamp', str), # Time Stamp: selectable format
    ('tic', float), # Time interval reading from the Time Interval Counter
    ('gps_clock_err', float), # GPS receiver "sawtooth" clock error data
    ('gps_accuracy', float), # GPS receiver accuracy estimate
    ('pps_offset', float), # PPS offset
    ('tic_corrected', float), # corrected TIC data
    ('pc_vs_utc', float), # PC time error vs UTC
    ('utc_corr_s', float), # UTC correction factor (seconds part)
    ('utc_corr_ns', float), # UTC correction factor (nanosecs part)
)

cns2log_pandasargs = dict(
    header=None,
    dtype={'timestamp':float},
    # parse_dates={'datetime':[0]},
    # keep_date_col=True,
    # date_parser=lambda dates: [datetime.datetime.strptime(d[:6], '%y%j') +
    #   datetime.timedelta(days=float(d[-7:])) for d in dates],
    names=[a[0] for a in CNS2LOG_FIELDS]
)

# GPS II time log file
def read_cns2log(filename):
    table = pd.read_csv(filename, **cns2log_pandasargs)
    return table

# X21 USB accelerometer
X21_FIELDS = (
    ('seconds', float),
    ('xacc', int),
    ('yacc', int),
    ('zacc', int),
)

x21_pandasargs = dict(
    header = None,
    comment=';',
    names=[a[0] for a in X21_FIELDS]
)

def read_x21log(filename):
    table = pd.read_csv(filename, **x21_pandasargs)
    return table

# GISELA Calibrated 3mm output
G3MM_FIELDS = (
    ('number', int),
    ('uu', float),
    ('vv', float),
    ('ww', float),
    ('date', float),
    ('baseline', int),
    ('int_time', float),
    ('gate_id', int),
    ('source', int),
    ('v_real', float),
    ('v_imag', float),
    ('weight', float),
)

g3mm_pandasargs = dict(
    delim_whitespace=True,
    skiprows=2,
    header = None,
    index_col=False,
    names=[a[0] for a in G3MM_FIELDS]
)

def read_g3mm(filename):
    table = pd.read_csv(filename, **g3mm_pandasargs)
    return table.dropna()

# MICHAEL 3mm debiased closure amplitudes
M3MMCA_FIELDS = [('time', float),] + \
	[("site%d" % (i+1), int) for i in range(8)] + \
	[field for i in range(4) for field in (("u%d" % (i+1), float), ("v%d" % (i+1), float))] + [
	('camp', float),
	('camp_err', float),
]

m3mmca_pandasargs = dict(
    delim_whitespace=True,
    skiprows=0,
    header = None,
    index_col=False,
    names=[a[0] for a in M3MMCA_FIELDS]
)

def read_m3mmca(filename):
    table = pd.read_csv(filename, **m3mmca_pandasargs)
    return table.dropna()

# ANDRE's blist for closure phase
BLIST_FIELDS = [
    ('year', int),
    ('day', int),
    ('hour', float),
    ('source', str),
    ('triangle', str),
    ('cphase', float),
    ('cphase_err', float),
    ('u0', float),
    ('u1', float),
    ('u2', float),
    ('v0', float),
    ('v1', float),
    ('v2', float),
]

blist_pandasargs = dict(
    delim_whitespace=True,
    comment='#',
    skiprows=0,
    header=None,
    parse_dates={'datetime':[0,1,2]},
    # index_col='datetime',
    keep_date_col=True,
    # note: pandas 0.15.1 cannot use generator for date_parser (unlike 0.18), so changed to a list comprehension
    date_parser=lambda years,days,hours: [datetime.datetime.strptime(x+y, '%Y%j')
         + datetime.timedelta(hours=float(z)) for (x,y,z) in zip(years,days,hours)],
    names=[a[0] for a in BLIST_FIELDS]
)

def read_blist(filename):
    table = pd.read_csv(filename, **blist_pandasargs)
    # return table.dropna()
    return table
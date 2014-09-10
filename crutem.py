#!/usr/bin/env python3

"""
Convert crutem4 station listing files to GHCN-M v3 format
"""

import sys

def crutem1(inp, dat, inv):
    # dict() of metadata.
    d = {}
    while True:
        s = inp.readline().strip()
        if s == "Obs:":
            break
        k, v = s.split('=', 1)
        d[k] = v.strip()

    start_from = d.get('First Good Year', 0)
    id = "CRU42" + d['Number']
    assert 11 == len(id)
    for s in inp:
        field = s.split()
        year = int(field[0])
        if year < start_from:
            continue
        ms = [float(x) for x in field[1:13]]
        ms = [convert1(v) for v in ms]
        if ms == [-9999] * 12:
            continue
        data = ["{:5.0f}   ".format(v) for v in ms]
        data = ''.join(data)
        dat.write("{}{}TAVG{}\n".format(id, year, data))
    lat = float(d['Lat'])
    lon = float(d['Long'])
    elev = float(d['Height'])
    name = d['Name']
    inv.write("{} {:8.4f} {:9.4f} {:6.1f} {:30.30s}\n".format(
      id, lat, lon, elev, name))

def convert1(s):
    """
    Convert single datum (as string) to float (scaled so that
    units are 0.01C). A crutem invalid value of -99.0 is
    converted to a GHCN-M invalid value of -9999.
    """

    x = float(s)
    if x == -99:
       return -9999
    return x*100

def crutem(dat, inv):
    import glob

    for station_file in glob.glob("CRUTEM.4.*.station_files/*/*"):
        with open(station_file, encoding="iso8859-1") as inp:
            try:
                crutem1(inp, dat, inv)
            except Exception as e:
                sys.stderr.write("{}\n".format(station_file))
                sys.stderr.write("{}\n".format(str(e)))
        

def main(argv=None):
    if argv is None:
        argv = sys.argv

    with open("crutem4.dat", 'w') as dat,\
      open("crutem4.inv", 'w') as inv:
        crutem(dat, inv)

if __name__ == '__main__':
    main()

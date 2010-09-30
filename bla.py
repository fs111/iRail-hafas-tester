#!/usr/bin/env python

import httplib
import urllib
from xml.dom import minidom
import sys

BASE_URL =  "http://hari.b-rail.be/Hafas/bin/extxml.exe"

FIRST = """<?xml version="1.0" encoding="iso-8859-1"?>
<ReqC ver="1.1" prod="iRail" lang="EN">
<LocValReq id="FROM" maxNr="1">
<ReqLoc match="%s" type="ST"/>
</LocValReq>
<LocValReq id="TO" maxNr="1">
<ReqLoc match="%s" type="ST"/>
</LocValReq>
</ReqC>"""

SECOND = """<?xml version="1.0" encoding="iso-8859-1"?>
<ReqC ver="1.1" prod="iRail" lang="EN">
<ConReq>
<Start min="10">
<Station externalId="%s" distance="0">
</Station>
<Prod prod="1111111111111111">
</Prod>
</Start>
<Dest min="10">
<Station externalId="%s" distance="0">
</Station>
</Dest>
<Via>
</Via>
<ReqT time="16:10" date="20100929" a="0">
</ReqT>
<RFlags b="0" f="6">
</RFlags>
<GISParameters>
<Front>
</Front>
<Back>
</Back>
</GISParameters>
</ConReq>
</ReqC>
"""



def make_request(xmlstring):
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection("hari.b-rail.be:80")
    conn.request("POST", "/Hafas/bin/extxml.exe", xmlstring, headers)
    response = conn.getresponse()
    return response.read()


def main():
    from_station_name = sys.argv[1]
    to_station_name = sys.argv[2]
    body = FIRST % (from_station_name, to_station_name)
    data = make_request(body)
    doc = minidom.parseString(data)

    to_station_id, from_station_id = -1, -1
    lvrs = doc.getElementsByTagName("LocValRes")
    for lvr in lvrs:
        st = lvr.getElementsByTagName("Station")[0]
        ext = st.getAttribute("externalId")
        print ext
        st_type = lvr.getAttribute("id")
        if st_type == "TO":
            to_station_id = ext
        else:
            from_station_id = ext
    from_station_id, to_station_id
    body = SECOND % (from_station_id, to_station_id)

    data = make_request(body)
    print data


if __name__ == "__main__":
    main()

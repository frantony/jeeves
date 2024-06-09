#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

import os

from rdflib import Graph, Literal, Namespace, XSD

from collections import OrderedDict
from tabulate import tabulate


ttlfile = "jeeves.ttl"

g = Graph()
ttlfile = os.path.abspath(ttlfile)
g.parse(ttlfile, format="ttl")

query = """
PREFIX uuid: <uuid:///>
PREFIX  scm: <terminusdb:///schema#>
PREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?uuid ?name ?gitblob
WHERE {
    ?file scm:name "computer file" .
    ?uuid scm:is-a+ ?file .
    ?uuid scm:name ?name .
    ?uuid scm:git-blob ?gitblob .
}
"""

t = []
for s in g.query(query):
    name = str(s["name"])
    if len(name) > 40:
        name = name[:37] + "..."
    t.append(
        OrderedDict([
            ('name', name),
            ('uuid', str(s["uuid"]).replace("urn:uuid:", "")),
            ('git-blob', s["gitblob"]),
        ])
    )

#def user_filter(x):
#    name = x["name"]
#    return "red" in name
#
#t = filter(user_filter, t)

def user_sort(x):
    n = x["name"]
    u = x["uuid"]

    return (n, u)

t = sorted(t, key=user_sort)

print(tabulate(t, headers="keys", tablefmt="simple", numalign="right"))

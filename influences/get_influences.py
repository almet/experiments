from collections import defaultdict
import time
import sys

import rdflib
from rdflib import plugin

# To be able to parse SPARQL
plugin.register('sparql', rdflib.query.Processor,
                'rdfextras.sparql.processor', 'Processor')
plugin.register('sparql', rdflib.query.Result,
                'rdfextras.sparql.query', 'SPARQLQueryResult')

# List of parsed information
LANGUAGES_INFO = {}
LANGUAGES_OBJECTS = {'asc': {}, 'desc': {}}

class Lang(object):
    def __init__(self, name):
        self.name = name
        self.influenced = []
        self.influenced_by = []
    
    @property
    def name_(self):
        return self.name.replace("+", "p").replace("-", "m").replace("#", "sharp")\
                .replace("/", "").replace(" ", "")

    def __repr__(self):
        return "<Lang %s>" % self.name

    def as_dot(self):
        """Return a dot representation from this node"""
        return "digraph %s {\n%s\n }" % (self.name, self._dotgraph())

    def _dotgraph(self, parsed=None):
        if parsed is None:
            parsed = {'inf': {}, 'infBy': {}}

        string = ""
        for elem in self.influenced:
            string = string + "%s -> %s;\n" % (self.name, elem.name_)
            if not elem.name in parsed['inf']:
                parsed['inf'][elem.name] = elem
                string = string + elem._dotgraph(parsed)

        for elem in self.influenced_by:
            string = string + "%s -> %s;\n" % (elem.name_, self.name_)
            if not elem.name in parsed['infBy']:
                parsed['infBy'][elem.name] = elem
                string = string + elem._dotgraph(parsed)

        return string 


def get_related(language):
    """Uses the dbpedia rdf triples to get the languages influenced and that
    influenced this one.

    Consider that names on wikipedia (and thus on dbpedia) are always capitalized, 
    and that when they don't have a page on their own, it is suffixed by something
    """

    def _run_query_on(language, loop=True):
        g = rdflib.Graph().parse("http://dbpedia.org/data/%s.rdf" % language)
        result = g.query("""SELECT ?influenced ?influencedBy WHERE {
                           ?lang dbp:influencedBy ?influencedBy . 
                           ?lang dbp:influenced ?influenced
                       }""", initNs=dict(dbp="http://dbpedia.org/property/")).result
        if loop and not result:
            result = _run_query_on(language + "_%28programming_language%29", False)
        return result

    def _query_dbpedia(language):
        language = language.capitalize() # wikipedia names are capitalized
        result, influenced, influenced_by = None, None, None

        try:
            result = _run_query_on(language)
        except: # sometimes dbpedia issue a 500 for unknown reasons, wait a bit
            time.sleep(1)
            try:
                result = _run_query_on(language)
            except:
                pass

        if result:
            influenced = result[0][0].split(", ")
            influenced_by = result[0][1].split(", ")

        return (influenced or [], influenced_by or [])
    
    # Don't issue the same request twice
    if language not in LANGUAGES_INFO:
        LANGUAGES_INFO[language] = _query_dbpedia(language)
    return LANGUAGES_INFO[language]

def get_tree(name, direction="both"):
    """Build the tree given a language name and a direction.

    :name: the language name to look for
    :oder: parsing desc or asc? (or both)
    """

    # do not parse the same thing twice
    if direction != "both":
        if name in LANGUAGES_OBJECTS[direction]:
            return LANGUAGES_OBJECTS[direction][name]

    elem = Lang(name)
    inf, inf_by = get_related(name)
    
    if direction == "desc" or direction == "both":
        LANGUAGES_OBJECTS["desc"][name] = elem
        elem.influenced = [get_tree(lang, "desc") for lang in inf]

    if direction == "asc" or direction == "both":
        LANGUAGES_OBJECTS["asc"][name] = elem
        elem.influenced_by = [get_tree(lang, "asc") for lang in inf_by]

    return elem

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "error: please specify a language to search for"
    elif (len(sys.argv) == 2):
        # passing only a lang will print a scheme for it
        print get_tree(sys.argv[1]).as_text()
    elif (len(sys.argv) == 3) and sys.argv[2] == "dot":
        # return a dot string
        print get_tree(sys.argv[1]).as_dot()

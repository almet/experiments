import rdflib
from rdflib import plugin

# To be able to parse SPARQL
plugin.register('sparql', rdflib.query.Processor,
                'rdfextras.sparql.processor', 'Processor')
plugin.register('sparql', rdflib.query.Result,
                'rdfextras.sparql.query', 'SPARQLQueryResult')

class Lang(object):
    def __init__(self, name):
        self.name = name
        self.influenced = []
        self.influenced_by = []
    
    def __repr__(self, level=1):
        def _print(char, elem):
            return "\n" + " " * level + char + " %s" % elem.__repr__(level + 1)

        repr = self.name
        for elem in self.influenced:
            repr = repr + _print(">", elem)
        for elem in self.influenced_by:
            repr = repr + _print("<", elem)
        return repr


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

    language = language.capitalize() # wikipedia names are capitalized
    influenced, influenced_by = None, None
    result = _run_query_on(language)

    if result:
        influenced = result[0][0].split(", ")
        influenced_by = result[0][0].split(", ")

    return (influenced or [], influenced_by or [])


def get_tree(name, desc=None, asc=None):
    """Build the tree given a language name and a direction.

    :name:
        the language name to look for

    :desc:
        Try to find the languages that have been influenced by this one (descending
        order)

    :asc:
        Try to find the languages that have influenced this one (ascending order)
    """

    # We are the root element if neither desc and asc are set
    is_root = desc is None and asc is None

    elem = Lang(name)
    inf, inf_by = get_related(name)

    if desc or is_root:
        elem.influenced = [get_tree(lang, desc=True) for lang in inf]

    if asc or is_root:
        elem.influenced_by = [get_tree(lang, asc=True) for lang in inf_by]

    return elem

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "error: please specify a language to search for"
    else:
        print get_tree(sys.argv[1])

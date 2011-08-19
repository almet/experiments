Various experiments
###################

This repository contains various experiments I've done and I wanted to share
with others.

Playing with SPARQL and DBPedia
===============================

I wanted to play a bit with DBPedia and the information about languages. It is
possible to get information about the languages that were influenced by a given
one, and the ones that influenced this language. The `influences/get_influences.py`
script generates a tree of those languages and can output a nice graph for you.

To generate the graph::

    $ python influences/get_influences.py python dot | dot -Tpng > influences.png

Which generates the following picture:

.. image:: http://files.lolnet.org/alexis/influences.png

Playing with nginx logfiles
===========================

I was wondering what the traffic on the different websites I have was, and thus
made a little script to extract informaton from nginx logs.

You can find it on `nginxgraph.py`. To use it::

    $ python nginxgraph.py nginx-access.log other-logfile.log

And it will generate some nice stuff for you:

.. image:: http://files.lolnet.org/alexis/nginxlog.png

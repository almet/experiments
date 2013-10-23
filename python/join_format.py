import time
import sys

def join(nb):
    for i in xrange(nb):
        youpi = '-'.join(('one', 'two'))


def format(nb):
    for i in xrange(nb):
        youpi = '{}-{}'.format('one', 'two')

if __name__ == '__main__':
    nb = int(sys.argv[1]) if (len(sys.argv) >= 2) else 10000
    print "doing the iteration %s times" % nb

    t1 = time.time()
    join(nb)
    t2 = time.time()
    format(nb)
    t3 = time.time()

    print 'join = %s' % (t2 - t1)
    print 'format = %s' % (t3 - t2)

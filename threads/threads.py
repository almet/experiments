from threading import Thread
from functools import partial
import sys


def job(msg):
    while True:


# generate the threads
def run_threads(nb_threads):
    for idx in range(nb_threads):
        t = Thread(target=partial(job, idx))
        t.start()

def run_processes(nb_processes):
    

if __name__ == '__main__':
    if len(sys.argv < 3):
        raise ValueError("signature is %s threads|processes nb" % sys.argv[0])
    elif sys.argv[1] == "threads":
        run_threads(int(sys.argv[2]))
    elif sys.argv[1] == "processes":
        run_processes(int(sys.argv[2]))

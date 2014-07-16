import subprocess, sys

db, max, hops = sys.argv[1:4]
subprocess.call('python util/tests.%s.py %s %s' % (db, max, hops), shell=True)
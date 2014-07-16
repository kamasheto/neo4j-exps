import subprocess, sys

db, pickle = sys.argv[1:3]
subprocess.call('python util/import.%s.py data/pickle.%s' % (db, pickle), shell=True)

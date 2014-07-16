import sys
sys.path.append('lib/neo4j/')

import cPickle, neo4jrest,simplejson, sys,time, random

# if len(sys.argv) < 4:
#     print 'usage:%s number_of_persons number_of_hops repetitions' % sys.argv[0]
#     sys.exit()

# namerange,pathlength,repeats = sys.argv[1:4]
namerange, pathlength, repeats = sys.argv[1], sys.argv[2], 10

namerange = int(namerange)
pathlength=int(pathlength)
repeats = int(repeats)
# "match  p=n:node<-[*4..4]-m where n.noscenda_name='dbpedia:Berlin' return count(p);"

g = neo4jrest.Neo4jRestConnector(debug=0)
#g.debug=1
times = []
printed = False
for i in range(0,repeats):
    target = 'person%s' % random.randint(1,namerange+1)
    hops ='-[:friend]->()' * (pathlength-1)
    query = "START person=node:node_auto_index(noscenda_name='%s') MATCH (person)%s-[:friend]->(friend) return count(friend);" % (target, hops)
    if not printed:
        printed = True
        print query
    print 'run %s: %s' % (i, target)
    start = time.time()
    result = g.cypher(query,dict(target=target))
    tt = time.time()-start
    times.append(tt)
    # print 'starting at',target,'found rels: ', 
    # print result
    # print result['data'][0][0]
    print "Time: ", tt
    print "---------"
avg = sum(times)/len(times)
print
print 'Average: ',avg

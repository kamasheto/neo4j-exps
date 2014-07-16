import MySQLdb
import cPickle, time, uuid, sys,random

# if len(sys.argv) < 4:
    # print 'usage:%s number_of_persons number_of_hops repetitions' % sys.argv[0]
    # sys.exit()

# namerange,pathlength,repeats = sys.argv[1:4]
namerange, pathlength, repeats = sys.argv[1], sys.argv[2], 10
namerange = int(namerange)
pathlength=int(pathlength)
repeats = int(repeats)


db = MySQLdb.connect("localhost","friends","","friends" )
# "match  p=n:node<-[*4..4]-m where n.noscenda_name='dbpedia:Berlin' return count(p);"

def make_sql(l,target):
    if l<1:
        raise 'len too small'
    start = """
    select 
        count(*)"""
    froms = """
    from
        t_user,
        t_user_friend as uf1"""

    wheres = """
    where
        t_user.name='%s' and 
        t_user.id = uf1.user_1""" % target
    i = 1
    if l>1:
        for i in range(2,l+1):
            froms+=', \n\tt_user_friend as uf%s' % i
            wheres+=' and\n\tuf%s.user_2 = uf%s.user_1' % (i-1,i)
    #froms+=""",
    #    t_user as final"""
    #wheres+=""" and
    #    uf%s.user_2=final.id""" % i
    return start+froms+wheres+';'


times = []
printed = False
for i in range(0,repeats):
    target = 'person%s' % random.randint(1,namerange+1)
    c = db.cursor()
    sql = make_sql(pathlength,target)
    # print ' '.join(sql.split())
    if not printed:
        printed = True
        print sql
    print 'run %s: %s' % (i, target)
    # print
    start = time.time()
    c.execute(sql)
    # print type(res)
    tt =  time.time()-start
    times.append(tt)
    print "Time: ", tt
    print "-----"
    # rows = c.fetchall()
    # print(rows)
    # print 'Num of paths: ',len(rows)
    # for row in rows:
        #print str(row).decode('utf-8')
        # pass
avg = sum(times)/len(times)
print 
print 'Average time: ', avg        

tasks = [{'id':'p1','arrival':0,'time':7},{'id':'p2','arrival':1,'time':4},{'id':'p3','arrival':2,'time':15},
{'id':'p4','arrival':3,'time':11},{'id':'p5','arrival':4,'time':20},{'id':'p6','arrival':4,'time':9}]
initial_time={}
for x in tasks:
    initial_time[x['id']]=x['time']
wt={}
qt=5
q=[]
t=0
last_processed = {'id':'','arrival':0,'time':0}
while len(tasks)>0 or len(q)>0 or last_processed['time']>0:
    while True and len(tasks)>0:
        if(tasks[0]['arrival']<=t):
            q.append(tasks.pop(0))
        else:
            break
    if(last_processed['time']>0):
        q.append(last_processed)
    elif last_processed['id']!='':
        wt[last_processed['id']]=t-(last_processed['arrival']+initial_time[last_processed['id']])
    time_passed = min(qt,q[0]['time'])
    q[0]['time']-=time_passed
    t+=time_passed
    last_processed = q.pop(0)

wt[last_processed['id']]=t-(last_processed['arrival']+initial_time[last_processed['id']])
print(last_processed)
print(wt)

#https://www.javatpoint.com/os-round-robin-scheduling-algorithm
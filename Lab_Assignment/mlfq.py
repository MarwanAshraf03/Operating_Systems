
class P:
    def __init__(self,id,arrival,execution,priority):
        self.id = id
        self.arrival= arrival
        self.priority = priority
        # we keep the two variables for execution time, one to decrement and one to keep the original value to calculate waiting time
        self.execution = execution
        self.execution_time = execution
        self.waiting_time = 0
    def __str__(self):
        return f'pid:{self.id} -- arrival time:{self.arrival} -- execution time:{self.execution} -- priority:{self.priority}'

# Round Robin
def rr(q):
    # quantum time
    qt=3
    # pop the first process in the queue
    process = q.pop(0)
    print(f't={time} --> {process.id} is executing')
    # we will enrcement time either with the quantum time or the process execution time left if it's shorter
    time_taken = min(qt,process.execution)
    process.execution-= time_taken
    if(process.execution==0):
        print(f'{process.id} finished executing at time {time+time_taken}')
        process.waiting_time = time+time_taken-process.arrival-process.execution_time
    else:
        q.append(process)
    return (q,process,time_taken)

def srt(q):
    qt = 2
    # index of shortes process until we find something shorter
    process = 0
    # locating the shortest process
    for x in range(len(q)):
        if(q[x].execution<q[process].execution):
            process=x
    process = q.pop(process)
    print(f't={time} --> {process.id} is executing')
    time_taken = min(qt,process.execution)
    process.execution-= time_taken
    if(process.execution==0):
        print(f'{process.id} finished executing at time {time+time_taken}')
        process.waiting_time = time+time_taken-process.arrival-process.execution_time
    else:
        q.append(process)
    return (q,process,time_taken)

def sjn(q):
    process = 0;
    for x in range(len(q)):
        if(q[x].execution<q[process].execution):
            process=x
    process = q.pop(process)
    print(f't={time} --> {process.id} is executing')
    time_taken = process.execution
    process.execution-= time_taken
    print(f'{process.id} finished executing at time {time+time_taken}')
    process.waiting_time = time+time_taken-process.arrival-process.execution_time
    return (q,process,time_taken)

# deciding which queue we're in to choose the appropriate algorithm
def execute(q,priority):
    if priority == 0:
        q,p,t= rr(q)
        return (q,p,t)
    if priority == 1:
        q,p,t= srt(q)
        return (q,p,t)
    if priority == 2:
        q,p,t= sjn(q)
        return (q,p,t)

# processes = [P('p0',0,10,0),P('p1',0,2,1),P('p2',0,4,0),P('p3',4,8,2),P('p4',5,10,1),P('p5',7,7,2)]
processes = [P('p0',0,5,1),P('p1',1,8,0),P('p2',3,6,2),P('p3',5,4,2),P('p4',8,2,1),P('p5',16,10,0)]
mlfq = [[],[],[]]

# c is a counter to how many process arrived so we don't duplicate them in the queue
c = 0
time = 0
while c<len(processes) or (len(mlfq[0]) != 0 or len(mlfq[1])!=0 or len(mlfq[2])!=0):
    # allocating the processes that arrived
    for x in range(c,len(processes)):
        p = processes[x]
        if(p.arrival<=time):
            mlfq[p.priority].append(p)
            c+=1
    # executing the process when it's its turn
    for q in range(len(mlfq)):
        if len(mlfq[q]) != 0:
            mlfq[q],process,t = execute(mlfq[q],q)
            break
    time+=t
print()
print('waiting time:')
avg=0
for x in processes:
    print(f'w{x.id} = {x.waiting_time}')
    avg+=x.waiting_time
print(f'average waiting time = {avg}/{len(processes)} = {avg/len(processes)}')
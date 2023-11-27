from tkinter import *
class P:
    allocated_number=0
    def __init__(self,id,arrival,execution,priority):
        self.id = id
        self.arrival= arrival
        self.priority = priority
        # we keep the two variables for execution time, one to decrement and one to keep the original value to calculate waiting time
        self.execution = execution
        self.execution_time = execution
        self.waiting_time = 0
        # the next variable to make sure we don't add a process in the queues more than once by setting it to true when the process gets allocated
        self.allocated=False
    def __str__(self):
        return f'pid:{self.id} -- arrival time:{self.arrival} -- execution time:{self.execution} -- priority:{self.priority}'

# Round Robin
def rr(q):
    # quantum time
    qt=3
    print(f't={time} --> {q[0].id} is executing')
    displayMLFQ(mlfq,time,q[0])
    # pop the first process in the queue
    process = q.pop(0)
    # we will enrcement time either with the quantum time or the process execution time left if it's shorter
    time_taken = min(qt,process.execution)
    chart.append((process.id,time))
    process.execution-= time_taken

    if(process.execution==0):
        print(f'{process.id} finished executing at time {time+time_taken}')
        process.waiting_time = time+time_taken-process.arrival-process.execution_time
    else:
        q.append(process)
    return (q,process,time_taken)

def srt(q):
    qt = 2
    # index of shortest process until we find something shorter
    process = 0
    # locating the shortest process
    for x in range(len(q)):
        if(q[x].execution<q[process].execution):
            process=x
    print(f't={time} --> {q[process].id} is executing')

    displayMLFQ(mlfq,time,q[process])
    process = q.pop(process)
    time_taken = min(qt,process.execution)
    chart.append((process.id,time))
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

    print(f't={time} --> {q[process].id} is executing')
    displayMLFQ(mlfq,time,q[process])
    process = q.pop(process)
    time_taken = process.execution
    chart.append((process.id,time))
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

def displayMLFQ(mlfq,time,process):
    tk = Tk()
    c = Canvas(tk,width=500,height=500,scrollregion=(0,0,P.allocated_number*30 + 10,P.allocated_number*30 + 10))
    c.configure(bg='white')
    scrollbar = Scrollbar(tk, orient="horizontal", command=c.xview)
    c.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="bottom", fill="x")
    c.pack()
    c.create_text(50,30,text=f"At time = {time}")
    c.create_text(30,100,text='priority 0')
    c.create_text(30,200,text='priority 1')
    c.create_text(30,300,text='priority 2')
    for q in range(len(mlfq)):
        for p in range(len(mlfq[q])):
            # vertical lines
            # x1 = p * 30 + 10 --> starts before the process with 30 pixels difference between each line and displace them with 10 pixels so it doesn't stick to the borders
            # y1 = (q + 1) * 100 + 30 --> start after the beginnig of the queue with 30 pixels
            # x2 = x1 --> because it's a vertical line
            # y2 = y1+30 --> give the line 30 pixels height
            c.create_line(p*30+10,(q+1)*100+30,p*30+10,(q+1)*100+60)
            if mlfq[q][p].id==process.id:
                # process name
                # x = vertical line before the process + 15 --> displace the process name by 15 pixels from the vertical line before it
                # y = start of the queue + 15 --> same idea in x
                # color the process that will enter the cpu in red
                c.create_text(p*30+25,(q+1)*100+45,text=mlfq[q][p].id,fill='red')
            else:
                c.create_text(p*30+25,(q+1)*100+45,text=mlfq[q][p].id)
            if(p==len(mlfq[q])-1):
                # since the last process is missing the vertical line on the right we add this line
                c.create_line((p+1)*30+10,(q+1)*100+30,(p+1)*30+10,(q+1)*100+60)
                # 2 horizontal lines
                # x1 = 10 --> the horizontal start of the first vertical line which is at 0 with 10 pixels displacement
                # y1 --> the vertical start of all vertical lines
                # x2 = --> the horizontal start of the last vertical line
                # y2 --> same as y1 since it's a horizontal line
                c.create_line(10,(q+1)*100+30,(p+1)*30+10,(q+1)*100+30)
                # the second horizontal line is the same as the first one but positioned at the bottom of the vertical lines
                c.create_line(10,(q+1)*100+60,(p+1)*30+10,(q+1)*100+60)
    c.create_text(150,400,text='*Process colored in red is the one that entered the cpu',fill='red')
    mainloop()

def checkID():
    while True:
        Id = input('process name: ')
        if Id not in namespace:
            namespace.append(Id)
            return Id
        else:
            print('process ID is duplicated')

def checkTime(time):
    while True:
        try:
            t = int(input(f"{time} time: "))
            if t >= 0:
                return t
            else:
                print("Time can't be a negative number")
        except ValueError:
            print("Please enter a valid integer for time.")

def checkPriority():
    while True:
        try:
            p = int(input('Priority: '))
            if 0 <= p <= 2:
                return p
            else:
                print('Priority must be between 0 and 2 (both ends included)')
        except ValueError:
            print("Please enter a valid integer for priority.")
            
def getNumberOfProcesses():
    while True:
        try:
            num_processes = int(input('Enter number of processes: '))
            if num_processes > 0:
                return num_processes
            else:
                print('Number of processes must be greater than zero.')
        except ValueError:
            print('Please enter a valid integer for the number of processes.')
            
# processes = [P('p0',0,10,0),P('p1',0,2,1),P('p2',0,4,0),P('p3',4,8,2),P('p4',5,10,1),P('p5',7,7,2)]
# processes = [P('p0',0,5,1),P('p1',1,8,0),P('p2',3,6,2),P('p3',5,4,2),P('p4',8,2,1),P('p5',16,10,0)]
processes = []
namespace = []

number_of_processes = getNumberOfProcesses()

for x in range(number_of_processes):
    Id = checkID()
    arrival = checkTime('Arrival')
    execution = checkTime('Execution')
    priority = checkPriority()
    processes.append(P(Id,arrival,execution,priority))

mlfq = [[],[],[]]
chart=[]

time = 0
while P.allocated_number<len(processes) or (len(mlfq[0]) != 0 or len(mlfq[1])!=0 or len(mlfq[2])!=0):
    # allocating the processes that arrived
    for x in range(len(processes)):
        p = processes[x]
        if(p.arrival<=time and p.allocated==False):
            mlfq[p.priority].append(p)
            print(f"At time {time} {p.id} arrived")
            p.allocated=True
            P.allocated_number+=1
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

tk = Tk()
c = Canvas(tk,height=500,width=1500,scrollregion=(0,0,time*40+20,time*40+20))
c.configure(bg='white')
scrollbar = Scrollbar(tk, orient="horizontal", command=c.xview)
c.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side="bottom", fill="x")
c.pack()
for p in range(len(chart)):
    # vertical lines:
    # x1 = the start time of each execution and give the 1 unit time a width of 40 pixels and displace them all with 10 pixels
    # y1 = the vertical start of the line
    # x2 = x1 --> a vertical line
    # y2 -->  this gives the lines a height of 60 pixels
    c.create_line(chart[p][1]*40+10,220,(chart[p][1]*40)+10,280)
    # time index
    # x = the exact position of the vertical line
    # y = after the end of the vertical line which is 280 by 10 pixels
    c.create_text(chart[p][1]*40+10,290,text=chart[p][1])
    if p!=len(chart)-1:
        # process name
        # x --> the same position of the vertical line but we add half the distance between the start line and the end line to place the process name in the middle
        c.create_text(chart[p][1]*40+10+(chart[p+1][1]-chart[p][1])*20,252,text=chart[p][0])
    else:
        # the same thing as the past line but the end here is the end time and not the next process's start because this was the last process
        c.create_text(chart[p][1]*40+10+(time-chart[p][1])*20,252,text=chart[p][0])

# creating the last vertical line which lies at the end time and giving it its time index
c.create_line(time*40+10,220,time*40+10,280)
c.create_text(time*40+10,290,text=time)
# the horizontal lines
c.create_line(10,220,time*40+10,220)
c.create_line(10,280,time*40+10,280)
c.mainloop()

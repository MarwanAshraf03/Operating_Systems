package rr;
import java.util.LinkedList;
import java.util.Queue;
public class Rr {
    
    public static void main(String[] args) {
        // pre-defining our process that will enter the queues to be able to monitor them
       process[] tasks = {new process("p1",0,7),new process("p2",1,4),new process("p3",2,15),
       new process("p4",3,11),new process("p5",4,20),new process("p6",4,9)};
       // counter for how many tasks arrived already
       int added = 0;
       
       // the time quantum for each queue
       int[] qt = {4,8,16};
       // counter to keep track of the current time
       int t = 0;
       
       // the multi queues
       Queue[]q = {new LinkedList<>(),new LinkedList<>(),new LinkedList<>()};
       
       // we will keep processing untill no new tasks arrive and all queues are emtpy
       while(added!=tasks.length | q[0].size()!=0 | q[1].size()!=0 | q[2].size()!=0){
           // check which tasks have arrived and add them in the first queue
           for(int i = added; i < tasks.length; i++){
               if(tasks[i].arrival_time<=t){
                   q[0].add(tasks[i]);
                   added++;
               }
           }
           System.out.println("at time = "+t);
           System.out.println(q[0]);
           System.out.println(q[1]);
           System.out.println(q[2]);
           
           // looping each queue to process the first task in the highest priority one
           for(int i = 0 ; i < q.length ; i++){
               if(q[i].size()>0){
                   // either increasing the time with a time quantum or if the task takes less time we increase it by its time left
                   process p = (process) q[i].element();
                   System.out.println("Task being processed: "+p.id);
                   int time_passed=Math.min(qt[i], p.time_left);
                   t+=time_passed;
                   p.time_left-=time_passed;
                   // if the task finished remove it otherwise add it to the next priority queue
                   if(p.time_left!=0){
                       q[Math.min(q.length-1, i+1)].add(q[i].remove());
                   }else{
                       p.out_time=t;
                       q[i].remove();
                   }
                   break;
               }
           }
           System.out.println("----------------------------");
       }
           System.out.println("at time = "+t);
           System.out.println(q[0]);
           System.out.println(q[1]);
           System.out.println(q[2]);
           
           System.out.println("------waiting times-------");
           int total = 0;
           for(int i = 0 ; i < tasks.length ; i++){
               int wt = tasks[i].waitingTime();
               total+=wt;
               System.out.println(tasks[i].id + ": " + wt);
           }
           System.out.println("average waiting time: "+total/tasks.length);
    }
}

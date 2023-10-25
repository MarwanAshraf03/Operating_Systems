package rr;
public class process {
    String id;
    int arrival_time;
    int execution_time;
    int time_left;
    int out_time;
    
    public process(String id, int arrival_time, int execution_time) {
        this.id = id;
        this.arrival_time = arrival_time;
        this.execution_time = execution_time;
        this.time_left=execution_time;
    }
    public process(){
        
    }
    
    public String toString(){
    return this.id + " - time left: " + this.time_left;  
    }
    
    public int waitingTime(){
        return this.out_time - this.arrival_time - this.execution_time;
    }
}

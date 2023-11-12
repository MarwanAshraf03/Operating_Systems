package AssignmentOS;
public class process {
    String id;
    int arrival_time;
    // The reason we have execution time and time left is we want something fixed to be able to calculate waiting time at the end and we need something that will change when we work on our process
    int execution_time;
    int time_left;
    // The time the process got finished to calculate waiting time
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
        //To calculate waiting time we see when did the task finished, when did it arrive, how much of this time it was running (the remaining time means it was waiting)
        return this.out_time - this.arrival_time - this.execution_time;
    }
}

package memory_management;
import java.util.ArrayList;
import java.lang.Integer;

/**
 * pid: an integer representing the process id
 * arrival_time: the time that process has has entered the ready
 *  queue
 * burst_time: the time that process needs to complete its task
 * size_needed: the number of bytes that the process needs to
 *  perform its tasks
 * data: this represents the data that the process needs like:
 *  stack, heap, etc
 * childs: a list of pids of process childs
 * parent: an integer represents the parent of the process
 */

public class process {
    private int pid = -1;
    private int arrival_time = -1;
    private int burst_time = -1;
    private double size_needed = -1;
    private ArrayList<Object> data;
    private ArrayList<Integer> childs = new ArrayList<Integer>();
    private int parent = -1;
    public process(int pid)
    {
        this.pid = pid;
    }
    public int pid_getter(){
        return this.pid;
    }
    public void pid_setter(int pid){
        this.pid = pid;
    }
    public int arrival_time_getter(){
        return this.arrival_time;
    }
    public void arrival_time_setter(int arrival_time){
        this.arrival_time = arrival_time;
    }
    public int burst_time_getter(){
        return this.burst_time;
    }
    public void burst_time_setter(int burst_time){
        this.burst_time = burst_time;
    }
    public double size_needed_getter(){
        return this.size_needed;
    }
    public void size_needed_setter(double size_needed){
        this.size_needed = size_needed;
    }
    public ArrayList<Object> data_getter(){
        return this.data;
    }
    public void data_setter(ArrayList<Object> data){
        this.data = data;
    }
    public ArrayList<Integer> childs_getter(){
        return this.childs;
    }
    public void childs_setter(ArrayList<Integer> childs){
        this.childs = childs;
    }
    public int parent_getter(){
        return this.parent;
    }
    public void parent_setter(int parent){
        this.parent = parent;
    }
}
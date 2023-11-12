package memory_management;
public class process {
    private int pid = 0;
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
}
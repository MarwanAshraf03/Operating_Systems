package memory_management2;

class Process {
    private int pid;
    private int arrivalTime;
    private int burstTime;
    private double sizeNeeded;

    public Process(int pid, int arrivalTime, int burstTime, double sizeNeeded) {
        this.pid = pid;
        this.arrivalTime = arrivalTime;
        this.burstTime = burstTime;
        this.sizeNeeded = sizeNeeded;
    }

    public int getPid() {
        return pid;
    }

    public int getArrivalTime() {
        return arrivalTime;
    }

    public int getBurstTime() {
        return burstTime;
    }

    public double getSizeNeeded() {
        return sizeNeeded;
    }

    public void decrementBurstTime() {
        burstTime--;
    }
}

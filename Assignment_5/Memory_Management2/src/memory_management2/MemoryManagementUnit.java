package memory_management2;
import java.util.LinkedList;
import java.util.Queue;
import java.util.ArrayList;


class MemoryManagementUnit {
    private double virtualMemorySize;
    private double diskSize;
    private double backStoreSize;
    private double RAMSize;
    private double pageSize;
    private double osSize;
    private int numberOfPages;
    // private Queue<Page> pageTable;
    private ArrayList<Page> pageTable;
    private LinkedList<Page> frames;

    public MemoryManagementUnit(double virtualMemorySize, double diskSize, double backStoreSize,
                                ArrayList<Page> pageTabledouble,double RAMSize, double pageSize, double osSize, int numberOfPages) {
        this.virtualMemorySize = virtualMemorySize;
        this.diskSize = diskSize;
        this.backStoreSize = backStoreSize;
        this.RAMSize = RAMSize;
        this.pageSize = pageSize;
        this.osSize = osSize;
        this.numberOfPages = numberOfPages;
        // this.pageTable = new LinkedList<>();
        this.pageTable = pageTable;
        this.frames = new LinkedList<>();
    }

    public void executeProcess(Process process) {
        System.out.println("\nExecuting Process " + process.getPid() + " with Size " + process.getSizeNeeded() + " KB With Burst time of " + process.getBurstTime());

        int requiredPages = (int) Math.ceil(process.getSizeNeeded() / pageSize);

        // if (requiredPages > numberOfPages) {
        //     System.out.println("Process " + process.getPid() + " requires more pages than available. Skipping.");
        //     return;
        // }

        int counter = 0;
        while (true) {
            if (pageTable.get(counter).getOccupiedBy() == -1) {
                pageTable.get(counter).setOccupiedBy(process.getPid());
                requiredPages--;
            }
            return;}

            // Page requiredPage = new Page(i, -1, (int) pageSize);

        //     if (pageTable.contains(requiredPage)) {
        //         System.out.println("Page " + requiredPage.getId() + " is already in memory (Page Hit)");
        //     } else {
        //         handlePageFault(requiredPage);
        //         System.out.println("Page " + requiredPage.getId() + " loaded into memory (Page Fault) and the process in it is process " + process.getPid());
        //     }
        // }

        // System.out.println("Process " + process.getPid() + " execution completed at time " + Global.CLOCK + ".\n");
    }

    private void handlePageFault(Page page) {
        if (frames.size() < numberOfPages) {
            page.setBase(frames.size() * (int) pageSize);
        } else {
            Page removedPage = frames.removeFirst();
            pageTable.remove(removedPage);
            System.out.println("Page " + removedPage.getId() + " removed from Frame " + removedPage.getBase());
            page.setBase(removedPage.getBase());
        }

        frames.add(page);
        pageTable.add(page);
    }
}

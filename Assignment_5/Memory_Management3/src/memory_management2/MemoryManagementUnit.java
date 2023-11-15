package memory_management2;
import java.util.ArrayList;
import java.util.LinkedList;
class MemoryManagementUnit {
    private double virtualMemorySize;
    private double diskSize;
    private double backStoreSize;
    private double RAMSize;
    private double pageSize;
    private double osSize;
    private int numberOfPages;
    private ArrayList<Page> pageTable;
    private LinkedList<Page> frames;
    private LinkedList<Page> lruQueue = new LinkedList<>();
    private int pageFaults = 0;

    public MemoryManagementUnit(double virtualMemorySize, double diskSize, double backStoreSize,
                                ArrayList<Page> pages, double RAMSize, double pageSize, double osSize, int numberOfPages) {
        this.virtualMemorySize = virtualMemorySize;
        this.diskSize = diskSize;
        this.backStoreSize = backStoreSize;
        this.RAMSize = RAMSize;
        this.pageSize = pageSize;
        this.osSize = osSize;
        this.numberOfPages = numberOfPages;
        this.pageTable = pages; // Fixed: Assign the provided 'pages' to the 'pageTable'
        this.frames = new LinkedList<>();
    }

     public void executeProcess(Process process) {
        System.out.println("\nExecuting Process " + process.getPid() + " with Size " + process.getSizeNeeded() + " KB With Burst time of " + process.getBurstTime());

        int requiredPages = (int) Math.ceil(process.getSizeNeeded() / pageSize);

        int counter = 0;
        while (requiredPages > 0 && counter < numberOfPages) {
            Page currentPage = pageTable.get(counter);
            if (currentPage.getOccupiedBy() == -1 || currentPage.getOccupiedBy() == process.getPid()) {
                // Allocate the page to the process if unoccupied or already occupied by the same process
                currentPage.setOccupiedBy(process.getPid());
                lruQueue.addLast(currentPage); // Add the page to the end of the LRU queue
                requiredPages--;

                // Print the history
                System.out.println("Page " + currentPage.getId() + " allocated to Process " + process.getPid());
            } else {
                // Page is occupied by a different process, update its position in the LRU queue
                lruQueue.remove(currentPage); // Remove the page from its current position
                lruQueue.addLast(currentPage); // Add the page to the end of the LRU queue
            }
            counter++;
        }

        // If there are more pages to allocate than available, perform LRU page replacement
        while (requiredPages > 0 && lruQueue.size() > 0) {
            Page leastRecentlyUsed = lruQueue.removeFirst(); // Get the least recently used page
            leastRecentlyUsed.setOccupiedBy(process.getPid()); // Allocate the page to the process
            lruQueue.addLast(leastRecentlyUsed); // Add the page to the end of the LRU queue
            requiredPages--;

            // Print the history
            System.out.println("Page " + leastRecentlyUsed.getId() + " replaced and allocated to Process " + process.getPid());
            pageFaults++;
        }

        // Check for additional page faults
        if (requiredPages > 0) {
            System.out.println("Page fault(s) occurred. Unable to allocate all required pages for Process " + process.getPid());
            pageFaults += requiredPages;
        }
    }

    public void printPageAllocationHistory() {
        System.out.println("\nPage Allocation History:");
        for (Page page : pageTable) {
            System.out.println("Page " + page.getId() + " - Occupied By: " + (page.getOccupiedBy() == -1 ? "Unoccupied" : "Process " + page.getOccupiedBy()));
        }
        System.out.println("\nTotal Page Faults: " + pageFaults);
    }

}
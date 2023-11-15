package memory_management2;
import java.util.ArrayList;
import java.util.LinkedList;
import java.lang.Integer;
class MemoryManagementUnit {
    private double pageSize;
    private int numberOfPhysicalPages;
    private ArrayList<Page> physicalPageTable;
    private int numberOfVirtualPages;
    private ArrayList<Page> virtualPageTable;
    // private LinkedList<Page> frames;
    private LinkedList<Page> lruQueue = new LinkedList<>();
    private int pageFaults = 0;

    public MemoryManagementUnit(ArrayList<Page> physicalPages, int numberOfPhysicalPages,
                                ArrayList<Page> virtualPageTable, int numberOfVirtualPages, double pageSize) {
        this.pageSize = pageSize;
        this.numberOfPhysicalPages = numberOfPhysicalPages;
        this.physicalPageTable = physicalPages; // Fixed: Assign the provided 'pages' to the 'physicalPageTable'
        this.virtualPageTable = virtualPageTable;
        this.numberOfVirtualPages = numberOfVirtualPages;
        // this.frames = new LinkedList<>();
    }

     public void executeProcess(Process process) {
        System.out.println("\nExecuting Process " + process.getPid() + " with Size " + process.getSizeNeeded() + " KB With Burst time of " + process.getBurstTime());

        int requiredPages = (int) Math.ceil(process.getSizeNeeded() / pageSize);

        int counter = 0;
        while (requiredPages > 0 && counter < numberOfPhysicalPages) {
            Page currentPage = physicalPageTable.get(counter);
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
        if (requiredPages > 0)
        {ArrayList<Integer> physicalSwapPages = new ArrayList<Integer>();
        ArrayList<Integer> virtualSwapPages = new ArrayList<Integer>();
        // If there are more pages to allocate than available, perform LRU page replacement
        while (requiredPages > 0 && lruQueue.size() > 0) {
            Page leastRecentlyUsed = lruQueue.removeFirst(); // Get the least recently used page
            int pid = leastRecentlyUsed.getOccupiedBy();
            for (int i = 0; i < numberOfPhysicalPages; i++) {
                if (pid == physicalPageTable.get(i).getOccupiedBy()) {
                    physicalSwapPages.add(i);
                    requiredPages--;
                    if (requiredPages <= 0)
                        break;
                    pageFaults++;
                }
            }
            // for (int i = 0; i < numberOfPhysicalPages; i++) {
            //     System.out.println(physicalSwapPages.get(i));
            // }
            // System.exit(0);
        }
        for (int i = 0, j = numberOfPhysicalPages; i < numberOfVirtualPages && j > 0; i++)
        if (virtualPageTable.get(i).getOccupiedBy() == -1) {
            virtualSwapPages.add(i);
            j--;
        }
        
        for (int i = 0; i < numberOfPhysicalPages; i++) {
            // System.out.println("Page " + leastRecentlyUsed.getId() + " replaced from and allocated to Process " + process.getPid());
            System.out.format("Physical Page %d having process %d is replaced by Virtual Page %d having process %d\n", physicalPageTable.get(i).getId(), physicalPageTable.get(i).getOccupiedBy(), virtualPageTable.get(i).getId(), virtualPageTable.get(i).getOccupiedBy());
            swapIn_swapOut(physicalPageTable.get(i), virtualPageTable.get(i));
        }
        
        // Check for additional page faults
        if (requiredPages > 0) {
            System.out.println("Page fault(s) occurred. Unable to allocate all required pages for Process " + process.getPid());
            pageFaults += requiredPages;
        }}
    }

    public void printPageAllocationHistory() {
        System.out.println("\nPage Allocation History:");
        for (Page page : physicalPageTable) {
            System.out.println("Page " + page.getId() + " - Occupied By: " + (page.getOccupiedBy() == -1 ? "Unoccupied" : "Process " + page.getOccupiedBy()));
        }
        System.out.println("\nTotal Page Faults: " + pageFaults);
    }
    public void removeProcess(int pid) {
        for (Page page : physicalPageTable)
            if (page.getOccupiedBy() == pid)
                page.setOccupiedBy(-1);
    }

    public void swapIn_swapOut(Page pPage, Page vPage) {
        int occupiedBy = pPage.getOccupiedBy();
        int id = pPage.getId();
        pPage.setId(vPage.getId());
        pPage.setOccupiedBy(vPage.getOccupiedBy());
        vPage.setId(id);
        vPage.setOccupiedBy(occupiedBy);
    }

}
package memory_management2;
import java.util.ArrayList;
import java.util.Random;

public class Main {

    public static void main(String[] args) {
        // final double size_virtual_memory = 100;
        final double size_virtual_memory = 50;
        // final double size_disk = 80000 - size_virtual_memory;
        // final double size_back_store = 0.1 * size_disk;
        // final double size_RAM = 200;
        final double size_RAM = 100;
        final double size_page = 4;
        final double size_os = 50;
        int numberOfVirtualPages = (int) (size_virtual_memory / size_page);
        int numberOfPhysicalPages = (int) ((size_RAM - size_os) / size_page);
        ArrayList<Page> physicalPages = new ArrayList<Page>();
        ArrayList<Page> virtualPages = new ArrayList<Page>();

        // Initialize processes
        ArrayList<Process> processes = createProcesses(30);
        ArrayList<Process> arrivedProcesses = new ArrayList<Process>();

        for (int i = (int) size_os, j = 0; j < numberOfPhysicalPages; i += size_page, j++)
            physicalPages.add(new Page(j, i, (int) size_page));
        for (int i = 0, j = numberOfPhysicalPages; j < numberOfVirtualPages + numberOfPhysicalPages; i += size_page, j++)
            virtualPages.add(new Page(j, i, (int) size_page));
        // Create memory management unit (MMU)
        MemoryManagementUnit mmu = new MemoryManagementUnit(physicalPages, numberOfPhysicalPages, virtualPages, numberOfVirtualPages, size_page);

        System.out.format("Number of physicalPages %d\n", numberOfPhysicalPages);
        System.out.format("Number of virtualPages %d\n", numberOfVirtualPages);
        while (true) {
            System.out.format("\n*******At Time %d *******\n", ++Global.CLOCK);
            for (int i = 0; i < processes.size(); i++)
                if (processes.get(i).getArrivalTime() == Global.CLOCK)
                    arrivedProcesses.add(processes.get(i));
            for (int i = 0; i < arrivedProcesses.size() - 1; i++)
                mmu.executeProcess(arrivedProcesses.get(i));
            for (int i = 0; i < arrivedProcesses.size(); i++) {
                arrivedProcesses.get(i).decrementBurstTime();
                if (arrivedProcesses.get(i).getBurstTime() == 0) {
                    System.out.format("\n++++At Time %d execution of %d is done++++\n",
                            Global.CLOCK, arrivedProcesses.get(i).getPid());
                    mmu.removeProcess(arrivedProcesses.get(i).getPid());
                    arrivedProcesses.remove(i);
                }
            }
            if (Global.CLOCK == 100)
                break;
        }
    }

    private static ArrayList<Process> createProcesses(int count) {
        ArrayList<Process> processes = new ArrayList<>();
        Random random = new Random();

        for (int i = 1; i <= count; i++) {
            int arrivalTime = random.nextInt(10);
            int burstTime = random.nextInt(20) + 1;
            // double sizeNeeded = random.nextDouble() * 20;
            // double sizeNeeded = 200;
            double sizeNeeded = 4;

            processes.add(new Process(i, arrivalTime, burstTime, sizeNeeded));
        }

        return processes;
    }
}

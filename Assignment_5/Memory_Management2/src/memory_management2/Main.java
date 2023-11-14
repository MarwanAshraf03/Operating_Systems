package memory_management2;
import java.util.ArrayList;
import java.util.Random;

// import memory_management.page;

public class Main {
    

    public static void main(String[] args) {
        final double virtual_memory = 10000;
        final double size_disk = 80000 - virtual_memory;
        final double size_back_store = 0.1 * size_disk;
        final double size_RAM = 2000;
        final double size_page = 4;
        final double size_os = 50;
        int number_of_pages = (int) ((size_RAM - size_os) / size_page);
        ArrayList<Page> pages = new ArrayList<Page>();

        // Initialize processes
        ArrayList<Process> processes = createProcesses(10);
        ArrayList<Process> arrivedProcesses = new ArrayList<Process>();

        for (int i = (int) size_os, j = 0; j < number_of_pages; i += size_page, j++)
            pages.add(new Page(j, i, (int) size_page));


        // Create memory management unit (MMU)
        MemoryManagementUnit mmu = new MemoryManagementUnit(virtual_memory, size_disk, size_back_store,
                pages, size_RAM, size_page, size_os, number_of_pages);


        System.out.format("Number of pages %d\n", number_of_pages);
        while (true) {
            System.out.format("\n*******At Time %d *******\n", ++Global.CLOCK);
            for (int i = 0; i < processes.size(); i++)
                if (processes.get(i).getArrivalTime() == Global.CLOCK)
                    arrivedProcesses.add(processes.get(i));
            for (int i = 0; i < arrivedProcesses.size(); i++)
                mmu.executeProcess(arrivedProcesses.get(i));
            for (int i = 0; i < arrivedProcesses.size(); i++) {
                arrivedProcesses.get(i).decrementBurstTime();
                if (arrivedProcesses.get(i).getBurstTime() == 0) {
                    System.out.format("\n++++At Time %d execution of %d is done++++\n",
                    Global.CLOCK, arrivedProcesses.get(i).getPid());
                    arrivedProcesses.remove(i);
                }
            }
            if (Global.CLOCK == 100)
                break;
        }

                // Simulate process execution
        // while (!processes.isEmpty()) {
        //     Process currentProcess = processes.get(0);

        //     // Execute process until burst time is complete
        //     while (currentProcess.getBurstTime() > 0) {
        //         mmu.executeProcess(currentProcess);
        //         Global.CLOCK++;
        //         currentProcess.decrementBurstTime();

        //         if (currentProcess.getBurstTime() == 0) {
        //             System.out.println("Process " + currentProcess.getPid() + " completed at time " + Global.CLOCK);
        //             processes.remove(0);
        //             break;
        //         }
        //     }
        // }
    }

    private static ArrayList<Process> createProcesses(int count) {
        ArrayList<Process> processes = new ArrayList<>();
        Random random = new Random();

        for (int i = 1; i <= count; i++) {
            int arrivalTime = random.nextInt(10);
            int burstTime = random.nextInt(20) + 1;
            // double sizeNeeded = random.nextDouble() * 10;
            double sizeNeeded = random.nextDouble() * 200;

            processes.add(new Process(i, arrivalTime, burstTime, sizeNeeded));
        }

        return processes;
    }
}

package memory_management2;
import java.util.ArrayList;
import java.util.Random;

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
        ArrayList<Process> processes = createProcesses(1000);
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
    }

    private static ArrayList<Process> createProcesses(int count) {
        ArrayList<Process> processes = new ArrayList<>();
        Random random = new Random();

        for (int i = 1; i <= count; i++) {
            int arrivalTime = random.nextInt(10);
            int burstTime = random.nextInt(20) + 1;
            double sizeNeeded = random.nextDouble() * 200;

            processes.add(new Process(i, arrivalTime, burstTime, sizeNeeded));
        }

        return processes;
    }
}

package memory_management;

/**
 * ALL SIZES IN THIS CODE IS CALCULATED BY KB => (KILO BYTES)
 * page_fault: number of faults happened (this indicates the
 *  number of swap in and swap out)
 * timer: a timer to keep track of all the timing processing
 *  in the code
 * size_disk: size of the hard disk
 * size_back_store: size of the back store
 *  (the storage that is used to store process data before
 *      the data is moved from memory to virtual memory)
 * size_RAM: size of the main memory
 * size_page: the size of the page
 * size_os: size of the operating system to calculate logical addresses
 * number_of_pages: number of pages without using the space of the
 *  operating system
 * pages: array of pages
 */

public class Main {
public static void main(String[] args) {
        int page_fault = 0;
        int timer = -1;
        final double virtual_memory = 10000;
        final double size_disk = 80000 - virtual_memory;
        final double size_back_store = 0.1 * size_disk;
        final double size_RAM = 2000;
        final double size_page = 4;
        final double size_os = 50;
        int number_of_pages = (int) ((size_RAM - size_os) / size_page);
        page[] pages = new page[number_of_pages];

        while (true) {
            timer = timer + 1;
            timer = (int) size_back_store;
            page_fault = page_fault + 1;
            break;
        }

        for (int i = (int) size_os, j = 0; j < number_of_pages; i += size_page, j++)
            pages[j] = new page(j, i, (int) size_page);
        System.out.print("page address is: \n");
        for (int i = 0; i < pages.length; i++)
            System.out.format("id => %d, base => %d\n", pages[i].id_getter(), pages[i].base_getter());
        System.out.println();
        System.out.format("number of pages = %d", number_of_pages);
    }  
}
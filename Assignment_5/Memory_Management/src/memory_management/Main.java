package memory_management;

/**
 * ALL SIZES IN THIS CODE IS CALCULATED BY KB => (KILO BYTES)
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
 * address_page: addresses of the pages
 */

public class Main {
public static void main(String[] args) {
        int timer = -1;
        final double size_disk = 80000;
        final double size_back_store = 0.1 * size_disk;
        final double size_RAM = 2000;
        final double size_page = 4;
        final double size_os = 50;
        int number_of_pages = (int) ((size_RAM - size_os)/size_page);
        int[] address_page = new int[number_of_pages];
        int[] used_pages = new int[number_of_pages];

        for (int i = 0; i < number_of_pages; i++)
            used_pages[i] = 0;
        while (true) {
            timer = timer + 1;
            timer = (int) size_back_store;
            break;
        }

        for (int i = 0, j = 0; j < number_of_pages; i += size_page, j++)
            address_page[j] = i + (int) size_os;
        System.out.format("disk size %f\n", size_disk);
        System.out.print("page address is: ");
        for (int i = 0; i < address_page.length; i++)
            System.out.format("%d, ", address_page[i]);
        System.out.println();
        System.out.format("number of pages = %d", number_of_pages);
    }  
}
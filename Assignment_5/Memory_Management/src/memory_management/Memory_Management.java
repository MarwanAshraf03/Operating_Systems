package memory_management;
public class Memory_Management {
public static void main(String[] args) {
    /**
     * This is the main function 
     * there should be the size of the disk
     * and the size of the RAM
     * the size of the page is 4kb
     * the sizes of the code is measured by kilo bytes
     * first the processes to be used must have class
     * the class should have base and limit logical address
     * memory
     * the class should have base and limit logical address
     */
        double size_disk = 80000;
        double size_RAM = 2000;
        double size_os = 30;
        int number_of_pages = (int) ((size_RAM - size_os)/4.0);
        
        int[] address_page = new int[number_of_pages];

        for (int i = 0; i < number_of_pages; i++)
            address_page[i] = i + (int) size_os;
        process p1 = new process(12);
        System.out.println(p1.pid_getter());
        System.out.println(size_disk);
    }  
}
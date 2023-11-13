package memory_management;

/**
 * base: the base address of the page
 * limit: the limit address of the page
 * valid: a flag to show if the page is in the main
 *  memory or the virtual memory
 * occubied_by: if the page is occubied this variable 
 *  should have the pid of that page
 * last_time_used: the last time this page was used
 */

public class page {
    private int id;
    private int base;
    private int limit;
    private int valid;
    private int occubied_by;
    private int last_time_used;

    public page(int id, int base, int size_page){
        this.id = id;
        this.base = base;
        this.limit = this.base + size_page;
        this.valid = 1;
        this.occubied_by = -1;
        this.last_time_used = 0;
    }

    public int id_getter(){
        return this.id;
    }
    public int base_getter(){
        return this.base;
    }
    public void base_setter(int base){
        this.base = base;
    }

    public int limit_getter(){
        return this.limit;
    }
    public void limit_setter(int limit){
        this.limit = limit;
    }

    public int valid_getter(){
        return this.valid;
    }
    public void valid_setter(int valid){
        this.valid = valid;
    }

    public int occubied_by_getter(){
        return this.occubied_by;
    }
    public void occubied_by_setter(int occubied_by){
        this.occubied_by = occubied_by;
    }

    public int last_time_used_getter(){
        return this.last_time_used;
    }
    public void last_time_used_setter(int last_time_used){
        this.last_time_used = last_time_used;
    }




}

package memory_management;
import java.util.ArrayList;

/**
 * This is a virtual machine class
 *  to contain the region details
 *  which is some pages.
 * the size is in bytes.
 * the attributes is yet to be known 
 *  what does it do
 */

public class vm {
    private int resident_pages;
    private double size;
    private ArrayList<Object> attributes = new ArrayList<>();
    public int resident_pages_getter(){
        return resident_pages;
    }
    public double size_getter(){
        return size;
    }
    public ArrayList<Object> attributes_getter(){
        return attributes;
    }
    public void resident_pages_setter(int resident_pages){
        this.resident_pages = resident_pages;
    }
    public void size_setter(double size){
        this.size = size;
    }
    public void attributes_setter(ArrayList<Object> attributes){
        this.attributes = attributes;
    }
}

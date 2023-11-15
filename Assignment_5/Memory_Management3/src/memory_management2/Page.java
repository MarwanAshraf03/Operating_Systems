package memory_management2;

class Page {
    private int id;
    private int base;
    private int limit;
    private int valid;
    private int occupiedBy;
    private int lastTimeUsed;

    public Page(int id, int base, int sizePage) {
        this.id = id;
        this.base = base;
        this.limit = this.base + sizePage;
        this.valid = 1;
        this.occupiedBy = -1;
        this.lastTimeUsed = 0;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getBase() {
        return base;
    }

    public void setBase(int base) {
        this.base = base;
    }

    public int getLimit() {
        return limit;
    }

    public void setLimit(int limit) {
        this.limit = limit;
    }

    public int getValid() {
        return valid;
    }

    public void setValid(int valid) {
        this.valid = valid;
    }

    public int getOccupiedBy() {
        return occupiedBy;
    }

    public void setOccupiedBy(int occupiedBy) {
        this.occupiedBy = occupiedBy;
    }

    public int getLastTimeUsed() {
        return lastTimeUsed;
    }

    public void setLastTimeUsed(int lastTimeUsed) {
        this.lastTimeUsed = lastTimeUsed;
    }
}

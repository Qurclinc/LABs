import java.util.Objects;

public class Client {
    private Integer ID;
    private Integer year;
    private Integer month;
    private Integer duration;

    public Client(Integer ID, Integer year, Integer month, Integer duraion) {
        this.ID = ID;
        this.year = year;
        this.month = month;
        this.duration = duraion;
    }

    public Client() {
        this(0, 1970, 1, 1);
    }

    public Client(Client other) {
        this.ID = other.ID;
        this.year = other.year;
        this.month = other.month;
        this.duration = other.duration;
    }

    public Integer getID() { return this.ID; }
    public Integer getYear() { return this.year; }
    public Integer getMonth() { return this.month; }
    public Integer getDuration() { return this.duration; }

    @Override
    public boolean equals(Object obj) {
        return this.ID == ((Client)(obj)).ID;
    }

    @Override
    public int hashCode() {
        return Objects.hash(this.ID);
    }

    public void printInfo() {
        System.out.printf("ID: %d\nyear: %d\nmonth: %d\nduration: %d\n\n",
                            this.ID, this.year, this.month, this.duration);
    }
}

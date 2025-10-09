package Task2.src;
import java.time.*;

public class MyFile {
    private String filename;
    private int size;
    private LocalDateTime creationDate;
    private LocalDateTime changeDate;
    private int accessCount;

    MyFile(String filename, int size, LocalDateTime creationDate, LocalDateTime changeDate, int accessCount) {
        this.filename = filename;
        this.size = size;
        this.creationDate = creationDate;
        this.changeDate = changeDate;
        this.accessCount = accessCount;
    }

    @Override
    public String toString() {
        return String.format("File %s\n%d KB\nCreated at: %s\nChanged at: %s\nAccessed %d times",
        this.filename,
        this.size,
        this.creationDate.toString(), this.changeDate.toString(),
        this.accessCount);
    }
}

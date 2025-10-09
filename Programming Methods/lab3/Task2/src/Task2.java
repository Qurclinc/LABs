package Task2.src;
import java.time.*;

public class Task2 {
    public static void main(String[] args) {
        MyFile file = new MyFile("aboba.txt",
                            10,
                            LocalDateTime.now(),
                            LocalDateTime.now(),
                            15);
        System.out.println(file);
    }
}
import java.util.stream.*;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public class Task2 {

    public static <T> void printList(List<T> lst) {
        for (T el : lst) {
            System.out.println(el);
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        List<Integer> lst = new Random()
        .ints(10, -100, 101)
        .boxed()
        .collect(Collectors.toList());

        printList(lst);

        lst = lst.stream()
        .filter(n -> {
            return n < 0 && n % 2 == 0;
        })
        .sorted(Comparator.reverseOrder())
        .collect(Collectors.toList());
        printList(lst);
    }
}

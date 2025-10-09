import java.util.Comparator;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;
import java.util.stream.*;

public class Task3 {

    public static <T> void printList(List<T> lst) {
        for (T el : lst) {
            System.out.println(el);
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        int size = 5, K = 2;
        Random rnd = new Random();
        List<String> A = Stream.generate(() -> {
            int length = rnd.nextInt(5, 10);
            return rnd.ints(length, 'a', 'z' + 1)
            .mapToObj(w -> String.valueOf((char)w))
            .collect(Collectors.joining());
        })
        .limit(size)
        .collect(Collectors.toList());

        printList(A);

        List<String> B = Stream.concat(
            A.stream()
            .limit(K)
            .map(w -> {
                StringBuilder builder = new StringBuilder();
                for (int i = 0; i < w.length(); i++) {
                    if ((i + 1) % 2 != 0) {
                        builder.append(w.charAt(i));
                    }
                }
                return builder.toString();
            })
            .skip(0),
            
            A.stream()
            .skip(K)
            .map(w -> {
                StringBuilder builder = new StringBuilder();
                for (int i = 0; i < w.length(); i++) {
                    if ((i + 1) % 2 == 0) {
                        builder.append(w.charAt(i));
                    }
                }
                return builder.toString();
            })
            .skip(0))
            .sorted(Comparator.reverseOrder())
            .collect(Collectors.toList());
        printList(B);
    }
}

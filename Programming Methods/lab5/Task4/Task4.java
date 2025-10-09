import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Task4 {

    public static <T> void printList(List<T> lst) {
        for (T el : lst) {
            System.out.println(el);
        }
        System.out.println();
    }

    public static List<String> initializeList(String filename) {
        try(Stream<String> lines = Files.lines(Paths.get(filename))) {
            return lines
            .filter(w -> {
                return w.matches("[A-Z0-9]+");
            })
            .collect(Collectors.toList());
        } catch (Exception e) {
            return null; 
        }
    }

    public static void main(String[] args) {    
        int L1 = 4, L2 = 7;

        List<String> A = initializeList("A.txt");
        List<String> B = initializeList("B.txt");
        printList(A);
        printList(B);

        List<String> C = Stream.concat(
            A.stream()
            .filter(w -> {
                return w.length() == L1;
            })
            ,
            B.stream()
            .filter(w -> {
                return w.length() == L2;
            })
        )
        .sorted(Comparator.reverseOrder())
        .collect(Collectors.toList());

        printList(C);
    }
}
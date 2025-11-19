import java.util.ArrayList;
import java.util.Arrays;
import java.util.Map;
import java.util.stream.*;

public class Task1 {
    public static void main(String[] args) {
        ArrayList<Client> clients = new ArrayList<Client>(Arrays.asList(
            new Client(1, 2000, 5, 5),
            new Client(3, 2025, 8, 9),
            new Client(1, 2300, 5, 10),
            new Client(2, 2025, 4, 7),
            new Client(1, 2025, 2, 8),
            new Client(2, 2025, 8, 2)
        ));
        
        // Map<Integer, Integer> output = new HashMap<>();
        // for (var i : clients.stream().distinct().map(cl -> cl.getID()).collect(Collectors.toList())) {
        //     int sum = clients.stream()
        //     .filter(x -> x.getID() == i)
        //     .mapToInt(x -> x.getDuration())
        //     .sum();
           //     output.put(i, sum);
        // }

        Map<Integer, Integer> output = clients.stream()
        .collect(Collectors.groupingBy(Client::getID, Collectors.summingInt(Client::getDuration)));

        output.entrySet().stream()
        .sorted( (e1, e2) -> {
            int sComp = e2.getValue().compareTo(e1.getValue());
            if (sComp != 0) { return sComp; }
            return e1.getKey().compareTo(e2.getKey());
        })
        .forEach(e -> {
            System.out.printf("Суммарная продолжительность: %d\t\tID: %d\n", e.getValue(), e.getKey());
        });
    }
}
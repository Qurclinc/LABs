
import java.lang.Exception;
import java.util.ArrayList;
import java.util.List;
import java.util.Arrays;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.stream.Collectors;

public class Task3 {
    public static void main(String[] args) {
        Integer FLATS = 144;
        Integer FLOORS = 9;
        House house = new House(FLATS, FLOORS, 4);
        // System.out.println(house.getFlatsPerFloor());
        // house.printFlats();
        ArrayList<Person> debtors = new ArrayList<>();
        try {
            debtors = new ArrayList<>(Arrays.asList(
                new Person("Иванов", 10, 14.88),
                new Person("Частухина", 9, 14.88),
                new Person("Корнев", 15, 1337.18),
                new Person("Сларков", 30, 6724D),
                new Person("Павлов", 34, 67.15),
                new Person("Антоненко", 35, 78.78),
                new Person("Бачурина", 106, 30.88)
            ));
        } catch (Exception ex) {
            System.out.println(ex.toString());
        }

        Map<Integer, List<Person>> grouped = debtors.stream()
        .collect(Collectors.groupingBy(x -> {
            return house.getFloorByFlat(x.getFlat());
        }));

        Map<Integer, Double> result = grouped.entrySet().stream()
        .sorted(Comparator.comparingInt((Map.Entry<Integer, List<Person>> x) -> x.getValue().size()).reversed().thenComparing(Comparator.comparingInt(k -> k.getKey())))
        .collect(Collectors.toMap(
            Map.Entry::getKey,
            x -> x.getValue().stream().mapToDouble(Person::getDebt).sum(),
            (a, b) -> a,
            LinkedHashMap::new
        ));
        
        result.entrySet().stream()
        .forEach(el -> {
            System.out.printf("Этаж: %d\tДолг: %5.2f\n", el.getKey(), el.getValue());
        });
    }
}
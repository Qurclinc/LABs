import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class House {
    private Map<Integer, ArrayList<Integer>> flats = new HashMap<>();
    private Integer flatsPerFloor;
    private Integer entrances;
    private Integer flatsAmount;
    private Integer floors;

    public House(Integer flatsAmount, Integer floors, Integer entrances) {
        this.entrances = entrances;
        this.flatsAmount = flatsAmount;
        this.floors = floors;
        this.flatsPerFloor = this.flatsAmount / this.floors / this.entrances;

        Integer flatsPerEntrance = this.flatsAmount / this.entrances;
        Integer flatsPerFloorForEntance = flatsPerEntrance / floors;

        for (Integer floor = 1; floor <= this.floors; floor++) {
            var list = new ArrayList<Integer>();

            for (Integer entrance = 1; entrance <= this.entrances; entrance++) {
                Integer firstFlatInEntrance = (entrance - 1) * flatsPerEntrance + 1;
                Integer firstFlatInFloor = firstFlatInEntrance + (floor - 1) * flatsPerFloorForEntance;

                for (Integer i = 0; i < flatsPerFloorForEntance; i++) {
                    list.add(firstFlatInFloor + i);
                }
            }
            
            flats.put(floor, list);
        }
    }

    public Integer getFlatsPerFloor() { return this.flatsPerFloor; }
    public Integer getFlatsAmount() { return this.flatsAmount; }
    public Integer getFloors() { return this.floors; }
    public Integer getEntrances() { return this.entrances; }

    public void printFlats() {
        // System.out.println(this.flats);
        this.flats.entrySet().stream()
        .forEach(floor -> {
            System.out.printf("Этаж %d:\t", floor.getKey());
            floor.getValue().stream()
            .sorted()
            .forEach(flat -> {
                System.out.printf("%d\t", flat);
            });
            System.out.println();
        });
    }

    public ArrayList<Integer> getFlatsByFloor(Integer floor) {
        return this.flats.getOrDefault(floor, new ArrayList<Integer>());
    }

    public Integer getFloorByFlat(Integer flat) {
        return this.flats.entrySet().stream()
        .filter(entry -> entry.getValue().contains(flat))
        .map(entry -> entry.getKey())
        .findFirst()
        .orElse(-1);
    }

}

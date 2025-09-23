from typing import List, Tuple

class KarnoughMaps:
    def __init__(self, func: List[int]):
        self.size = 4
        self.table: List[List[int]] = []
        self.func = func
        self.init_table(func)

        # подписи строк/столбцов (Грей-код)
        self.row_labels = ["00", "01", "11", "10"]  # AB
        self.col_labels = ["00", "01", "11", "10"]  # CD

    def get_table(self) -> List[List[int]]:
        return self.table

    def init_table(self, func: List[int]):
        """Инициализация таблицы с правильным порядком минтермов"""
        # Правильное соответствие позиций в таблице номерам минтермов
        mapping = [
            [0,  1,  3,  2],
            [4,  5,  7,  6],
            [12, 13, 15, 14],
            [8,  9,  11, 10]
        ]
        
        for i in range(4):
            row = []
            for j in range(4):
                row.append(1 if mapping[i][j] in func else 0)
            self.table.append(row)

    def _get_vars(self, row: int, col: int) -> List[int]:
        A, B = self.row_labels[row]
        C, D = self.col_labels[col]
        return [int(A), int(B), int(C), int(D)]

    def _make_term(self, cells: List[Tuple[int, int]]) -> str:
        """Строим логический член по множеству клеток"""
        vars_fixed = [None] * 4
        for (r, c) in cells:
            vals = self._get_vars(r, c)
            for i, v in enumerate(vals):
                if vars_fixed[i] is None:
                    vars_fixed[i] = v
                elif vars_fixed[i] != v:
                    vars_fixed[i] = "x"  # переменная сокращается
        
        expr = []
        for i, v in enumerate(vars_fixed):
            if v == "x":
                continue
            name = "ABCD"[i]
            expr.append(name if v == 1 else f"{name}'")
        
        return "".join(expr) if expr else "1"

    def _all_groups(self) -> List[List[Tuple[int, int]]]:
        """Генерация всех допустимых групп (с оборачиванием)"""
        groups = []
        
        # Проверяем возможность создания группы заданного размера
        def can_form_group(start_r, start_c, height, width):
            for dr in range(height):
                for dc in range(width):
                    r = (start_r + dr) % 4
                    c = (start_c + dc) % 4
                    if self.table[r][c] != 1:
                        return False
            return True
        
        # Возможные размеры групп
        sizes = [(1, 1), (1, 2), (2, 1), (2, 2), (1, 4), (4, 1), (4, 2), (2, 4), (4, 4)]
        
        for h, w in sizes:
            for r in range(4):
                for c in range(4):
                    if can_form_group(r, c, h, w):
                        cells = []
                        for dr in range(h):
                            for dc in range(w):
                                rr = (r + dr) % 4
                                cc = (c + dc) % 4
                                cells.append((rr, cc))
                        cells = sorted(set(cells))
                        if cells not in groups:
                            groups.append(cells)
        
        return groups

    def minimize(self) -> str:
        groups = self._all_groups()

        # строим импликанты
        implicants = {tuple(g): self._make_term(g) for g in groups}

        # удаляем группы, которые полностью содержатся в других
        prime_implicants = {}
        for g1, term1 in implicants.items():
            is_prime = True
            for g2, term2 in implicants.items():
                if g1 != g2 and set(g1).issubset(set(g2)):
                    is_prime = False
                    break
            if is_prime:
                prime_implicants[g1] = term1

        # покрытие минтермов
        minterms = [(r, c) for r in range(4) for c in range(4) if self.table[r][c] == 1]

        essential_terms = []
        covered = set()

        while covered != set(minterms):
            # находим импликант, покрывающий наибольшее количество ещё не покрытых клеток
            best_group, best_term = None, None
            best_cover_count = 0
            
            for g, term in prime_implicants.items():
                uncovered = set(g) - covered
                if len(uncovered) > best_cover_count:
                    best_cover_count = len(uncovered)
                    best_group, best_term = g, term
            
            if best_group is None:
                break
                
            essential_terms.append(best_term)
            covered |= set(best_group)

        return " + ".join(essential_terms) if essential_terms else "0"

from typing import List, Dict, Set, Tuple
import itertools


class McCluskey:
    def __init__(self, func: List[int], n_vars: int = 4, dontcares: List[int] = None):
        """
        func: список минтермов (целые номера)
        n_vars: число переменных (по умолчанию 4)
        dontcares: необязательный список dont-care минтермов
        """
        self.n = n_vars
        self.minterms = sorted(set(func))
        self.dontcares = sorted(set(dontcares)) if dontcares else []
        self._init_terms()

    def _init_terms(self):
        # term: dict {'pattern': str, 'minterms': frozenset, 'used': False}
        self.terms = []
        for m in sorted(self.minterms + self.dontcares):
            pat = format(m, "b").zfill(self.n)
            self.terms.append({'pattern': pat, 'minterms': frozenset([m]), 'used': False})

    def __str__(self):
        return "\n".join([t['pattern'] for t in self.terms])

    @staticmethod
    def _count_ones(pat: str) -> int:
        return pat.count("1")

    @staticmethod
    def _can_combine(a: str, b: str) -> bool:
        """Можно ли совместить две маски: отличаются ровно в одной позиции
           и в местах '-' обе одинаковы (т.е. не комбинируют '-' с '0'/'1')."""
        if len(a) != len(b):
            return False
        diff = 0
        for ca, cb in zip(a, b):
            if ca == cb:
                continue
            # нельзя комбинировать '-' с '0'/'1'
            if ca == "-" or cb == "-":
                return False
            # разница 0/1
            diff += 1
            if diff > 1:
                return False
        return diff == 1

    @staticmethod
    def _combine_patterns(a: str, b: str) -> str:
        """Возвращает объединённую маску (с '-') при условии, что can_combine True."""
        out = []
        for ca, cb in zip(a, b):
            if ca == cb:
                out.append(ca)
            else:
                out.append("-")
        return "".join(out)

    def _group_terms(self, terms: List[Dict]) -> Dict[int, List[Dict]]:
        groups: Dict[int, List[Dict]] = {}
        for t in terms:
            k = self._count_ones(t['pattern'])
            groups.setdefault(k, []).append(t)
        # сортировка для предсказуемости
        for k in groups:
            groups[k].sort(key=lambda x: x['pattern'])
        return groups

    def _iterate_combinations(self) -> Tuple[List[Dict], List[str]]:
        """Одна итерация комбинирования: возвращает список новых терминов и лог шагов."""
        groups = self._group_terms(self.terms)
        new_terms: List[Dict] = []
        steps: List[str] = []

        used_pairs = set()
        produced = {}

        ks = sorted(groups.keys())
        for k in ks:
            if (k + 1) not in groups:
                continue
            for t1 in groups[k]:
                for t2 in groups[k + 1]:
                    p1, p2 = t1['pattern'], t2['pattern']
                    if self._can_combine(p1, p2):
                        newpat = self._combine_patterns(p1, p2)
                        new_min = frozenset(t1['minterms'] | t2['minterms'])
                        key = (newpat, new_min)
                        if key not in produced:
                            produced[key] = {'pattern': newpat, 'minterms': new_min, 'used': False}
                        # помечаем исходные как использованные
                        t1['used'] = True
                        t2['used'] = True
                        steps.append(f"{p1} + {p2} -> {newpat} (covers {sorted(new_min)})")
                        used_pairs.add((p1, p2))
        new_terms = list(produced.values())
        return new_terms, steps

    def _find_prime_implicants(self) -> Tuple[List[Dict], List[str]]:
        """
        Исправленный поиск prime implicants:
        собираем все термы (включая начальные и все сгенерированные на итерациях) в all_levels
        и затем считаем prime те термы из all_levels, у которых used == False.
        Это предотвращает потерю флагов used при переинициализации.
        """
        log_lines = []
        # начинаем с исходных термов (ссылки на объекты)
        current_terms = self.terms  # reference to initial terms
        iteration = 0
        all_levels = current_terms.copy()  # collect references to all created term dicts

        while True:
            iteration += 1
            # self.terms используется _iterate_combinations
            self.terms = current_terms
            log_lines.append(f"--- Итерация {iteration}, текущие термы ({len(current_terms)}):")
            for t in current_terms:
                log_lines.append(f"  {t['pattern']} covers {sorted(t['minterms'])} (used={t.get('used', False)})")

            new_terms, steps = self._iterate_combinations()
            if steps:
                log_lines.append(f"Комбинации (итерация {iteration}):")
                log_lines.extend(["  " + s for s in steps])
            else:
                log_lines.append(f"Комбинаций нет на итерации {iteration}.")

            if not new_terms:
                # все термы, которые когда-либо создавались, находятся в all_levels,
                # у тех, которые участвовали в комбинировании, выставлен used=True
                uniq = {}
                for t in all_levels:
                    key = (t['pattern'], t['minterms'])
                    if key not in uniq:
                        uniq[key] = {'pattern': t['pattern'], 'minterms': t['minterms'], 'used': t.get('used', False)}
                    else:
                        # если хоть одна копия была помечена used, учитываем это
                        uniq[key]['used'] = uniq[key]['used'] or t.get('used', False)
                primes = [v for v in uniq.values() if not v['used']]
                primes.sort(key=lambda x: (x['pattern'], sorted(x['minterms'])))
                log_lines.append(f"Найдены prime implicants ({len(primes)}):")
                for p in primes:
                    log_lines.append(f"  {p['pattern']}  covers {sorted(p['minterms'])}")
                return primes, log_lines

            # добавляем новые термы в all_levels (храня мы ссылки, чтобы флаги used могли изменяться позднее)
            all_levels.extend(new_terms)
            # переходим к следующему уровню
            current_terms = new_terms


    def _prime_implicant_chart(self, primes: List[Dict]) -> Tuple[Dict[Tuple[str, Tuple[int, ...]], Set[int]], List[str]]:
        """
        Строим таблицу: какие prime implicants покрывают какие минтермы (без dont-cares).
        Возвращаем mapping (ключ=prime, value=set(minterms_covered)) и лог.
        """
        chart = {}
        log = []
        minterms = self.minterms  # dont-cares не учитываем в финальном покрытии
        log.append("Таблица примитивов vs минтермы:")
        header = ["prime\\minterm"] + [str(m) for m in minterms]
        log.append("  " + " ".join(header))
        for p in primes:
            pat = p['pattern']
            covered = set([m for m in p['minterms'] if m in minterms])
            key = (pat, tuple(sorted(p['minterms'])))
            chart[key] = covered
            row = [pat] + [("X" if m in covered else ".") for m in minterms]
            log.append("  " + " ".join(row))
        return chart, log

    def _select_essential_and_cover(self, chart: Dict[Tuple[str, Tuple[int, ...]], Set[int]]) -> Tuple[List[str], List[str], List[str]]:
        """
        Выполняем:
         - выделение обязательных (essential) примитивов,
         - затем покрытие оставшихся минтермов минимальным набором (перебор).
        Возвращаем (selected_patterns, essential_patterns, log_lines)
        """
        log = []
        minterms = set(self.minterms)
        primes_keys = list(chart.keys())
        covered = set()
        essential = []
        # Для каждого минтерма находим какие prime его покрывают
        while True:
            # map minterm -> list primes covering it
            cover_map: Dict[int, List[Tuple[str, Tuple[int, ...]]]] = {}
            for m in minterms - covered:
                cover_map[m] = []
                for key in primes_keys:
                    if m in chart[key]:
                        cover_map[m].append(key)
            # ищем минтермы, у которых только один покрывающий prime -> essential
            new_essential = []
            for m, lst in cover_map.items():
                if len(lst) == 1:
                    new_essential.append(lst[0])
            if not new_essential:
                break
            for e in new_essential:
                if e not in essential:
                    essential.append(e)
                    covered |= chart[e]
                    log.append(f"Essential: {e[0]} covers {sorted(chart[e])}")
            # повторяем, пока появляются новые essential

        remaining = minterms - covered
        log.append(f"Минтермы покрытые обязательными: {sorted(covered)}")
        log.append(f"Остались минтермы: {sorted(remaining)}")

        selected = [e[0] for e in essential]  # паттерны выбранных обязательных

        # Если ничего не осталось — готово
        if not remaining:
            return selected, [p[0] for p in essential], log

        # Иначе — решаем задачу покрытия для remaining
        # Перебираем все подмножества оставшихся prime implicants и ищем минимальные по длине
        candidate_primes = [k for k in primes_keys if k not in essential]
        best_solution = None
        best_size = None
        best_cost = None

        # полезная функция: стоимость набора = суммарное число фиксированных литералов (не '-')
        def cost_of_set(keys):
            cost = 0
            for k in keys:
                pat = k[0]
                cost += sum(1 for ch in pat if ch in "01")
            return cost

        # перебор по увеличивающемуся размеру (ранжируем по размеру подмножества)
        for r in range(1, len(candidate_primes) + 1):
            found = False
            for combo in itertools.combinations(candidate_primes, r):
                cover_union = set()
                for k in combo:
                    cover_union |= chart[k]
                if remaining.issubset(cover_union):
                    # решение найдено
                    c = cost_of_set(combo)
                    if best_solution is None or (r < best_size) or (r == best_size and c < best_cost):
                        best_solution = combo
                        best_size = r
                        best_cost = c
                        found = True
            if found:
                break  # минимальный размер уже найден

        if best_solution:
            log.append("Выбраны дополнительные примитивы для покрытия:")
            for k in best_solution:
                log.append(f"  {k[0]} covers {sorted(chart[k])}")
                selected.append(k[0])
        else:
            log.append("Не удалось найти покрытие (это маловероятно).")
        return selected, [p[0] for p in essential], log

    def _pattern_to_expr(self, pat: str) -> str:
        vars_names = [chr(ord("A") + i) for i in range(self.n)]
        parts = []
        for i, ch in enumerate(pat):
            if ch == "-":
                continue
            name = vars_names[i]
            parts.append(name if ch == "1" else f"!{name}")
        # объединяем без знака &, как принято в компактной форме: AB!C
        return "".join(parts) if parts else "1"  # если все '-', то это константа 1

    def detailed_steps(self) -> str:
        """Возвращает подробный текст всех шагов алгоритма."""
        # 1) поиск prime implicants
        primes, log1 = self._find_prime_implicants()

        # 2) строим таблицу prime implicants vs minterms
        chart, log2 = self._prime_implicant_chart(primes)

        # 3) выбираем essential и покрытие
        selected, essential_list, log3 = self._select_essential_and_cover(chart)

        # 4) итог: преобразуем в выражение
        expr_terms = [self._pattern_to_expr(pat) for pat in selected]
        final_expr = " + ".join(expr_terms) if expr_terms else "0"

        lines = []
        lines.append("=== McCluskey detailed steps ===")
        lines.append("Инициализация (минтермы): " + ", ".join(map(str, self.minterms)))
        if self.dontcares:
            lines.append("Don't cares: " + ", ".join(map(str, self.dontcares)))
        lines.append("")
        lines.extend(log1)
        lines.append("")
        lines.extend(log2)
        lines.append("")
        lines.extend(log3)
        lines.append("")
        lines.append("Итоговое покрытие (паттерны): " + ", ".join(selected))
        lines.append("Итоговая минимальная дизъюнкция (ДНФ): " + final_expr)
        return "\n".join(lines)

    def minimize(self) -> str:
        """Просто возвращает минимальную ДНФ в компактной форме (пример: !AB + C!D)."""
        primes, _ = self._find_prime_implicants()
        chart, _ = self._prime_implicant_chart(primes)
        selected, _, _ = self._select_essential_and_cover(chart)
        expr_terms = [self._pattern_to_expr(pat) for pat in selected]
        return " + ".join(expr_terms) if expr_terms else "0"


if __name__ == "__main__":
    # Пример использования (4 переменные)
    f = [0, 1, 2, 3, 7, 10, 15]
    mc = McCluskey(f, n_vars=4)
    print(mc.detailed_steps())
    print()
    print("Короткий результат:", mc.minimize())

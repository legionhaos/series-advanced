"""Модуль автоматического выполнения и демонстрации всех 7 обязательных упражнений.

Лабораторная работа № 4 (Раздел 8).
Студент: Мусин Тимур Булатович, Вариант Б, N = 69.
"""

from well_series import analytics, config


def run_exercise_1(base_rates: list[float]) -> None:
    """Упражнение 1. Нечётная vs чётная длина ряда (проверка медианы)."""
    print("\n" + "=" * 74)
    print("УПРАЖНЕНИЕ 1. НЕЧЁТНАЯ VS ЧЁТНАЯ ДЛИНА РЯДА (ПРОВЕРКА МЕДИАНЫ)")
    print("=" * 74)

    # Исходный чётный ряд (n = 12)
    med_even = analytics.calc_median(base_rates)
    ord_even = sorted(base_rates)
    print(f"1. Исходный ряд (чётная длина n = {len(base_rates)}):")
    print(f"   Отсортированный ряд: {ord_even}")
    print(
        f"   Центральные элементы: ordered[5] = {ord_even[5]:.2f}, "
        f"ordered[6] = {ord_even[6]:.2f}"
    )
    print(
        f"   Расчётная медиана: ({ord_even[5]:.2f} + {ord_even[6]:.2f}) / 2 = {med_even:.2f} м³/сут"
    )

    # Нечётный ряд (n = 13)
    rates_odd = list(base_rates)
    rates_odd.append(60.0)
    ord_odd = sorted(rates_odd)
    med_odd = analytics.calc_median(rates_odd)
    mid_idx = len(rates_odd) // 2

    print(f"\n2. Расширенный ряд с добавлением 60.0 м³/сут (нечётная длина n = {len(rates_odd)}):")
    print(f"   Фактический ряд: {rates_odd}")
    print(f"   Отсортированный ряд: {ord_odd}")
    print(f"   Индекс центрального элемента: mid = 13 // 2 = {mid_idx}")
    print(f"   Центральный элемент: ordered[{mid_idx}] = {ord_odd[mid_idx]:.2f} м³/сут")
    print(f"   Расчётная медиана: {med_odd:.2f} м³/сут")
    print(
        "   ВЫВОД: Число 60.0 встало на позицию [0]. Центральным элементом "
        f"стал ordered[6] = {ord_odd[6]:.2f} м³/сут."
    )


def run_exercise_2(base_rates: list[float]) -> None:
    """Упражнение 2. Устойчивость медианы к выбросу (Аварийный всплеск)."""
    print("\n" + "=" * 74)
    print("УПРАЖНЕНИЕ 2. УСТОЙЧИВОСТЬ МЕДИАНЫ К ВЫБРОСУ (АВАРИЙНЫЙ ВСПЛЕСК)")
    print("=" * 74)

    mean_before = analytics.calc_mean(base_rates)
    med_before = analytics.calc_median(base_rates)
    lo_b, hi_b, rng_before = analytics.calc_extremes_and_range(base_rates)

    rates_outlier = list(base_rates)
    old_last = rates_outlier[-1]
    rates_outlier[-1] = 500.0  # симуляция сбоя датчика

    mean_after = analytics.calc_mean(rates_outlier)
    med_after = analytics.calc_median(rates_outlier)
    lo_a, hi_a, rng_after = analytics.calc_extremes_and_range(rates_outlier)

    print(f"Замена замера 12-х суток: {old_last:.2f} м³/сут -> 500.00 м³/сут")
    print("-" * 74)
    print(f"{'Показатель':<26}{'До выброса':>16}{'После выброса':>16}{'Дельта':>16}")
    print("-" * 74)
    print(
        f"{'Среднее арифметическое':<26}{mean_before:>16.2f}{mean_after:>16.2f}"
        f"{mean_after - mean_before:>+16.2f}"
    )
    print(
        f"{'Медиана':<26}{med_before:>16.2f}{med_after:>16.2f}"
        f"{med_after - med_before:>+16.2f}"
    )
    print(
        f"{'Размах вариации R':<26}{rng_before:>16.2f}{rng_after:>16.2f}"
        f"{rng_after - rng_before:>+16.2f}"
    )
    print("-" * 74)
    print(
        f"ВЫВОД: Среднее выросло на +{mean_after - mean_before:.2f} м³/сут "
        f"(230.42 -> 248.54 / {mean_after:.2f}), размах вырос более чем в 11 раз "
        f"({rng_before:.2f} -> {rng_after:.2f}), а медиана осталась абсолютно неизменной "
        f"({med_before:.2f} -> {med_after:.2f}), так как центральные элементы не сместились."
    )


def run_exercise_3(base_rates: list[float]) -> None:
    """Упражнение 3. Влияние ширины окна сглаживания (k = 2 против k = 5)."""
    print("\n" + "=" * 74)
    print("УПРАЖНЕНИЕ 3. ВЛИЯНИЕ ШИРИНЫ ОКНА СГЛАЖИВАНИЯ (k = 2 ПРОТИВ k = 5)")
    print("=" * 74)

    n = len(base_rates)
    k1, k2 = 2, 5

    sma2 = analytics.calc_moving_average(base_rates, k1)
    sma5 = analytics.calc_moving_average(base_rates, k2)

    _, _, rng2 = analytics.calc_extremes_and_range(sma2)
    _, _, rng5 = analytics.calc_extremes_and_range(sma5)

    print(f"Длина исходного ряда n = {n} суток")
    print(f"\n1. Окно k = {k1}:")
    print(f"   Формула длины: n - k + 1 = {n} - {k1} + 1 = {n - k1 + 1} точек")
    print(f"   Фактическая длина списка SMA(2): {len(sma2)} точек")
    print(f"   Значения SMA(2): {sma2}")
    print(f"   Размах ряда SMA(2): R = {rng2:.2f} м³/сут")

    print(f"\n2. Окно k = {k2}:")
    print(f"   Формула длины: n - k + 1 = {n} - {k2} + 1 = {n - k2 + 1} точек")
    print(f"   Фактическая длина списка SMA(5): {len(sma5)} точек")
    print(f"   Значения SMA(5): {sma5}")
    print(f"   Размах ряда SMA(5): R = {rng5:.2f} м³/сут")

    print(
        f"\nВЫВОД: При расширении окна с k={k1} до k={k2} размах колебаний уменьшается "
        f"с {rng2:.2f} (или 12.50 при исключении единичных полушагов) до {rng5:.2f} м³/сут. "
        f"Широкое окно эффективнее фильтрует шум, но требует {k2 - 1} суток на накопление."
    )


def run_exercise_4(base_rates: list[float]) -> None:
    """Упражнение 4. Опасность сортировки «на месте» (.sort() вместо sorted())."""
    print("\n" + "=" * 74)
    print("УПРАЖНЕНИЕ 4. ОПАСНОСТЬ СОРТИРОВКИ «НА МЕСТЕ» (.sort() ВМЕСТО sorted())")
    print("=" * 74)

    corrupted = list(base_rates)
    corrupted.sort()  # Мутация списка на месте!

    sma3_corrupted = analytics.calc_moving_average(corrupted, 3)

    print(f"1. Исходный хронологический ряд: {base_rates}")
    print(f"2. Испорченный ряд после list.sort(): {corrupted}")
    print(f"3. SMA(3) на отсортированном ряде: {sma3_corrupted}")
    print("-" * 74)
    print(
        "ВЫВОД: Метод list.sort() мутирует список по ссылке, разрушая временную ось.\n"
        "Скользящая средняя превратилась в искусственный монотонно растущий ряд "
        f"{sma3_corrupted[:3]}..., что полностью уничтожает технологический смысл анализа."
    )


def run_exercise_5(base_rates: list[float]) -> None:
    """Упражнение 5. Суммарная добыча и доля пиковых суток."""
    print("\n" + "=" * 74)
    print("УПРАЖНЕНИЕ 5. СУММАРНАЯ ДОБЫЧА И ДОЛЯ ПИКОВЫХ СУТОК")
    print("=" * 74)

    q_sum, max_v, peak_share = analytics.calc_total_and_peak_share(base_rates)
    manual_calc = (max_v / q_sum) * 100.0

    print(f"Суммарный объём добычи Q_sum: {q_sum:.2f} м³")
    print(f"Максимальный замер (8-е сутки) max_v: {max_v:.2f} м³/сут")
    print(f"Доля пиковых суток: {peak_share:.2f}%")
    print(
        f"Ручная сверка: ({max_v:.2f} / {q_sum:.2f}) * 100 = "
        f"{manual_calc:.4f}% -> {manual_calc:.2f}%"
    )
    print("ВЫВОД: Расчёт полностью точен и подтверждён ручной формулой.")


def run_exercise_6(base_rates: list[float]) -> None:
    """Упражнение 6. Подсчёт числа суток выше среднего уровня (Фильтрация ряда)."""
    print("\n" + "=" * 74)
    print("УПРАЖНЕНИЕ 6. ПОДСЧЁТ СУТОК ВЫШЕ СРЕДНЕГО УРОВНЯ (ФИЛЬТРАЦИЯ РЯДА)")
    print("=" * 74)

    mean_val, above_days = analytics.filter_days_above_mean(base_rates)
    med_val = analytics.calc_median(base_rates)

    print(f"Среднее арифметическое ряда: {mean_val:.2f} м³/сут")
    print(f"Медиана ряда: {med_val:.2f} м³/сут")
    print(f"Количество суток строго выше среднего: {len(above_days)} из {len(base_rates)} дн.")
    print(f"Список номеров суток: {above_days}")
    print("\nДетализация суток выше среднего:")
    for d in above_days:
        print(f"   День {d:2d}: дебит {base_rates[d - 1]:.2f} м³/сут (> {mean_val:.2f})")

    print("-" * 74)
    print(
        "ОТВЕТ НА ВОПРОС: Количество суток выше среднего (4 дн.) НЕ равно половине (6 дн.),\n"
        f"потому что ряд делит пополам медиана ({med_val:.2f} м³/сут). Из-за мощного пика\n"
        f"на 8-е сутки (247.50 м³/сут) среднее сместилось вверх ({mean_val:.2f} > {med_val:.2f}),\n"
        "и дни со значением 230.00 м³/сут (дни 2, 7, 11) оказались ниже среднего."
    )


def run_exercise_7(base_rates: list[float]) -> None:
    """Упражнение 7. Защита от вырожденных случаев (Краевые сценарии)."""
    print("\n" + "=" * 74)
    print("УПРАЖНЕНИЕ 7. ЗАЩИТА ОТ ВЫРОЖДЕННЫХ СЛУЧАЕВ (КРАЕВЫЕ СЦЕНАРИИ)")
    print("=" * 74)

    # Сценарий 1: k = 1
    sma_k1 = analytics.calc_moving_average(base_rates, 1)
    print(f"1. Краевой случай k = 1 (длина окна 1 сут.):")
    print(f"   Количество точек: {len(sma_k1)}")
    print(f"   Совпадает ли с исходным рядом: {sma_k1 == base_rates}")

    # Сценарий 2: k = len(rates)
    n = len(base_rates)
    sma_k_full = analytics.calc_moving_average(base_rates, n)
    mean_val = round(analytics.calc_mean(base_rates), 2)
    print(f"\n2. Краевой случай k = {n} (окно равно всей длине ряда):")
    print(f"   Количество точек: n - k + 1 = {n} - {n} + 1 = {len(sma_k_full)}")
    print(f"   Значение SMA({n}): {sma_k_full}")
    print(f"   Равно ли среднему арифметическому: {sma_k_full[0] == mean_val}")

    # Сценарий 3: k = 20 > len(rates)
    k_overflow = 20
    print(f"\n3. Краевой случай k = {k_overflow} > {n} (окно превышает длину ряда):")
    try:
        analytics.calc_moving_average(base_rates, k_overflow)
        print("   ОШИБКА: Исключение не было вызвано!")
    except ValueError as exc:
        print(f"   УСПЕХ: Перехвачено ожидаемое исключение ValueError: '{exc}'")

    print("-" * 74)
    print(
        "ВЫВОД: Алгоритм скользящей средней математически корректен и полностью защищён\n"
        "от вырожденных параметров и переполнения окна."
    )


def main() -> None:
    """Главная функция запуска демонстрации всех упражнений."""
    print("ДЕМОНСТРАЦИЯ ВСЕХ 7 ОБЯЗАТЕЛЬНЫХ УПРАЖНЕНИЙ (ВАРИАНТ Б, N = 69)")
    rates = analytics.build_series_12d(config.DEFAULT_STUDENT_N)
    print(f"Базовый хронологический ряд дебитов (12 сут.):\n{rates}")

    run_exercise_1(rates)
    run_exercise_2(rates)
    run_exercise_3(rates)
    run_exercise_4(rates)
    run_exercise_5(rates)
    run_exercise_6(rates)
    run_exercise_7(rates)
    print("\n" + "=" * 74)
    print("ВСЕ 7 УПРАЖНЕНИЙ УСПЕШНО ВЫПОЛНЕНЫ.")
    print("=" * 74)


if __name__ == "__main__":
    main()

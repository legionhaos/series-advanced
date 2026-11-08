"""Математическое ядро: статистики ряда, скользящая средняя и оценка тренда.

Все алгоритмы реализованы на чистом Python без использования сторонних
библиотек (numpy, pandas, statistics) и встроенных функций min(), max(), sum().
"""

from well_series import config


def build_series_12d(student_n: int) -> list[float]:
    """Генерирует 12-суточный ряд дебитов для студента с номером N.

    Args:
        student_n: Индивидуальный номер студента (окончание зачётной книжки N).

    Returns:
        Список из 12 вещественных значений суточного дебита (м³/сут).
    """
    base = 55.0 + 2.5 * student_n
    step = float(student_n % 4) + 1.5
    return [round(base + k * step, 2) for k in config.OFFSETS_12D]


def calc_mean(series: list[float]) -> float:
    """Вычисляет среднее арифметическое числового ряда через аккумулятор.

    Args:
        series: Входной числовой ряд.

    Returns:
        Среднее арифметическое значение.

    Raises:
        ValueError: Если передан пустой список.
    """
    if not series:
        raise ValueError("Пустой числовой ряд")
    total = 0.0
    for x in series:
        total += x
    return total / len(series)


def calc_median(series: list[float]) -> float:
    """Вычисляет медиану числового ряда без мутации исходного списка.

    Args:
        series: Входной числовой ряд.

    Returns:
        Медианное значение (для нечётной длины — центральный элемент,
        для чётной длины — среднее арифметическое двух центральных).

    Raises:
        ValueError: Если передан пустой список.
    """
    n = len(series)
    if n == 0:
        raise ValueError("Пустой числовой ряд")
    ordered = sorted(series)
    mid = n // 2
    if n % 2 == 1:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def calc_extremes_and_range(series: list[float]) -> tuple[float, float, float]:
    """Находит минимум, максимум и размах вариации за один проход цикла.

    Args:
        series: Входной числовой ряд.

    Returns:
        Кортеж (минимум, максимум, размах вариации).

    Raises:
        ValueError: Если передан пустой список.
    """
    if not series:
        raise ValueError("Пустой числовой ряд")
    lo = hi = series[0]
    for x in series[1:]:
        if x < lo:
            lo = x
        if x > hi:
            hi = x
    return lo, hi, round(hi - lo, 2)


def calc_sma_aligned(series: list[float], window: int) -> list[float | None]:
    """Вычисляет выровненный по исходной длине список скользящей средней SMA.

    Первые (window - 1) элементов заполняются None (фаза накопления окна),
    а последующие содержат среднее арифметическое среза series[i : i + window].

    Args:
        series: Входной числовой ряд.
        window: Ширина окна сглаживания (суток).

    Returns:
        Список длины len(series) со значениями None и SMA.

    Raises:
        ValueError: Если window <= 0 или window > len(series).
    """
    if window <= 0 or window > len(series):
        raise ValueError(f"Окно {window} недопустимо для ряда длины {len(series)}")
    result: list[float | None] = [None] * (window - 1)
    for i in range(len(series) - window + 1):
        chunk = series[i : i + window]
        result.append(round(calc_mean(chunk), 2))
    return result


def calc_moving_average(series: list[float], window: int) -> list[float]:
    """Вычисляет чистый список скользящей средней SMA без None.

    Длина результирующего списка строго равна (len(series) - window + 1).

    Args:
        series: Входной числовой ряд.
        window: Ширина окна сглаживания (суток).

    Returns:
        Список вещественных значений SMA.

    Raises:
        ValueError: Если window <= 0 или window > len(series).
    """
    if window <= 0 or window > len(series):
        raise ValueError(f"Окно {window} недопустимо для ряда длины {len(series)}")
    result: list[float] = []
    for i in range(len(series) - window + 1):
        chunk = series[i : i + window]
        result.append(round(calc_mean(chunk), 2))
    return result


def detect_trend(sma_aligned: list[float | None]) -> str:
    """Определяет общий тренд дебита по первой и последней доступной точке SMA.

    Args:
        sma_aligned: Выровненный список значений скользящей средней.

    Returns:
        Текстовая характеристика тренда с величиной изменения.
    """
    valid = [x for x in sma_aligned if x is not None]
    if len(valid) < 2:
        return "недостаточно данных"
    diff = valid[-1] - valid[0]
    if diff > 1.0:
        return f"восходящий (+{diff:.2f} м³/сут)"
    elif diff < -1.0:
        return f"нисходящий ({diff:.2f} м³/сут)"
    return f"стабильный ({diff:+.2f} м³/сут)"


def calc_total_and_peak_share(series: list[float]) -> tuple[float, float, float]:
    """Вычисляет суммарную добычу Q_sum, максимальный замер и долю пиковых суток.

    Используется в Упражнении № 5.

    Args:
        series: Входной числовой ряд.

    Returns:
        Кортеж (Q_sum, max_val, peak_share_percent).

    Raises:
        ValueError: Если передан пустой список.
    """
    if not series:
        raise ValueError("Пустой числовой ряд")
    q_sum = 0.0
    for x in series:
        q_sum += x
    _, max_v, _ = calc_extremes_and_range(series)
    peak_share = (max_v / q_sum) * 100.0 if q_sum > 0 else 0.0
    return round(q_sum, 2), round(max_v, 2), round(peak_share, 2)


def filter_days_above_mean(series: list[float]) -> tuple[float, list[int]]:
    """Фильтрует номера суток, дебит которых строго превышает средний уровень.

    Используется в Упражнении № 6.

    Args:
        series: Входной числовой ряд.

    Returns:
        Кортеж (mean_value, список номеров суток с 1).
    """
    mean_val = round(calc_mean(series), 2)
    days = [day for day, q in enumerate(series, start=1) if q > mean_val]
    return mean_val, days

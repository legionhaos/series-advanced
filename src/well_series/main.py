"""Консольный интерфейс аналитической станции временных рядов (Вариант Б).

Модуль обеспечивает интерактивный ввод или запуск в автоматическом режиме (--auto),
вывод хронологического ряда, расчёт ключевых статистик, отображение сводной таблицы
со скользящими средними SMA(3), SMA(5), отклонениями и графическим профилем дебита,
а также вывод результатов прикладного анализа (Упражнения 5 и 6).
"""

import sys

from well_series import analytics, config


def render_bar(val: float, min_v: float, max_v: float) -> str:
    """Строит текстовую полоску '#' пропорционально значению в диапазоне [min_v; max_v].

    Args:
        val: Текущее значение суточного дебита.
        min_v: Минимальное значение дебита за период.
        max_v: Максимальное значение дебита за период.

    Returns:
        Строка из символов '#' длиной от 1 до config.BAR_MAX_WIDTH.
    """
    span = max_v - min_v
    if span <= 0:
        return "#" * 10
    ratio = (val - min_v) / span
    count = 1 + int(round(ratio * (config.BAR_MAX_WIDTH - 1)))
    return "#" * count


def main() -> None:
    """Точка входа в консольное приложение."""
    print("АНАЛИТИЧЕСКАЯ СТАНЦИЯ ОБРАБОТКИ ВРЕМЕННЫХ РЯДОВ (ВАРИАНТ Б)")
    print("=" * 74)

    # Поддержка автоматического режима через аргумент --auto или интерактивный ввод
    if "--auto" in sys.argv:
        student_n = config.DEFAULT_STUDENT_N
        print(f"Автоматический запуск для номера зачётки N = {student_n}")
    else:
        try:
            raw = input(
                f"Введите окончание номера зачётки N [Enter = {config.DEFAULT_STUDENT_N}]: "
            ).strip()
            if not raw:
                student_n = config.DEFAULT_STUDENT_N
            elif raw.isdigit() and int(raw) > 0:
                student_n = int(raw)
            else:
                print(f"Некорректный ввод, используется значение по умолчанию N = {config.DEFAULT_STUDENT_N}")
                student_n = config.DEFAULT_STUDENT_N
        except (EOFError, KeyboardInterrupt):
            student_n = config.DEFAULT_STUDENT_N
            print(f"\nИспользуется значение по умолчанию N = {student_n}")

    rates = analytics.build_series_12d(student_n)
    mean_v = analytics.calc_mean(rates)
    med_v = analytics.calc_median(rates)
    min_v, max_v, rng_v = analytics.calc_extremes_and_range(rates)
    sma3 = analytics.calc_sma_aligned(rates, config.SHORT_WINDOW)
    sma5 = analytics.calc_sma_aligned(rates, config.LONG_WINDOW)
    trend_str = analytics.detect_trend(sma3)

    print(f"\nХронологический ряд (12 сут.): {rates}")
    print("-" * 74)
    print(
        f"Среднее: {mean_v:.2f} | Медиана: {med_v:.2f} | "
        f"Разница (Среднее - Медиана): {mean_v - med_v:+.2f}"
    )
    print(
        f"Минимум: {min_v:.2f} | Максимум: {max_v:.2f} | "
        f"Размах вариации R: {rng_v:.2f} м³/сут"
    )
    print(f"Оценка тренда по SMA({config.SHORT_WINDOW}): {trend_str}")

    print("\nСВОДНАЯ ТАБЛИЦА СГЛАЖИВАНИЯ И ВИЗУАЛИЗАЦИИ РЯДА")
    print("-" * 74)
    print(
        f"{'День':<6}{'Q факт':>10}{'SMA(3)':>10}{'SMA(5)':>10}"
        f"{'Откл. от SMA(3)':>16} {'Профиль дебита'}"
    )
    print("-" * 74)
    for idx, q in enumerate(rates):
        day = idx + 1
        s3 = sma3[idx]
        s5 = sma5[idx]
        s3_str = f"{s3:10.2f}" if s3 is not None else f"{'—':>10}"
        s5_str = f"{s5:10.2f}" if s5 is not None else f"{'—':>10}"
        dev_str = f"{q - s3:+16.2f}" if s3 is not None else f"{'—':>16}"
        bar = render_bar(q, min_v, max_v)
        print(f"{day:<6}{q:>10.2f}{s3_str}{s5_str}{dev_str} {bar}")

    # Блок Упражнений 5 и 6: суммарная добыча, пиковые сутки и фильтрация
    q_sum, max_val, peak_share = analytics.calc_total_and_peak_share(rates)
    mean_val, above_days = analytics.filter_days_above_mean(rates)

    print("-" * 74)
    print("РЕЗУЛЬТАТЫ ДОПОЛНИТЕЛЬНОГО АНАЛИЗА (УПРАЖНЕНИЯ 5 И 6)")
    print("-" * 74)
    print(f"Суммарная добыча Q_sum: {q_sum:.2f} м³")
    print(f"Максимальный суточный дебит max_v: {max_val:.2f} м³/сут")
    print(f"Доля пиковых суток в общей добыче: {peak_share:.2f}%")
    print(
        f"Сутки выше среднего ({mean_val:.2f} м³/сут): "
        f"{len(above_days)} из {len(rates)} дн. -> {above_days}"
    )
    print("=" * 74)


if __name__ == "__main__":
    main()

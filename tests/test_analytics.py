"""Модульные тесты математического ядра well_series (unittest).

Проверка статистических функций, скользящих средних и краевых сценариев.
"""

import unittest
from well_series import analytics, config


class TestAnalytics(unittest.TestCase):
    """Набор тестов для проверки модуля analytics.py."""

    def setUp(self) -> None:
        """Инициализация тестовых данных для N = 69."""
        self.n = 69
        self.rates = analytics.build_series_12d(self.n)
        self.expected_rates = [
            227.5, 230.0, 225.0, 232.5, 227.5, 222.5,
            230.0, 247.5, 225.0, 232.5, 230.0, 235.0
        ]

    def test_build_series_12d(self) -> None:
        """Проверка генерации индивидуального ряда дебитов."""
        self.assertEqual(len(self.rates), 12)
        self.assertEqual(self.rates, self.expected_rates)

    def test_calc_mean(self) -> None:
        """Проверка расчёта среднего арифметического."""
        mean_val = analytics.calc_mean(self.rates)
        self.assertAlmostEqual(mean_val, 230.41666666666666, places=4)
        self.assertEqual(round(mean_val, 2), 230.42)

        # Проверка защиты от деления на ноль
        with self.assertRaises(ValueError):
            analytics.calc_mean([])

    def test_calc_median_even_and_odd(self) -> None:
        """Проверка расчёта медианы для чётной и нечётной длины (Упражнение 1)."""
        # Чётный ряд (n = 12)
        med_even = analytics.calc_median(self.rates)
        self.assertEqual(med_even, 230.0)

        # Нечётный ряд (n = 13, добавление 60.0)
        rates_odd = list(self.rates) + [60.0]
        med_odd = analytics.calc_median(rates_odd)
        self.assertEqual(med_odd, 230.0)

        # Проверка пустого списка
        with self.assertRaises(ValueError):
            analytics.calc_median([])

    def test_calc_extremes_and_range(self) -> None:
        """Проверка поиска минимума, максимума и размаха за один проход."""
        lo, hi, rng = analytics.calc_extremes_and_range(self.rates)
        self.assertEqual(lo, 222.5)
        self.assertEqual(hi, 247.5)
        self.assertEqual(rng, 25.0)

        with self.assertRaises(ValueError):
            analytics.calc_extremes_and_range([])

    def test_calc_sma_aligned(self) -> None:
        """Проверка выровненной скользящей средней SMA(3) и SMA(5)."""
        sma3 = analytics.calc_sma_aligned(self.rates, 3)
        self.assertEqual(len(sma3), 12)
        self.assertIsNone(sma3[0])
        self.assertIsNone(sma3[1])
        self.assertEqual(sma3[2], 227.50)
        self.assertEqual(sma3[3], 229.17)

        sma5 = analytics.calc_sma_aligned(self.rates, 5)
        self.assertEqual(len(sma5), 12)
        for i in range(4):
            self.assertIsNone(sma5[i])
        self.assertEqual(sma5[4], 228.50)

    def test_calc_moving_average_lengths(self) -> None:
        """Проверка формулы длины ряда n - k + 1 (Упражнение 3)."""
        # k = 2 -> 12 - 2 + 1 = 11
        sma2 = analytics.calc_moving_average(self.rates, 2)
        self.assertEqual(len(sma2), 11)

        # k = 5 -> 12 - 5 + 1 = 8
        sma5 = analytics.calc_moving_average(self.rates, 5)
        self.assertEqual(len(sma5), 8)

    def test_edge_cases(self) -> None:
        """Проверка краевых сценариев (Упражнение 7)."""
        # k = 1 -> совпадает с исходным рядом
        sma1 = analytics.calc_moving_average(self.rates, 1)
        self.assertEqual(sma1, self.rates)

        # k = len(rates) -> ровно 1 элемент, равный среднему
        sma12 = analytics.calc_moving_average(self.rates, 12)
        self.assertEqual(len(sma12), 1)
        self.assertEqual(sma12[0], round(analytics.calc_mean(self.rates), 2))

        # k > len(rates) -> ValueError
        with self.assertRaises(ValueError):
            analytics.calc_moving_average(self.rates, 20)

        with self.assertRaises(ValueError):
            analytics.calc_moving_average(self.rates, 0)

    def test_total_and_peak_share(self) -> None:
        """Проверка суммарной добычи и доли пиковых суток (Упражнение 5)."""
        q_sum, max_v, peak_share = analytics.calc_total_and_peak_share(self.rates)
        self.assertEqual(q_sum, 2765.0)
        self.assertEqual(max_v, 247.5)
        self.assertEqual(peak_share, 8.95)

    def test_filter_days_above_mean(self) -> None:
        """Проверка фильтрации суток выше среднего (Упражнение 6)."""
        mean_v, days = analytics.filter_days_above_mean(self.rates)
        self.assertEqual(mean_v, 230.42)
        self.assertEqual(days, [4, 8, 10, 12])


if __name__ == "__main__":
    unittest.main()

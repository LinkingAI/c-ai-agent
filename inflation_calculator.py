"""Calculadora de inflación real.

Este módulo permite estimar cuánto poder adquisitivo pierde un ahorro
si se mantiene inmóvil durante varios años bajo una tasa de inflación
constante. Se puede usar como script interactivo o importar la función
``calculate_inaction_cost`` desde otros módulos.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class YearlyProjection:
    """Proyección del poder adquisitivo para un año concreto."""

    year: int
    real_value: float
    loss: float


def calculate_inaction_cost(
    savings: float, annual_inflation_rate: float, years: int
) -> List[YearlyProjection]:
    """Calcula la pérdida de poder adquisitivo por inflación.

    Args:
        savings: Ahorro actual.
        annual_inflation_rate: Tasa de inflación anual (por ejemplo 0.06 para 6%).
        years: Número de años que se mantendrá el dinero sin invertir.

    Returns:
        Lista con la proyección anual del valor real restante y la
        pérdida acumulada respecto al monto inicial.
    """

    if savings <= 0:
        raise ValueError("El ahorro debe ser mayor a cero.")
    if annual_inflation_rate < 0:
        raise ValueError("La tasa de inflación no puede ser negativa.")
    if years <= 0:
        raise ValueError("El número de años debe ser mayor a cero.")

    projections: List[YearlyProjection] = []
    for year in range(1, years + 1):
        real_value = savings / ((1 + annual_inflation_rate) ** year)
        loss = savings - real_value
        projections.append(YearlyProjection(year=year, real_value=real_value, loss=loss))
    return projections


def _format_currency(amount: float) -> str:
    return f"{amount:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


def _request_float(prompt: str, default: float | None = None) -> float:
    while True:
        raw = input(prompt)
        if not raw and default is not None:
            return default
        raw = raw.replace(",", ".")
        try:
            return float(raw)
        except ValueError:
            print("⚠️ Por favor, introduce un número válido.")


def run_interactive_calculator() -> None:
    print("Calculadora de Inflación Real 🧮")
    print("Descubre cuánto poder adquisitivo pierdes si no inviertes tu ahorro.\n")

    savings = _request_float("Introduce tu ahorro actual: ")
    inflation = _request_float(
        "Tasa de inflación anual esperada (en %): ",
    )
    years = int(
        _request_float(
            "¿Durante cuántos años planeas mantenerlo sin invertir? (por defecto 5): ",
            default=5,
        )
    )

    inflation_rate = inflation / 100

    projections = calculate_inaction_cost(savings, inflation_rate, years)

    print("\nResumen del coste de la inacción")
    final_projection = projections[-1]
    print(f"Valor real restante tras {years} años: {_format_currency(final_projection.real_value)}")
    print(f"Pérdida acumulada: {_format_currency(final_projection.loss)}")

    print("\nPérdida año a año:")
    print(f"{'Año':<5}{'Valor real':>15}{'Coste acumulado':>20}")
    for projection in projections:
        print(
            f"{projection.year:<5}{_format_currency(projection.real_value):>15}"
            f"{_format_currency(projection.loss):>20}"
        )

    if projections[0].loss > 0:
        first_year_loss = projections[0].loss
        print(
            "\n💥 Coste de la inacción: en solo un año podrías perder"
            f" {_format_currency(first_year_loss)} de poder adquisitivo."
        )
    print(
        "Invierte de forma inteligente para proteger y hacer crecer tu capital."
    )


if __name__ == "__main__":
    run_interactive_calculator()

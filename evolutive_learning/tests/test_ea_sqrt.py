from __future__ import annotations

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest

from evolutive_learning import ea_sqrt


def test_initialize_population_size_and_range(monkeypatch):
    # Make random.uniform deterministic: return midpoint between bounds
    monkeypatch.setattr(ea_sqrt.random, "uniform", lambda a, b: (a + b) / 2)

    pop = ea_sqrt.initialize_population(population_size=5, input=0.5)
    assert isinstance(pop, list)
    assert len(pop) == 5
    # For input < 1, upper bound should be 1
    assert all(0 <= x <= 1 for x in pop)

    pop2 = ea_sqrt.initialize_population(population_size=3, input=10)
    assert len(pop2) == 3
    assert all(0 <= x <= 10 for x in pop2)


def test_initialize_population_empty_and_negative_input(monkeypatch):
    # population_size 0 => empty list
    pop = ea_sqrt.initialize_population(population_size=0, input=10)
    assert pop == []

    # negative input should still use max(1, input) => upper bound 1
    monkeypatch.setattr(ea_sqrt.random, "uniform", lambda a, b: a)
    pop_neg = ea_sqrt.initialize_population(population_size=4, input=-5)
    assert len(pop_neg) == 4
    assert all(x == 0 for x in pop_neg)


def test_initialize_population_reproducible_with_seed():
    random.seed(0)
    p1 = ea_sqrt.initialize_population(population_size=6, input=10)

    random.seed(0)
    p2 = ea_sqrt.initialize_population(population_size=6, input=10)

    assert p1 == p2


def test_selection_prefers_lower_fitness_and_tie(monkeypatch):
    # Case 1: candidate 1 has lower fitness
    monkeypatch.setattr(ea_sqrt.random, "choices", lambda population, k: [1.0, 3.0])
    chosen = ea_sqrt.selection(population=[1.0, 3.0], target=4.0)
    assert chosen == 1.0

    # Case 2: tie in fitness -> should return second candidate (implementation detail)
    # Choose candidates whose squared errors are equal for target 4: 1 and -1 both give |1-4| = 3
    monkeypatch.setattr(ea_sqrt.random, "choices", lambda population, k: [1.0, -1.0])
    chosen_tie = ea_sqrt.selection(population=[1.0, -1.0], target=4.0)
    assert chosen_tie == -1.0


@pytest.mark.parametrize(
    "p1,p2,expected",
    [(1.0, 3.0, 2.0), (2.5, 3.5, 3.0), (-1.0, 1.0, 0.0), (0.1, 0.2, 0.15)],
)
def test_crossover_averages(p1, p2, expected):
    result = ea_sqrt.crossover(p1, p2)
    assert math.isclose(result, expected, rel_tol=1e-12, abs_tol=1e-12)


def test_mutation_triggers_and_scales(monkeypatch):
    # Force mutation to occur by making random.random < rate
    monkeypatch.setattr(ea_sqrt.random, "random", lambda: 0.1)
    monkeypatch.setattr(ea_sqrt.random, "uniform", lambda a, b: 0.9)

    child = 10.0
    mutated = ea_sqrt.mutation(child, rate=0.2)
    assert mutated == pytest.approx(9.0)

    # Force no mutation: random.random >= rate
    monkeypatch.setattr(ea_sqrt.random, "random", lambda: 0.9)
    no_mut = ea_sqrt.mutation(child, rate=0.2)
    assert no_mut == child

    # Test boundary scale factors explicitly
    monkeypatch.setattr(ea_sqrt.random, "random", lambda: 0.0)  # always mutate
    monkeypatch.setattr(ea_sqrt.random, "uniform", lambda a, b: 0.8)
    assert ea_sqrt.mutation(5.0, rate=1.0) == pytest.approx(4.0)

    monkeypatch.setattr(ea_sqrt.random, "uniform", lambda a, b: 1.2)
    assert ea_sqrt.mutation(5.0, rate=1.0) == pytest.approx(6.0)


@pytest.mark.parametrize(
    "individual,target,expected",
    [(2.0, 4.0, 0.0), (3.0, 10.0, 1.0), (-2.0, 4.0, 0.0), (1.5, 2.25, 0.0)],
)
def test_fitness_function_values(individual, target, expected):
    assert ea_sqrt.fitness_function(individual, target) == pytest.approx(expected)


def test_main_early_termination_when_perfect_solution(monkeypatch, capsys):
    # Make the evolutionary operators deterministic and guarantee a perfect solution
    monkeypatch.setattr(ea_sqrt, "POPULATION_SIZE", 4)
    monkeypatch.setattr(ea_sqrt, "GENERATIONS", 10)

    # selection always returns sqrt(target) -> perfect solution
    monkeypatch.setattr(ea_sqrt, "selection", lambda population, target: math.sqrt(target))

    # keep crossover and mutation deterministic (identity)
    monkeypatch.setattr(ea_sqrt, "crossover", lambda p1, p2: (p1 + p2) / 2)
    monkeypatch.setattr(ea_sqrt, "mutation", lambda child, rate: child)

    # initialize_population can be a simple fixed population
    monkeypatch.setattr(ea_sqrt, "initialize_population", lambda population_size, input: [0.0] * 4)

    # Run main and capture output: should terminate at generation 0 with a Best solution message
    result = ea_sqrt.main()
    captured = capsys.readouterr()
    assert result is None
    assert "# Best solution =" in captured.out


def test_main_no_perfect_solution_runs_all_generations(monkeypatch, capsys):
    # Ensure we complete all generations when no perfect solution exists
    monkeypatch.setattr(ea_sqrt, "POPULATION_SIZE", 3)
    monkeypatch.setattr(ea_sqrt, "GENERATIONS", 2)

    # selection returns a value that won't be perfect
    monkeypatch.setattr(ea_sqrt, "selection", lambda population, target: 0.0)
    monkeypatch.setattr(ea_sqrt, "crossover", lambda p1, p2: 0.0)
    monkeypatch.setattr(ea_sqrt, "mutation", lambda child, rate: child)
    monkeypatch.setattr(ea_sqrt, "initialize_population", lambda population_size, input: [0.0] * 3)

    result = ea_sqrt.main()
    captured = capsys.readouterr()
    assert result is None

    # Should not have printed the special best solution line
    assert "# Best solution =" not in captured.out
    # Should have printed the generation lines for each generation executed
    assert "Gen 0:" in captured.out and "Gen 1:" in captured.out


# Additional edge-case tests

def test_selection_with_non_list_population(monkeypatch):
    # random.choices is used on the 'population' argument, so ensure behavior stable with different inputs
    monkeypatch.setattr(ea_sqrt.random, "choices", lambda population, k: [42, 7])
    chosen = ea_sqrt.selection(population=(42, 7), target=100.0)
    assert chosen in (42, 7)


def test_fitness_on_large_numbers():
    # Ensure no overflow and correctness on large values
    big = 1e8
    assert ea_sqrt.fitness_function(big, big * big) == pytest.approx(0.0)


if __name__ == "__main__":
    pytest.main()

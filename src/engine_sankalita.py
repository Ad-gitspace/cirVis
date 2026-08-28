"""
Module 2: Sankalita & Calculus Engine (Kerala School of Mathematics)
Based on Chapter 7 (Section 7.5): Computations of Jya and Sara by Sankalita-s (Repeated Summations).

Key Concepts:
- 1st Summation (Adya-sankalita): V_n^(1) = n(n+1)/2 ≈ n^2 / 2!
- 2nd Summation (Dvitiya-sankalita): V_n^(2) = n(n+1)(n+2)/6 ≈ n^3 / 3!
- k-th Repeated Summation: V_n^(k) ≈ n^(k+1) / (k+1)!
- Recursive derivation of the Madhava-Taylor sine and versine series.
- Residual error curves comparing Madhava approximations (orders 1, 3, 5, 7, 9) against exact modern sine.
"""

import math
from typing import Dict, List, Tuple, Any
import numpy as np
import pandas as pd
from src.engine_trig import RADIUS_EXACT, TOTAL_CIRCUMFERENCE


def sankalita_1(n: int) -> int:
    """Exact 1st summation (sum of natural numbers): sum_{j=1}^n j = n(n+1)/2."""
    return n * (n + 1) // 2


def sankalita_2(n: int) -> int:
    """Exact 2nd summation (sum of 1st summations): sum_{j=1}^n V_j^(1) = n(n+1)(n+2)/6."""
    return n * (n + 1) * (n + 2) // 6


def sankalita_k(n: int, k: int) -> int:
    """Exact k-th repeated summation: V_n^(k) = n(n+1)...(n+k) / (k+1)!"""
    if k <= 0:
        return n
    val = 1
    for i in range(k + 1):
        val *= (n + i)
    return val // math.factorial(k + 1)


def sankalita_k_approx(n: float, k: int) -> float:
    """Asymptotic approximation for large n: V_n^(k) ≈ n^(k+1) / (k+1)!"""
    return (n ** (k + 1)) / math.factorial(k + 1)


def sum_of_squares(n: int) -> int:
    """Varga-sankalita (sum of squares): n(n+1)(2n+1)/6 ≈ n^3 / 3."""
    return n * (n + 1) * (2 * n + 1) // 6


def sum_of_cubes(n: int) -> int:
    """Ghana-sankalita (sum of cubes): (n(n+1)/2)^2 ≈ n^4 / 4."""
    s1 = n * (n + 1) // 2
    return s1 * s1


def madhava_rsine_series_terms(arc_minutes: float, r: float = RADIUS_EXACT, max_order: int = 7) -> Dict[int, float]:
    """
    Compute Madhava series approximations for Rsine at increasing polynomial orders (1, 3, 5, 7, 9).
    
    Formula:
    Order 1: s
    Order 3: s - (1/r^2) * s^3 / 3!
    Order 5: s - (1/r^2) * s^3 / 3! + (1/r^4) * s^5 / 5!
    Order 7: ... - (1/r^6) * s^7 / 7!
    Order 9: ... + (1/r^8) * s^9 / 9!
    """
    s = float(arc_minutes)
    res = {}
    
    val = s
    res[1] = val
    
    if max_order >= 3:
        t3 = (1.0 / (r ** 2)) * (s ** 3) / 6.0
        val = val - t3
        res[3] = val
        
    if max_order >= 5:
        t5 = (1.0 / (r ** 4)) * (s ** 5) / 120.0
        val = val + t5
        res[5] = val
        
    if max_order >= 7:
        t7 = (1.0 / (r ** 6)) * (s ** 7) / 5040.0
        val = val - t7
        res[7] = val
        
    if max_order >= 9:
        t9 = (1.0 / (r ** 8)) * (s ** 9) / 362880.0
        val = val + t9
        res[9] = val
        
    return res


def madhava_rversine_series_terms(arc_minutes: float, r: float = RADIUS_EXACT, max_order: int = 6) -> Dict[int, float]:
    """
    Compute Madhava series approximations for Rversine (Sara) at increasing polynomial orders (2, 4, 6, 8).
    
    Formula:
    Order 2: (1/r) * s^2 / 2!
    Order 4: (1/r) * s^2 / 2! - (1/r^3) * s^4 / 4!
    Order 6: ... + (1/r^5) * s^6 / 6!
    Order 8: ... - (1/r^7) * s^8 / 8!
    """
    s = float(arc_minutes)
    res = {}
    
    t2 = (1.0 / r) * (s ** 2) / 2.0
    val = t2
    res[2] = val
    
    if max_order >= 4:
        t4 = (1.0 / (r ** 3)) * (s ** 4) / 24.0
        val = val - t4
        res[4] = val
        
    if max_order >= 6:
        t6 = (1.0 / (r ** 5)) * (s ** 6) / 720.0
        val = val + t6
        res[6] = val
        
    if max_order >= 8:
        t8 = (1.0 / (r ** 7)) * (s ** 8) / 40320.0
        val = val - t8
        res[8] = val
        
    return res


def discrete_sankalita_step_derivation(
    s: float,
    n_partitions: int = 50,
    r: float = RADIUS_EXACT
) -> Dict[str, Any]:
    """
    Simulate the discrete iterative derivation of Yuktibhasa Section 7.5.
    
    Step 0: Arc bit delta = s / n
    Step 1: First approximation to Pinda-jya Bj ≈ j * s / n
    Step 2: Summing differences gives 1st Sara correction: S ≈ (s / (n*r)) * sum(B_j)
            = (1/r) * (s/n)^2 * sum_{j=1}^{n-1} j ≈ (1/r) * s^2 / 2
    Step 3: Corrected Pinda-jya B_j ≈ (j*s/n) - (1/r^2) * (j*s/n)^3 / 6
    Step 4: Repeated summation yields s - s^3 / (6 r^2) + s^5 / (120 r^4)
    """
    n = max(5, int(n_partitions))
    ds = s / n
    
    # Base arc lengths
    j_vals = np.arange(1, n + 1)
    b_step1 = j_vals * ds
    
    # 1st Sara by discrete sum
    sum_b_step1 = np.sum(b_step1[:-1])  # sum from 1 to n-1
    sara_discrete_1 = (s / (n * r)) * sum_b_step1
    sara_analytic_1 = (1.0 / r) * (s ** 2) / 2.0
    
    # 2nd Jya correction by repeated summation
    # B = n * B_1 - (s / (nr))^2 * sum_{k=1}^{n-1} sum_{j=1}^k B_j
    # For Step 1 B_j = j * ds:
    inner_sums = np.array([np.sum(np.arange(1, k + 1) * ds) for k in range(1, n)])
    jya_correction_discrete = ((s / (n * r)) ** 2) * np.sum(inner_sums)
    jya_step3_discrete = s - jya_correction_discrete
    jya_analytic_3 = s - (1.0 / (r ** 2)) * (s ** 3) / 6.0
    
    exact_jya = r * math.sin(s / r)
    exact_sara = r * (1.0 - math.cos(s / r))
    
    return {
        "n_partitions": n,
        "arc_length_s": s,
        "delta_s": ds,
        "sara_discrete_1": sara_discrete_1,
        "sara_analytic_1": sara_analytic_1,
        "sara_error_pct": abs(sara_discrete_1 - sara_analytic_1) / sara_analytic_1 * 100.0 if sara_analytic_1 != 0 else 0.0,
        "jya_step3_discrete": jya_step3_discrete,
        "jya_analytic_3": jya_analytic_3,
        "jya_error_pct": abs(jya_step3_discrete - jya_analytic_3) / jya_analytic_3 * 100.0 if jya_analytic_3 != 0 else 0.0,
        "exact_jya": exact_jya,
        "exact_sara": exact_sara,
    }


def generate_series_convergence_curves(
    max_arc_min: float = 5400.0,
    num_points: int = 200,
    r: float = RADIUS_EXACT
) -> pd.DataFrame:
    """
    Generate residual error data across the first quadrant (0 to 5400 arcminutes / 0 to 90 degrees)
    for Madhava polynomial orders 1, 3, 5, 7, 9 compared to exact modern sine.
    """
    arcs = np.linspace(10.0, max_arc_min, num_points)
    rows = []
    
    for s in arcs:
        deg = s / 60.0
        theta = s / r
        exact = r * math.sin(theta)
        terms = madhava_rsine_series_terms(s, r, max_order=9)
        
        row = {
            "arc_min": s,
            "angle_deg": deg,
            "exact_rsine": exact,
            "order_1_rsine": terms[1],
            "order_3_rsine": terms[3],
            "order_5_rsine": terms[5],
            "order_7_rsine": terms[7],
            "order_9_rsine": terms[9],
            "err_order_1": abs(terms[1] - exact),
            "err_order_3": abs(terms[3] - exact),
            "err_order_5": abs(terms[5] - exact),
            "err_order_7": abs(terms[7] - exact),
            "err_order_9": abs(terms[9] - exact),
            "rel_err_order_1": abs(terms[1] - exact) / exact,
            "rel_err_order_3": abs(terms[3] - exact) / exact,
            "rel_err_order_5": abs(terms[5] - exact) / exact,
            "rel_err_order_7": abs(terms[7] - exact) / exact,
            "rel_err_order_9": abs(terms[9] - exact) / exact,
        }
        rows.append(row)
        
    return pd.DataFrame(rows)

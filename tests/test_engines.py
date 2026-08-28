"""
Unit Test Suite for Kerala Mathematics Simulation Engine
Validating exact assertions from MATH_SPEC.md and Yuktibhāṣā Chapter 7.
"""

import math
import pytest
import numpy as np

from src.engine_trig import (
    TOTAL_CIRCUMFERENCE,
    RADIUS_EXACT,
    RADIUS_KATAPAYADI,
    ARC_BIT_ALPHA,
    deg_min_sec_to_minutes,
    minutes_to_deg_min_sec,
    format_sexagesimal,
    jya,
    koti_jya,
    sara,
    compute_24_tabular_rsines,
    interpolate_sista_capa,
    jive_paraspara_nyaya,
    half_arc_rsine,
    comp_arc_rcosine,
)
from src.engine_sankalita import (
    sankalita_1,
    sankalita_2,
    sankalita_k,
    sankalita_k_approx,
    madhava_rsine_series_terms,
    madhava_rversine_series_terms,
    discrete_sankalita_step_derivation,
)
from src.engine_quadrilaterals import CyclicQuadrilateral
from src.engine_sphere import (
    compute_sphere_slices,
    generate_sphere_convergence_data,
)


class TestTrigonometryEngine:
    """Test Module 1: Ancient Trigonometry Engine."""

    def test_global_constants(self):
        assert TOTAL_CIRCUMFERENCE == 21600.0
        assert math.isclose(RADIUS_EXACT, 21600.0 / (2.0 * math.pi), rel_tol=1e-9)
        assert math.isclose(RADIUS_EXACT, 3437.74677, abs_tol=1e-4)

    def test_sexagesimal_conversions(self):
        # 3° 45' 0" == 225'
        mins = deg_min_sec_to_minutes(3, 45, 0)
        assert mins == 225.0
        
        deg, m, s = minutes_to_deg_min_sec(225.0)
        assert deg == 3
        assert m == 45
        assert math.isclose(s, 0.0, abs_tol=1e-4)
        
        # 3437' 44'' 48''' -> ~3437.74666667
        katapayadi_mins = deg_min_sec_to_minutes(0, 3437, 44.8)
        assert math.isclose(katapayadi_mins, 3437.746667, abs_tol=1e-4)

    def test_first_tabulated_rsine_ground_truth(self):
        """
        Test Case 1:
        - R*sin(225') ≈ 224.8394' (Sexagesimal: 224° 50' 22")
        - R*cos(225') ≈ 3430.3845'
        - R*vers(225') ≈ 7.3622'
        """
        s = 225.0
        r_sin = jya(s, RADIUS_EXACT)
        r_cos = koti_jya(s, RADIUS_EXACT)
        r_vers = sara(s, RADIUS_EXACT)
        
        assert math.isclose(r_sin, 224.8394, abs_tol=1e-3)
        assert math.isclose(r_cos, 3430.3845, abs_tol=1e-2)
        assert math.isclose(r_vers, 7.3622, abs_tol=1e-2)

    def test_canonical_24_tabular_rsines(self):
        df = compute_24_tabular_rsines(RADIUS_EXACT)
        assert len(df) == 24
        
        # 8th tabulated Rsine: 30° (1800') -> R/2
        r8 = df.loc[df["Index (j)"] == 8, "Rsine (Jya)"].values[0]
        assert math.isclose(r8, RADIUS_EXACT / 2.0, rel_tol=1e-7)
        
        # 12th tabulated Rsine: 45° (2700') -> sqrt(R^2 / 2)
        r12 = df.loc[df["Index (j)"] == 12, "Rsine (Jya)"].values[0]
        assert math.isclose(r12, math.sqrt(RADIUS_EXACT ** 2 / 2.0), rel_tol=1e-7)
        
        # 24th tabulated Rsine: 90° (5400') -> R
        r24 = df.loc[df["Index (j)"] == 24, "Rsine (Jya)"].values[0]
        assert math.isclose(r24, RADIUS_EXACT, rel_tol=1e-7)

    def test_sista_capa_interpolation(self):
        # Interpolate at 337.5' (1.5 * 225')
        res = interpolate_sista_capa(337.5, RADIUS_EXACT, order=2)
        exact = jya(337.5, RADIUS_EXACT)
        assert res["nearest_tabular_index"] in (1, 2)
        assert math.isclose(res["approx_rsine"], exact, rel_tol=1e-4)

    def test_jive_paraspara_nyaya(self):
        # Addition: 30° (1800') + 15° (900') = 45° (2700')
        res = jive_paraspara_nyaya(1800.0, 900.0, operation="add", r=RADIUS_EXACT)
        exact_45 = jya(2700.0, RADIUS_EXACT)
        assert math.isclose(res["computed_rsine"], exact_45, rel_tol=1e-7)
        
        # Subtraction: 60° (3600') - 15° (900') = 45° (2700')
        res_sub = jive_paraspara_nyaya(3600.0, 900.0, operation="sub", r=RADIUS_EXACT)
        assert math.isclose(res_sub["computed_rsine"], exact_45, rel_tol=1e-7)


class TestSankalitaEngine:
    """Test Module 2: Sankalita & Calculus Engine."""

    def test_discrete_sankalita_formulas(self):
        # V_10^(1) = 1 + ... + 10 = 55
        assert sankalita_1(10) == 55
        # V_10^(2) = 10*11*12 / 6 = 220
        assert sankalita_2(10) == 220
        # V_10^(3) = 10*11*12*13 / 24 = 715
        assert sankalita_k(10, 3) == 715

    def test_madhava_series_convergence(self):
        # Test at s = 1800' (30°) -> exact = R/2 = 1718.873385'
        s = 1800.0
        exact = jya(s, RADIUS_EXACT)
        terms = madhava_rsine_series_terms(s, RADIUS_EXACT, max_order=9)
        
        err1 = abs(terms[1] - exact)
        err3 = abs(terms[3] - exact)
        err5 = abs(terms[5] - exact)
        err7 = abs(terms[7] - exact)
        
        # Each higher order must strictly reduce error
        assert err3 < err1
        assert err5 < err3
        assert err7 < err5
        assert err7 < 1e-4  # Accurate to within fraction of an arcsecond

    def test_discrete_step_simulation(self):
        res = discrete_sankalita_step_derivation(1800.0, n_partitions=100, r=RADIUS_EXACT)
        assert res["sara_error_pct"] < 1.5
        assert res["jya_error_pct"] < 1.5


class TestQuadrilateralEngine:
    """Test Module 3: Cyclic Quadrilateral Solver."""

    def test_lilavati_171_ground_truth(self):
        """
        Test Case 2:
        - Inputs: a = 75, b = 40, c = 51, d = 68
        - Semi-perimeter: s = (75+40+51+68)/2 = 117
        - Expected Diagonal x = BD = 77.0
        - Expected Diagonal y = AC = 85.0
        - Expected Third Diagonal z = DF = 84.0
        - Expected Area A = sqrt(42 * 77 * 66 * 49) = 3234.0 (Exact integer)
        - Expected Circum-radius r = 42.5
        """
        quad = CyclicQuadrilateral(75.0, 40.0, 51.0, 68.0)
        assert quad.is_valid is True
        assert quad.s == 117.0
        assert math.isclose(quad.diagonal_x, 77.0, abs_tol=1e-4)
        assert math.isclose(quad.diagonal_y, 85.0, abs_tol=1e-4)
        assert math.isclose(quad.diagonal_z, 84.0, abs_tol=1e-4)
        assert math.isclose(quad.area, 3234.0, abs_tol=1e-4)
        assert math.isclose(quad.circum_radius, 42.5, abs_tol=1e-4)
        assert math.isclose(quad.circum_diameter, 85.0, abs_tol=1e-4)

    def test_lamba_nipatanantara(self):
        quad = CyclicQuadrilateral(75.0, 40.0, 51.0, 68.0)
        # EF = 0.5 * ((75^2 + 51^2) - (40^2 + 68^2)) / 77
        expected_ef = 0.5 * ((75**2 + 51**2) - (40**2 + 68**2)) / 77.0
        assert math.isclose(quad.lamba_nipatanantara, expected_ef, abs_tol=1e-5)
        # Altitude sum relation: AP^2 + EF^2 = y^2
        ap = quad.lamba_yoga
        assert math.isclose(ap**2 + quad.lamba_nipatanantara**2, quad.diagonal_y**2, rel_tol=1e-5)

    def test_invalid_quadrilateral(self):
        # Side greater than semi-perimeter
        quad = CyclicQuadrilateral(100.0, 10.0, 10.0, 10.0)
        assert quad.is_valid is False


class TestSphereEngine:
    """Test Module 4: 3D Sphere Dissection & Pre-Calculus Integration."""

    def test_sphere_convergence_ground_truth(self):
        """
        Test Case 3:
        - Radius r = 10.0, N = 500
        - Discrete Surface Area S_500 ≈ 4*pi*(10^2) ± 0.1%
        - Discrete Volume V_500 ≈ (4/3)*pi*(10^3) ± 0.1%
        """
        res = compute_sphere_slices(radius=10.0, n_slices=500)
        assert res["sa_relative_error_pct"] < 0.1
        assert res["vol_relative_error_pct"] < 0.1

    def test_convergence_table_generator(self):
        df = generate_sphere_convergence_data(radius=10.0, n_values=[10, 50, 100, 500])
        assert len(df) == 4
        # Error strictly decreases as N increases
        assert df["SA Error %"].iloc[-1] < df["SA Error %"].iloc[0]
        assert df["Vol Error %"].iloc[-1] < df["Vol Error %"].iloc[0]

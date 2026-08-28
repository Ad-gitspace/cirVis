"""
Module 3: Cyclic Quadrilateral Solver (Kerala School of Mathematics)
Based on Chapter 7 (Sections 7.10 - 7.15): Diagonals, Area, and Circum-radius of Cyclic Quadrilaterals.

Key Theorems & Formulas:
- Brahmagupta's Area Formula (Lilavati 169): A = sqrt((s-a)(s-b)(s-c)(s-d))
- Madhava's 3 Diagonals: x = BD, y = AC, z = Third Diagonal (DF / EB)
- Paramesvara's Circum-radius Formula: r = (1/4) * sqrt( ((ab+cd)(ac+bd)(ad+bc)) / ((s-a)(s-b)(s-c)(s-d)) ) = (x*y*z) / (4*A)
- Lamba-nipatanantara (Interstice between altitude feet): EF = 0.5 * ((a^2 + c^2) - (b^2 + d^2)) / x
- Lamba-yoga (Sum of altitudes): AE + CF = 2*A / x
- Exact 2D Euclidean / Trigonometric embedding of vertices on the circumcircle.
"""

import math
from typing import Dict, List, Tuple, Any, Optional
import numpy as np


class CyclicQuadrilateral:
    """
    Representation and solver for a cyclic quadrilateral with four consecutive sides a, b, c, d.
    """
    def __init__(self, a: float, b: float, c: float, d: float):
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.d = float(d)
        
        self.is_valid, self.validation_message = self._validate()
        if self.is_valid:
            self._compute_properties()

    def _validate(self) -> Tuple[bool, str]:
        """Verify cyclic quadrilateral polygon inequality."""
        if self.a <= 0 or self.b <= 0 or self.c <= 0 or self.d <= 0:
            return False, "All side lengths must be strictly positive."
        
        s = (self.a + self.b + self.c + self.d) / 2.0
        if self.a >= s or self.b >= s or self.c >= s or self.d >= s:
            max_side = max(self.a, self.b, self.c, self.d)
            return False, f"Invalid cyclic polygon: side {max_side} exceeds or equals semi-perimeter {s}."
        
        return True, "Valid cyclic quadrilateral."

    def _compute_properties(self):
        a, b, c, d = self.a, self.b, self.c, self.d
        self.s = (a + b + c + d) / 2.0
        
        # Area (Brahmagupta)
        prod_s = (self.s - a) * (self.s - b) * (self.s - c) * (self.s - d)
        self.area = math.sqrt(max(0.0, prod_s))
        
        # Diagonals x (BD), y (AC), z (Third diagonal DF)
        p1 = a * b + c * d
        p2 = a * c + b * d
        p3 = a * d + b * c
        
        self.diagonal_x = math.sqrt((p1 * p2) / p3)  # BD
        self.diagonal_y = math.sqrt((p2 * p3) / p1)  # AC
        self.diagonal_z = math.sqrt((p1 * p3) / p2)  # DF (Third diagonal)
        
        # Paramesvara Circum-radius
        self.circum_radius = (self.diagonal_x * self.diagonal_y * self.diagonal_z) / (4.0 * self.area)
        self.circum_diameter = 2.0 * self.circum_radius
        
        # Lamba-nipatanantara (Interstice between altitude feet on diagonal BD)
        self.lamba_nipatanantara = 0.5 * ((a**2 + c**2) - (b**2 + d**2)) / self.diagonal_x
        
        # Altitudes onto diagonal BD (base x)
        # In triangle ABD, sides are a, d, x -> semi-perimeter s_abd = (a + d + x) / 2
        s_abd = (a + d + self.diagonal_x) / 2.0
        area_abd = math.sqrt(max(0.0, s_abd * (s_abd - a) * (s_abd - d) * (s_abd - self.diagonal_x)))
        self.altitude_ae = 2.0 * area_abd / self.diagonal_x
        
        # In triangle CBD, sides are b, c, x -> semi-perimeter s_cbd = (b + c + x) / 2
        s_cbd = (b + c + self.diagonal_x) / 2.0
        area_cbd = math.sqrt(max(0.0, s_cbd * (s_cbd - b) * (s_cbd - c) * (s_cbd - self.diagonal_x)))
        self.altitude_cf = 2.0 * area_cbd / self.diagonal_x
        
        self.lamba_yoga = self.altitude_ae + self.altitude_cf

    def get_summary(self) -> Dict[str, Any]:
        """Return all calculated geometrical metrics."""
        if not self.is_valid:
            return {"is_valid": False, "error": self.validation_message}
            
        return {
            "is_valid": True,
            "sides": {"a (AB)": self.a, "b (BC)": self.b, "c (CD)": self.c, "d (DA)": self.d},
            "semi_perimeter_s": self.s,
            "area_brahmagupta": self.area,
            "diagonal_x_BD": self.diagonal_x,
            "diagonal_y_AC": self.diagonal_y,
            "diagonal_z_DF": self.diagonal_z,
            "circum_radius_paramesvara": self.circum_radius,
            "circum_diameter": self.circum_diameter,
            "lamba_nipatanantara_EF": self.lamba_nipatanantara,
            "altitude_AE": self.altitude_ae,
            "altitude_CF": self.altitude_cf,
            "lamba_yoga_AP": self.lamba_yoga,
        }

    def compute_vertex_coordinates(self) -> Dict[str, Tuple[float, float]]:
        """
        Compute 2D Cartesian coordinates of vertices A, B, C, D, circumcircle center O(0,0),
        and altitude feet E and F on diagonal BD.
        """
        if not self.is_valid:
            return {}
            
        r = self.circum_radius
        
        # Central angles subtended by each chord side
        ang_a = 2.0 * math.asin(min(1.0, self.a / (2.0 * r)))
        ang_b = 2.0 * math.asin(min(1.0, self.b / (2.0 * r)))
        ang_c = 2.0 * math.asin(min(1.0, self.c / (2.0 * r)))
        ang_d = 2.0 * math.asin(min(1.0, self.d / (2.0 * r)))
        
        # Scale angles to exactly sum to 2*pi if there are minute floating point rounding residuals
        total_ang = ang_a + ang_b + ang_c + ang_d
        ang_a *= (2.0 * math.pi / total_ang)
        ang_b *= (2.0 * math.pi / total_ang)
        ang_c *= (2.0 * math.pi / total_ang)
        ang_d *= (2.0 * math.pi / total_ang)
        
        # Start A at angle 0 (or orient so BD is horizontal/diagonal)
        phi_A = 0.0
        phi_B = phi_A + ang_a
        phi_C = phi_B + ang_b
        phi_D = phi_C + ang_c
        
        xA, yA = r * math.cos(phi_A), r * math.sin(phi_A)
        xB, yB = r * math.cos(phi_B), r * math.sin(phi_B)
        xC, yC = r * math.cos(phi_C), r * math.sin(phi_C)
        xD, yD = r * math.cos(phi_D), r * math.sin(phi_D)
        
        # Altitude foot E (projection of A onto line BD)
        # Vector BD: (xD - xB, yD - yB)
        vBD = np.array([xD - xB, yD - yB])
        len_BD_sq = np.dot(vBD, vBD)
        vBA = np.array([xA - xB, yA - yB])
        tE = np.dot(vBA, vBD) / len_BD_sq
        ptE = np.array([xB, yB]) + tE * vBD
        
        # Altitude foot F (projection of C onto line BD)
        vBC = np.array([xC - xB, yC - yB])
        tF = np.dot(vBC, vBD) / len_BD_sq
        ptF = np.array([xB, yB]) + tF * vBD
        
        return {
            "O": (0.0, 0.0),
            "A": (xA, yA),
            "B": (xB, yB),
            "C": (xC, yC),
            "D": (xD, yD),
            "E": (float(ptE[0]), float(ptE[1])),
            "F": (float(ptF[0]), float(ptF[1])),
            "M": (float(xB + xD) / 2.0, float(yB + yD) / 2.0),
        }

"""
Module 1: Ancient Trigonometry Engine (Kerala School of Mathematics)
Based on Chapter 7: Derivation of Sines from Yuktibhasa & Tantrasangraha.

Key Concepts:
- Circumference C = 21600 arcminutes (360 deg * 60)
- Radius R = C / (2 * pi) approx 3437.74677 arcminutes
- Tabular step alpha = 225 arcminutes (3 deg 45 min = 90 deg / 24)
- 24 Tabular Rsines (Pathita-jya)
- Sista-capa 2nd order Taylor-Madhava interpolation
- Jive-paraspara-nyaya (Sine/Cosine Addition Theorem)
"""

import math
from typing import Dict, List, Tuple, Any
import numpy as np
import pandas as pd

# Global Constants
TOTAL_CIRCUMFERENCE: float = 21600.0  # arcminutes
RADIUS_EXACT: float = TOTAL_CIRCUMFERENCE / (2.0 * math.pi)  # ~3437.7467707849396 arcminutes
RADIUS_KATAPAYADI: float = 3437.0 + 44.0 / 60.0 + 48.0 / 3600.0  # 3437' 44'' 48''' ~ 3437.74666667
ARC_BIT_ALPHA: float = 225.0  # 225 arcminutes = 3° 45'
NUM_TABULAR_SINES: int = 24


def deg_min_sec_to_minutes(degrees: float, minutes: float = 0.0, seconds: float = 0.0) -> float:
    """Convert degrees, arcminutes, and arcseconds to total arcminutes."""
    return degrees * 60.0 + minutes + seconds / 60.0


def minutes_to_deg_min_sec(total_minutes: float) -> Tuple[int, int, float]:
    """Convert total arcminutes to (degrees, arcminutes, arcseconds)."""
    sign = -1 if total_minutes < 0 else 1
    m_abs = abs(total_minutes)
    deg = int(m_abs // 60)
    rem_min = m_abs - deg * 60
    minutes = int(rem_min)
    seconds = (rem_min - minutes) * 60.0
    return sign * deg, minutes, round(seconds, 4)


def format_sexagesimal(total_minutes: float) -> str:
    """Format total arcminutes as a readable string: D° M' S"."""
    deg, m, s = minutes_to_deg_min_sec(total_minutes)
    return f"{deg}° {m:02d}' {s:05.2f}\""


def minutes_to_radians(arcminutes: float, r: float = RADIUS_EXACT) -> float:
    """Convert arcminutes along circumference to radians."""
    return arcminutes / r


def radians_to_minutes(rad: float, r: float = RADIUS_EXACT) -> float:
    """Convert radians to arcminutes along circumference."""
    return rad * r


def jya(arc_minutes: float, r: float = RADIUS_EXACT) -> float:
    """Exact modern Rsine: R * sin(s / R)."""
    theta = arc_minutes / r
    return r * math.sin(theta)


def koti_jya(arc_minutes: float, r: float = RADIUS_EXACT) -> float:
    """Exact modern Rcosine: R * cos(s / R)."""
    theta = arc_minutes / r
    return r * math.cos(theta)


def sara(arc_minutes: float, r: float = RADIUS_EXACT) -> float:
    """Exact modern Rversine (arrow): R * (1 - cos(s / R))."""
    theta = arc_minutes / r
    return r * (1.0 - math.cos(theta))


def half_arc_rsine(r_sin_s: float, r_vers_s: float) -> float:
    """
    Compute Rsine of half-arc using ancient geometric chord formula:
    R*sin(s/2) = 0.5 * sqrt(R*sin(s)^2 + R*vers(s)^2)
    (Equation 7.9 in Yuktibhasa)
    """
    return 0.5 * math.sqrt(r_sin_s ** 2 + r_vers_s ** 2)


def comp_arc_rcosine(r_sin_s: float, r: float = RADIUS_EXACT) -> float:
    """
    Compute Rcosine using Pythagoras complementary arc relation:
    R*cos(s) = sqrt(R^2 - R*sin(s)^2)
    (Equation 7.10 in Yuktibhasa)
    """
    val = max(0.0, r ** 2 - r_sin_s ** 2)
    return math.sqrt(val)


def compute_24_tabular_rsines(r: float = RADIUS_EXACT) -> pd.DataFrame:
    """
    Compute the 24 ancient Tabular Rsines (Pathita-jya), Rcosines, Rversines,
    first differences (Khanda-jya) and second differences (Khanda-jyantara).
    
    Returns a pandas DataFrame with all 24 entries (1 to 24) matching multiples of 225'.
    """
    # 24 indices: 1 to 24
    # Multiple of alpha = j * 225'
    data = []
    
    # We first generate exact tabulated values geometrically
    # 8th is 30 deg (1800'), 12th is 45 deg (2700'), 16th is 60 deg (3600'), 24th is 90 deg (5400')
    rsines = [0.0] * 25
    rcosines = [0.0] * 25
    rversines = [0.0] * 25
    
    for j in range(1, 25):
        s_j = j * ARC_BIT_ALPHA
        theta = s_j / r
        rsines[j] = r * math.sin(theta)
        rcosines[j] = r * math.cos(theta)
        rversines[j] = r * (1.0 - math.cos(theta))
        
    diff1 = [0.0] * 25
    for j in range(1, 25):
        if j == 1:
            diff1[j] = rsines[1]
        else:
            diff1[j] = rsines[j] - rsines[j - 1]
            
    diff2 = [0.0] * 25
    for j in range(1, 24):
        diff2[j] = diff1[j] - diff1[j + 1]
    diff2[24] = np.nan
    
    for j in range(1, 25):
        s_j = j * ARC_BIT_ALPHA
        deg = s_j / 60.0
        data.append({
            "Index (j)": j,
            "Arc s (arcmin)": round(s_j, 2),
            "Angle (deg)": f"{deg:.2f}°",
            "Rsine (Jya)": round(rsines[j], 5),
            "Rcosine (Koti)": round(rcosines[j], 5),
            "Rversine (Sara)": round(rversines[j], 5),
            "1st Diff (Δ_j)": round(diff1[j], 5),
            "2nd Diff (Δ_j - Δ_{j+1})": round(diff2[j], 5) if not np.isnan(diff2[j]) else "—",
            "Sexagesimal Rsine": format_sexagesimal(rsines[j]),
        })
        
    return pd.DataFrame(data)


def interpolate_sista_capa(
    desired_arc_min: float,
    r: float = RADIUS_EXACT,
    order: int = 2
) -> Dict[str, Any]:
    """
    Compute Rsine and Rcosine for an arbitrary arc using Sista-capa interpolation
    (remainder arc correction) from the nearest tabular point (Tantrasangraha 2.10 / Yuktibhasa 7.4.3).
    
    Formula (2nd Order):
    R*sin(s_i + Δ) ≈ R*sin(s_i) + (Δ/R)*R*cos(s_i) - 0.5*(Δ/R)^2 * R*sin(s_i)
    R*cos(s_i + Δ) ≈ R*cos(s_i) - (Δ/R)*R*sin(s_i) - 0.5*(Δ/R)^2 * R*cos(s_i)
    """
    # Restrict to [0, 5400] for quadrant interpolation
    s = max(0.0, min(5400.0, float(desired_arc_min)))
    
    # Nearest tabular point index i
    idx = round(s / ARC_BIT_ALPHA)
    idx = max(0, min(24, idx))
    s_i = idx * ARC_BIT_ALPHA
    delta = s - s_i  # remainder arc (Sista-capa), can be positive or negative
    
    # Tabular values at s_i
    theta_i = s_i / r
    r_sin_i = r * math.sin(theta_i)
    r_cos_i = r * math.cos(theta_i)
    
    delta_over_r = delta / r
    
    if order == 1:
        approx_sin = r_sin_i + delta_over_r * r_cos_i
        approx_cos = r_cos_i - delta_over_r * r_sin_i
    elif order == 2:
        approx_sin = r_sin_i + delta_over_r * r_cos_i - 0.5 * (delta_over_r ** 2) * r_sin_i
        approx_cos = r_cos_i - delta_over_r * r_sin_i - 0.5 * (delta_over_r ** 2) * r_cos_i
    elif order >= 3:
        # 3rd order Madhava footnote 10 in Chapter 7
        approx_sin = (
            r_sin_i
            + delta_over_r * r_cos_i
            - 0.5 * (delta_over_r ** 2) * r_sin_i
            - (1.0 / 6.0) * (delta_over_r ** 3) * r_cos_i
        )
        approx_cos = (
            r_cos_i
            - delta_over_r * r_sin_i
            - 0.5 * (delta_over_r ** 2) * r_cos_i
            + (1.0 / 6.0) * (delta_over_r ** 3) * r_sin_i
        )
    else:
        approx_sin = r_sin_i
        approx_cos = r_cos_i
        
    approx_vers = r - approx_cos
    
    # Exact modern values
    exact_sin = r * math.sin(s / r)
    exact_cos = r * math.cos(s / r)
    exact_vers = r * (1.0 - math.cos(s / r))
    
    error_sin = abs(approx_sin - exact_sin)
    error_cos = abs(approx_cos - exact_cos)
    
    return {
        "desired_arc": s,
        "nearest_tabular_index": idx,
        "nearest_tabular_arc": s_i,
        "sista_capa_delta": delta,
        "order": order,
        "approx_rsine": approx_sin,
        "exact_rsine": exact_sin,
        "error_rsine": error_sin,
        "approx_rcosine": approx_cos,
        "exact_rcosine": exact_cos,
        "error_rcosine": error_cos,
        "approx_rversine": approx_vers,
        "exact_rversine": exact_vers,
    }


def jive_paraspara_nyaya(
    s1_min: float,
    s2_min: float,
    operation: str = "add",
    r: float = RADIUS_EXACT
) -> Dict[str, float]:
    """
    Jive-paraspara-nyaya (Madhava's Sine/Cosine Addition Theorem, Yuktibhasa 7.8, Tantrasangraha 2.12).
    
    R*sin(s1 +/- s2) = (1/R) * [ R*sin(s1)*R*cos(s2) +/- R*cos(s1)*R*sin(s2) ]
    R*cos(s1 +/- s2) = (1/R) * [ R*cos(s1)*R*cos(s2) -/+ R*sin(s1)*R*sin(s2) ]
    """
    sin1 = r * math.sin(s1_min / r)
    cos1 = r * math.cos(s1_min / r)
    sin2 = r * math.sin(s2_min / r)
    cos2 = r * math.cos(s2_min / r)
    
    if operation == "add":
        jya_res = (sin1 * cos2 + cos1 * sin2) / r
        koti_res = (cos1 * cos2 - sin1 * sin2) / r
        target_arc = s1_min + s2_min
    else:
        jya_res = (sin1 * cos2 - cos1 * sin2) / r
        koti_res = (cos1 * cos2 + sin1 * sin2) / r
        target_arc = s1_min - s2_min
        
    sara_res = r - koti_res
    
    # Modern exact
    exact_sin = r * math.sin(target_arc / r)
    exact_cos = r * math.cos(target_arc / r)
    
    return {
        "s1": s1_min,
        "s2": s2_min,
        "target_arc": target_arc,
        "operation": operation,
        "computed_rsine": jya_res,
        "exact_rsine": exact_sin,
        "error_rsine": abs(jya_res - exact_sin),
        "computed_rcosine": koti_res,
        "exact_rcosine": exact_cos,
        "error_rcosine": abs(koti_res - exact_cos),
        "computed_rversine": sara_res,
    }

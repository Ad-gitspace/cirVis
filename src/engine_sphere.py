"""
Module 4: 3D Sphere Slicing & Pre-Calculus Integration Engine
Based on Chapter 7 (Sections 7.18 - 7.19): Surface Area and Volume of a Sphere via Slicing & Sankalita.

Key Principles from Yuktibhāṣā:
1. Surface Area (Section 7.18):
   - Meridian circle is divided into N equal arc-bits of length Delta s = pi * r / N.
   - At each arc-bit with colatitude theta_j = (j - 0.5) * pi / N, the parallel circle radius is B_j = r * sin(theta_j).
   - Unrolled surface strip area: Area_j = (C/r) * B_j * Delta s = 2 * pi * r^2 * sin(theta_j) * Delta theta.
   - Total Surface Area: S_N = sum Area_j -> C * d = 4 * pi * r^2.

2. Volume (Section 7.19):
   - Sphere is divided into N horizontal cylindrical slices along vertical diameter, Delta z = 2*r / N.
   - Slice radius at height z_j: B_j = sqrt(r^2 - z_j^2).
   - Slice circular cross-section area: A_j = 0.5 * (C/r) * B_j^2 = pi * B_j^2.
   - Sliced volume sum: V_N = sum A_j * Delta z = sum pi * B_j^2 * Delta z -> (1/6) * C * d^2 = (4/3) * pi * r^3.
"""

import math
from typing import Dict, List, Tuple, Any
import numpy as np
import pandas as pd


def compute_sphere_slices(radius: float = 10.0, n_slices: int = 50) -> Dict[str, Any]:
    """
    Compute properties of N slices of a sphere for both surface area (meridian arc-bits)
    and volume (vertical cylindrical disks).
    """
    r = float(radius)
    n = max(4, int(n_slices))
    
    circumference = 2.0 * math.pi * r
    diameter = 2.0 * r
    
    # 1. Volume via vertical cylindrical slicing: Delta z = 2r / N
    delta_z = diameter / n
    total_volume = 0.0
    
    # 2. Surface Area via meridian arc-bit slicing: Delta theta = pi / N, Delta s = pi * r / N
    delta_theta = math.pi / n
    delta_s = r * delta_theta
    total_surface_area = 0.0
    
    slice_data = []
    
    for j in range(1, n + 1):
        # Vertical slice coordinates (for volume & 3D disks)
        z_mid = -r + (j - 0.5) * delta_z
        z_lower = -r + (j - 1) * delta_z
        z_upper = -r + j * delta_z
        bj_z = math.sqrt(max(0.0, r ** 2 - z_mid ** 2))
        
        # Volume of j-th cylindrical disk: pi * B_j^2 * Delta z
        slice_vol = math.pi * (bj_z ** 2) * delta_z
        total_volume += slice_vol
        
        # Meridian arc coordinates (for surface area strips)
        theta_j = (j - 0.5) * delta_theta
        bj_theta = r * math.sin(theta_j)
        slice_circ = 2.0 * math.pi * bj_theta
        
        # Surface area of j-th trapezoidal/rectangular unrolled strip
        strip_sa = (circumference / r) * bj_theta * delta_s  # = 2 * pi * r * sin(theta_j) * (r * dtheta)
        total_surface_area += strip_sa
        
        slice_data.append({
            "slice_index": j,
            "z_mid": z_mid,
            "radius_bj": bj_z,
            "theta_deg": math.degrees(theta_j),
            "slice_circumference": slice_circ,
            "surface_strip_area": strip_sa,
            "slice_volume": slice_vol,
        })
        
    exact_surface_area = 4.0 * math.pi * (r ** 2)
    exact_volume = (4.0 / 3.0) * math.pi * (r ** 3)
    
    sa_error = abs(total_surface_area - exact_surface_area)
    vol_error = abs(total_volume - exact_volume)
    
    return {
        "radius": r,
        "diameter": diameter,
        "n_slices": n,
        "delta_z": delta_z,
        "delta_s": delta_s,
        "slices_df": pd.DataFrame(slice_data),
        "discrete_surface_area": total_surface_area,
        "exact_surface_area": exact_surface_area,
        "sa_absolute_error": sa_error,
        "sa_relative_error_pct": (sa_error / exact_surface_area) * 100.0,
        "discrete_volume": total_volume,
        "exact_volume": exact_volume,
        "vol_absolute_error": vol_error,
        "vol_relative_error_pct": (vol_error / exact_volume) * 100.0,
    }


def generate_sphere_convergence_data(
    radius: float = 10.0,
    n_values: List[int] = None
) -> pd.DataFrame:
    """
    Generate convergence data for varying N slices from 10 up to 1000.
    """
    if n_values is None:
        n_values = [10, 20, 50, 100, 200, 500, 1000]
        
    r = float(radius)
    exact_sa = 4.0 * math.pi * (r ** 2)
    exact_vol = (4.0 / 3.0) * math.pi * (r ** 3)
    
    records = []
    for n in n_values:
        res = compute_sphere_slices(r, n)
        records.append({
            "N Slices": n,
            "Δz": round(res["delta_z"], 4),
            "Δs (Arc-Bit)": round(res["delta_s"], 4),
            "Discrete Surface Area": round(res["discrete_surface_area"], 4),
            "Exact Surface Area": round(exact_sa, 4),
            "SA Error %": round(res["sa_relative_error_pct"], 5),
            "Discrete Volume": round(res["discrete_volume"], 4),
            "Exact Volume": round(exact_vol, 4),
            "Vol Error %": round(res["vol_relative_error_pct"], 5),
        })
        
    return pd.DataFrame(records)

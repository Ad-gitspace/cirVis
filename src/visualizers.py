"""
Module 5: Visualization Pipelines (Plotly 2D & 3D)
Interactive charts and geometric diagrams for Kerala Mathematics concepts.
"""

import math
from typing import Dict, List, Tuple, Any, Optional
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from src.engine_trig import (
    RADIUS_EXACT,
    TOTAL_CIRCUMFERENCE,
    ARC_BIT_ALPHA,
    jya,
    koti_jya,
    sara,
    format_sexagesimal,
    jive_paraspara_nyaya,
)
from src.engine_sankalita import (
    madhava_rsine_series_terms,
    generate_series_convergence_curves,
)
from src.engine_quadrilaterals import CyclicQuadrilateral
from src.engine_sphere import compute_sphere_slices


# Theme color constants
COLOR_PRIMARY = "#00D4FF"      # Cyan
COLOR_SECONDARY = "#FF6B6B"    # Coral / Red
COLOR_ACCENT = "#FFD166"       # Gold / Amber
COLOR_GREEN = "#06D6A0"        # Emerald
COLOR_PURPLE = "#9B5DE5"       # Lavender / Purple
COLOR_BG = "rgba(17, 24, 39, 0.95)"
COLOR_GRID = "rgba(255, 255, 255, 0.1)"


def plot_chapter_proof(section: str, r: float = RADIUS_EXACT) -> go.Figure:
    """Draw a focused geometric/sequence sketch for a Chapter 7 proof."""
    fig = go.Figure()
    theta = np.linspace(0, 2 * np.pi, 360)

    if section == "7.1–7.2 | Hexagon and Rsine geometry":
        vertex_angles = np.pi / 6 + np.arange(6) * np.pi / 3
        points = np.column_stack((r * np.cos(vertex_angles), r * np.sin(vertex_angles)))
        closed = np.vstack((points, points[0]))
        fig.add_trace(go.Scatter(x=closed[:, 0], y=closed[:, 1], mode="lines+markers", name="Inscribed regular hexagon", line=dict(color=COLOR_PRIMARY, width=3), marker=dict(size=8)))
        x30, y30 = r * math.cos(math.pi / 6), r * math.sin(math.pi / 6)
        fig.add_trace(go.Scatter(x=[0, x30], y=[0, y30], mode="lines+markers+text", text=["O", "P (30°)"], textposition="top center", name="Radius r", line=dict(color=COLOR_ACCENT, width=2)))
        fig.add_trace(go.Scatter(x=[x30, x30], y=[-y30, y30], mode="lines", name="60° chord = r", line=dict(color=COLOR_GREEN, width=3)))
        fig.add_trace(go.Scatter(x=[x30, x30], y=[0, y30], mode="lines+markers+text", text=["", "Jyā = r/2"], textposition="middle right", name="Half-chord: Rsine 30°", line=dict(color=COLOR_SECONDARY, width=4, dash="dash")))
        title = "A 60° chord equals the radius; its half-chord gives R sin 30° = r/2"
        extent = r * 1.25
    elif section == "7.3 | Quadrants and sine/cosine signs":
        fig.add_trace(go.Scatter(x=r * np.cos(theta), y=r * np.sin(theta), mode="lines", name="Circle", line=dict(color="#94A3B8")))
        for deg in (45, 135, 225, 315):
            a = math.radians(deg)
            x, y = r * math.cos(a), r * math.sin(a)
            fig.add_trace(go.Scatter(x=[0, x], y=[0, y], mode="lines+markers", name=f"{deg}°", line=dict(color=COLOR_PURPLE, width=2)))
            fig.add_annotation(x=x * 1.18, y=y * 1.18, text=f"Q{(deg - 1) // 90 + 1}: sin {y/r:+.1f}, cos {x/r:+.1f}", showarrow=False, font=dict(color="#E5E7EB", size=11))
        title = "Signs follow the north/south and east/west projections"
        extent = r * 1.42
    elif section == "7.7 | Square of the Rsine":
        angle = math.radians(55)
        x, y = r * math.cos(angle), r * math.sin(angle)
        fig.add_trace(go.Scatter(x=[0, x, 0, 0], y=[0, 0, y, 0], mode="lines+markers+text", text=["O", "K", "A", ""], textposition="top center", name="Right triangle", fill="toself", fillcolor="rgba(0,212,255,0.10)", line=dict(color=COLOR_PRIMARY, width=3)))
        fig.add_trace(go.Scatter(x=[0, x], y=[0, y], mode="lines", name="Radius r", line=dict(color=COLOR_ACCENT, width=3)))
        fig.add_annotation(x=x / 2, y=-r * .1, text="Rcos(s)", showarrow=False, font=dict(color=COLOR_ACCENT))
        fig.add_annotation(x=-r * .1, y=y / 2, text="Rsin(s)", showarrow=False, textangle=-90, font=dict(color=COLOR_SECONDARY))
        title = "Pythagoras on the radius: (R sin s)² + (R cos s)² = r²"
        extent = r * 1.2
    elif section == "7.9 | Area of a triangle":
        a = (0, 0); b = (r, 0); c = (r * .68, r * .72); foot = (c[0], 0)
        fig.add_trace(go.Scatter(x=[a[0], b[0], c[0], a[0]], y=[a[1], b[1], c[1], a[1]], mode="lines+markers+text", text=["A", "B", "C", ""], textposition="top center", fill="toself", fillcolor="rgba(155,93,229,.12)", name="Triangle ABC", line=dict(color=COLOR_PRIMARY, width=3)))
        fig.add_trace(go.Scatter(x=[foot[0], foot[0]], y=[0, c[1]], mode="lines+markers+text", text=["", "H"], textposition="middle right", name="Altitude h", line=dict(color=COLOR_SECONDARY, dash="dash", width=3)))
        fig.add_annotation(x=r/2, y=-r*.1, text="Base b", showarrow=False)
        fig.add_annotation(x=r*.8, y=r*.5, text="Area = ½ b h", showarrow=False, font=dict(color=COLOR_ACCENT, size=15))
        title = "The same triangle area is half the base times its perpendicular height"
        extent = r * 1.2
    elif section == "7.11 | Cyclic proof of angle addition":
        a1, a2 = math.radians(35), math.radians(70)
        fig.add_trace(go.Scatter(x=r * np.cos(theta), y=r * np.sin(theta), mode="lines", name="Circumcircle", line=dict(color="#94A3B8")))
        pts = [(r*math.cos(v), r*math.sin(v)) for v in (0, a1, a1+a2)]
        for i, (x, y) in enumerate(pts):
            fig.add_trace(go.Scatter(x=[0, x], y=[0, y], mode="lines+markers", name=["First arc", "Intermediate radius", "Combined arc"][i], line=dict(color=[COLOR_ACCENT, COLOR_PURPLE, COLOR_SECONDARY][i], width=2)))
        fig.add_trace(go.Scatter(x=[p[0] for p in pts], y=[p[1] for p in pts], mode="markers+text", text=["E", "A₁", "A₂"], textposition="top center", showlegend=False))
        title = "The cyclic-quadrilateral diagonals encode the sine of a sum"
        extent = r * 1.2
    elif section == "7.12 | Tabular Rsines without the radius":
        indices = np.arange(1, 25)
        vals = np.array([r * math.sin(j * ARC_BIT_ALPHA / r) for j in range(25)])
        first = np.diff(vals)
        second = first[:-1] - first[1:]
        fig.add_trace(go.Scatter(x=indices, y=vals[1:], mode="lines+markers", name="Rsines Bⱼ", line=dict(color=COLOR_PRIMARY, width=3)))
        fig.add_trace(go.Scatter(x=indices, y=first, mode="lines+markers", name="First differences Δⱼ", yaxis="y2", line=dict(color=COLOR_ACCENT, width=2)))
        fig.add_trace(go.Scatter(x=indices[1:-1], y=second, mode="lines+markers", name="Second differences", yaxis="y2", line=dict(color=COLOR_SECONDARY, width=2, dash="dash")))
        fig.update_layout(yaxis2=dict(title="First/second difference", overlaying="y", side="right", showgrid=False))
        title = "Successive equal arc-bits create a second-difference recurrence"
        fig.update_layout(xaxis_title="Arc-bit index j", yaxis_title="Length (arcminutes)")
        fig.update_layout(template="plotly_dark")
        fig.update_layout(paper_bgcolor=COLOR_BG, plot_bgcolor=COLOR_BG, font=dict(color="#E5E7EB"), height=480)
        return fig
    elif section == "7.13 | Altitude and circum-diameter":
        pts = {"A": (0, r*.72), "B": (-r*.85, 0), "C": (r*.85, 0)}
        fig.add_trace(go.Scatter(x=[pts[k][0] for k in ("A", "B", "C", "A")], y=[pts[k][1] for k in ("A", "B", "C", "A")], mode="lines+markers+text", text=["A", "B", "C", ""], textposition="top center", fill="toself", fillcolor="rgba(0,212,255,.08)", name="Triangle"))
        fig.add_trace(go.Scatter(x=[0, 0], y=[0, pts["A"][1]], mode="lines+markers", name="Altitude h", line=dict(color=COLOR_SECONDARY, width=3, dash="dash")))
        fig.add_trace(go.Scatter(x=[-r*.85, r*.85], y=[0, 0], mode="lines", name="Opposite side a", line=dict(color=COLOR_ACCENT, width=3)))
        fig.add_annotation(x=0, y=-r*.15, text="For an inscribed triangle: a = 2R sin A", showarrow=False, font=dict(color=COLOR_ACCENT, size=14))
        title = "Chord, altitude, and circumradius connect through the inscribed angle"
        extent = r * 1.2
    elif section == "7.17 | Solving the shadow problem":
        h = r * .48; base = r
        fig.add_trace(go.Scatter(x=[0, base, base, 0], y=[0, 0, h, 0], mode="lines+markers+text", text=["Foot 1", "Foot 2", "Lamp", ""], textposition="top center", name="Shadow triangle", fill="toself", fillcolor="rgba(255,107,107,.10)", line=dict(color=COLOR_PRIMARY, width=3)))
        fig.add_trace(go.Scatter(x=[0, base], y=[0, h], mode="lines", name="Shadow hypotenuse", line=dict(color=COLOR_ACCENT, width=2, dash="dash")))
        fig.add_annotation(x=base/2, y=-h*.16, text="Shadow difference", showarrow=False)
        title = "Similar-triangle and square-difference relations recover unknown shadows"
        extent = r * 1.2
    elif section == "7.19.1 | Area of a circle":
        a = np.linspace(0, np.pi, 120)
        fig.add_trace(go.Scatter(x=r*np.cos(a), y=r*np.sin(a), mode="lines", name="Semicircle", line=dict(color=COLOR_PRIMARY, width=3), fill="toself", fillcolor="rgba(0,212,255,.08)"))
        fig.add_trace(go.Scatter(x=r*np.cos(a), y=-r*np.sin(a), mode="lines", name="Semicircle", line=dict(color=COLOR_PURPLE, width=3), fill="toself", fillcolor="rgba(155,93,229,.08)"))
        fig.add_annotation(x=0, y=r*.5, text="Rearranged sectors form a rectangle\nArea = ½ × circumference × radius", showarrow=False, font=dict(color=COLOR_ACCENT, size=14))
        title = "Rearranging many circle sectors gives area = ½Cr"
        extent = r * 1.2
    else:
        raise ValueError(f"Unknown Chapter 7 proof section: {section}")

    fig.update_layout(title=title, xaxis=dict(range=[-extent, extent], zeroline=False, gridcolor=COLOR_GRID), yaxis=dict(range=[-extent, extent], scaleanchor="x", scaleratio=1, zeroline=False, gridcolor=COLOR_GRID), paper_bgcolor=COLOR_BG, plot_bgcolor=COLOR_BG, font=dict(color="#E5E7EB"), legend=dict(orientation="h", y=-0.18), margin=dict(l=30, r=30, t=65, b=60), height=480)
    return fig


def plot_trig_circle(
    s1_min: float,
    s2_min: Optional[float] = None,
    mode: str = "single",
    r: float = RADIUS_EXACT
) -> go.Figure:
    """
    Generate 2D interactive trigonometric circle for Yuktibhasa Chapter 7.
    """
    fig = go.Figure()
    
    # 1. Base Circle
    circle_theta = np.linspace(0, 2 * np.pi, 300)
    cx = r * np.cos(circle_theta)
    cy = r * np.sin(circle_theta)
    
    fig.add_trace(go.Scatter(
        x=cx, y=cy,
        mode="lines",
        line=dict(color="rgba(156, 163, 175, 0.6)", width=2),
        name="Circumference (C=21600')",
        hoverinfo="skip"
    ))
    
    # Coordinate Axes
    fig.add_trace(go.Scatter(
        x=[-r * 1.15, r * 1.15], y=[0, 0],
        mode="lines",
        line=dict(color=COLOR_GRID, width=1.5, dash="dash"),
        name="East-West Line (EW)",
        hoverinfo="skip"
    ))
    fig.add_trace(go.Scatter(
        x=[0, 0], y=[-r * 1.15, r * 1.15],
        mode="lines",
        line=dict(color=COLOR_GRID, width=1.5, dash="dash"),
        name="North-South Line (NS)",
        hoverinfo="skip"
    ))
    
    # Cardinal Points: E(r, 0), N(0, r), W(-r, 0), S(0, -r), O(0,0)
    cardinals_x = [r, 0, -r, 0, 0]
    cardinals_y = [0, r, 0, -r, 0]
    cardinals_text = ["<b>E (East)</b>", "<b>N (North)</b>", "<b>W (West)</b>", "<b>S (South)</b>", "<b>O (Center)</b>"]
    
    fig.add_trace(go.Scatter(
        x=cardinals_x, y=cardinals_y,
        mode="markers+text",
        marker=dict(size=7, color="#E5E7EB"),
        text=cardinals_text,
        textposition=["middle right", "top center", "middle left", "bottom center", "bottom right"],
        textfont=dict(color="#D1D5DB", size=12),
        showlegend=False
    ))
    
    if mode == "single":
        theta1 = s1_min / r
        x1 = r * math.cos(theta1)
        y1 = r * math.sin(theta1)
        
        # Arc trace
        arc_thetas = np.linspace(0, theta1, 100)
        arc_x = r * np.cos(arc_thetas)
        arc_y = r * np.sin(arc_thetas)
        fig.add_trace(go.Scatter(
            x=arc_x, y=arc_y,
            mode="lines",
            line=dict(color=COLOR_PURPLE, width=4),
            name=f"Arc s = {s1_min:.1f}' ({format_sexagesimal(s1_min)})",
            hoverinfo="name"
        ))
        
        # Radius line OC1
        fig.add_trace(go.Scatter(
            x=[0, x1], y=[0, y1],
            mode="lines+markers",
            line=dict(color="rgba(255, 255, 255, 0.4)", width=2),
            marker=dict(size=8, color=COLOR_PURPLE),
            name="Radius r (OA)",
            hoverinfo="text",
            hovertext=f"Point A: ({x1:.1f}, {y1:.1f})"
        ))
        
        # Jyā (Rsine): vertical segment from (x1, 0) to (x1, y1)
        fig.add_trace(go.Scatter(
            x=[x1, x1], y=[0, y1],
            mode="lines+markers",
            line=dict(color=COLOR_PRIMARY, width=4),
            marker=dict(size=8, color=COLOR_PRIMARY),
            name=f"Jyā (Rsine) = {y1:.2f}'",
            hoverinfo="text",
            hovertext=f"Jyā: {y1:.3f}' ({format_sexagesimal(y1)})"
        ))
        
        # Koṭi-jyā (Rcosine): horizontal segment from (0,0) to (x1, 0)
        fig.add_trace(go.Scatter(
            x=[0, x1], y=[0, 0],
            mode="lines+markers",
            line=dict(color=COLOR_ACCENT, width=4),
            marker=dict(size=8, color=COLOR_ACCENT),
            name=f"Koṭi (Rcosine) = {x1:.2f}'",
            hoverinfo="text",
            hovertext=f"Koṭi: {x1:.3f}' ({format_sexagesimal(x1)})"
        ))
        
        # Śara (Rversine): horizontal arrow segment from (x1, 0) to (r, 0)
        sara_val = r - x1
        fig.add_trace(go.Scatter(
            x=[x1, r], y=[0, 0],
            mode="lines+markers",
            line=dict(color=COLOR_SECONDARY, width=4),
            marker=dict(size=8, color=COLOR_SECONDARY),
            name=f"Śara (Rversine) = {sara_val:.2f}'",
            hoverinfo="text",
            hovertext=f"Śara: {sara_val:.3f}' ({format_sexagesimal(sara_val)})"
        ))
        
        # Point A label
        fig.add_trace(go.Scatter(
            x=[x1], y=[y1],
            mode="text",
            text=[f"<b>A ({s1_min/60.0:.1f}°)</b>"],
            textposition="top right",
            textfont=dict(color="#FFFFFF", size=13),
            showlegend=False
        ))
        
    elif mode == "jive_paraspara" and s2_min is not None:
        # Show s1, s2, and (s1 + s2)
        theta1 = s1_min / r
        theta2 = s2_min / r
        theta_sum = (s1_min + s2_min) / r
        
        x1, y1 = r * math.cos(theta1), r * math.sin(theta1)
        x_sum, y_sum = r * math.cos(theta_sum), r * math.sin(theta_sum)
        
        # Arc s1
        arc1_th = np.linspace(0, theta1, 60)
        fig.add_trace(go.Scatter(
            x=r * np.cos(arc1_th), y=r * np.sin(arc1_th),
            mode="lines", line=dict(color=COLOR_PRIMARY, width=3),
            name=f"Arc s1 = {s1_min:.1f}'"
        ))
        
        # Arc s2 from s1 to s1+s2
        arc2_th = np.linspace(theta1, theta_sum, 60)
        fig.add_trace(go.Scatter(
            x=r * np.cos(arc2_th), y=r * np.sin(arc2_th),
            mode="lines", line=dict(color=COLOR_ACCENT, width=3),
            name=f"Arc s2 = {s2_min:.1f}'"
        ))
        
        # Total Rsine for (s1 + s2)
        fig.add_trace(go.Scatter(
            x=[x_sum, x_sum], y=[0, y_sum],
            mode="lines+markers",
            line=dict(color=COLOR_GREEN, width=4),
            name=f"R*sin(s1+s2) = {y_sum:.2f}'"
        ))
        
        # Radii
        fig.add_trace(go.Scatter(
            x=[0, x1], y=[0, y1],
            mode="lines", line=dict(color="rgba(255,255,255,0.3)", width=1.5),
            name="Radius to s1", hoverinfo="skip"
        ))
        fig.add_trace(go.Scatter(
            x=[0, x_sum], y=[0, y_sum],
            mode="lines", line=dict(color="rgba(255,255,255,0.3)", width=1.5),
            name="Radius to s1+s2", hoverinfo="skip"
        ))
        
        fig.add_trace(go.Scatter(
            x=[x1, x_sum], y=[y1, y_sum],
            mode="markers+text",
            marker=dict(size=9, color=[COLOR_PRIMARY, COLOR_GREEN]),
            text=["<b>A1 (s1)</b>", "<b>A2 (s1+s2)</b>"],
            textposition=["top right", "top right"],
            textfont=dict(color="#FFFFFF", size=13),
            showlegend=False
        ))
        
    fig.update_layout(
        title=dict(
            text="<b>Trigonometric Circle & Geometric Decomposition (Yuktibhāṣā Ch. 7)</b>",
            font=dict(size=16, color="#FFFFFF"),
            x=0.5
        ),
        xaxis=dict(
            range=[-r * 1.25, r * 1.25],
            zeroline=False,
            showgrid=True,
            gridcolor=COLOR_GRID,
            scaleanchor="y",
            scaleratio=1,
            title=dict(text="East-West Axis (Minutes)", font=dict(color="#9CA3AF")),
            tickfont=dict(color="#9CA3AF")
        ),
        yaxis=dict(
            range=[-r * 1.25, r * 1.25],
            zeroline=False,
            showgrid=True,
            gridcolor=COLOR_GRID,
            title=dict(text="North-South Axis (Minutes)", font=dict(color="#9CA3AF")),
            tickfont=dict(color="#9CA3AF")
        ),
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(color="#E5E7EB", size=11)
        ),
        margin=dict(l=40, r=40, t=60, b=80),
        height=550
    )
    
    return fig


def plot_sankalita_convergence(
    s_selected_min: float = 2700.0,
    r: float = RADIUS_EXACT
) -> go.Figure:
    """
    Plot Madhava series convergence curves (orders 1, 3, 5, 7, 9) vs modern exact sine
    and log-residual error chart.
    """
    df = generate_series_convergence_curves(max_arc_min=5400.0, num_points=150, r=r)
    
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.12,
        subplot_titles=(
            "<b>Madhava Series Approximations vs Exact Modern Sine</b>",
            "<b>Log-Scale Absolute Error Residuals (|Madhava - Exact|)</b>"
        )
    )
    
    # Subplot 1: Curves
    fig.add_trace(go.Scatter(
        x=df["angle_deg"], y=df["exact_rsine"],
        mode="lines", line=dict(color="#FFFFFF", width=3),
        name="Exact Rsine: R*sin(θ)"
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df["angle_deg"], y=df["order_1_rsine"],
        mode="lines", line=dict(color=COLOR_SECONDARY, width=2, dash="dot"),
        name="Order 1: s"
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df["angle_deg"], y=df["order_3_rsine"],
        mode="lines", line=dict(color=COLOR_ACCENT, width=2, dash="dash"),
        name="Order 3: s - s³/6r²"
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df["angle_deg"], y=df["order_5_rsine"],
        mode="lines", line=dict(color=COLOR_GREEN, width=2, dash="dashdot"),
        name="Order 5: s - s³/6r² + s⁵/120r⁴"
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df["angle_deg"], y=df["order_7_rsine"],
        mode="lines", line=dict(color=COLOR_PRIMARY, width=2),
        name="Order 7: ... - s⁷/5040r⁶"
    ), row=1, col=1)
    
    # Marker for selected point
    sel_deg = s_selected_min / 60.0
    sel_terms = madhava_rsine_series_terms(s_selected_min, r=r, max_order=9)
    sel_exact = r * math.sin(s_selected_min / r)
    
    fig.add_trace(go.Scatter(
        x=[sel_deg], y=[sel_exact],
        mode="markers",
        marker=dict(size=12, color="#FF007F", symbol="diamond"),
        name=f"Selected s = {s_selected_min:.0f}' ({sel_deg:.1f}°)"
    ), row=1, col=1)
    
    # Subplot 2: Log residuals
    fig.add_trace(go.Scatter(
        x=df["angle_deg"], y=np.maximum(1e-12, df["err_order_1"]),
        mode="lines", line=dict(color=COLOR_SECONDARY, width=2),
        name="Error (Order 1)", showlegend=False
    ), row=2, col=1)
    
    fig.add_trace(go.Scatter(
        x=df["angle_deg"], y=np.maximum(1e-12, df["err_order_3"]),
        mode="lines", line=dict(color=COLOR_ACCENT, width=2),
        name="Error (Order 3)", showlegend=False
    ), row=2, col=1)
    
    fig.add_trace(go.Scatter(
        x=df["angle_deg"], y=np.maximum(1e-12, df["err_order_5"]),
        mode="lines", line=dict(color=COLOR_GREEN, width=2),
        name="Error (Order 5)", showlegend=False
    ), row=2, col=1)
    
    fig.add_trace(go.Scatter(
        x=df["angle_deg"], y=np.maximum(1e-12, df["err_order_7"]),
        mode="lines", line=dict(color=COLOR_PRIMARY, width=2),
        name="Error (Order 7)", showlegend=False
    ), row=2, col=1)
    
    fig.update_yaxes(title_text="Rsine (Minutes)", row=1, col=1, gridcolor=COLOR_GRID)
    fig.update_yaxes(type="log", title_text="Abs Error (Minutes)", row=2, col=1, gridcolor=COLOR_GRID)
    fig.update_xaxes(title_text="Angle θ (Degrees)", row=2, col=1, gridcolor=COLOR_GRID)
    
    fig.update_layout(
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font=dict(color="#E5E7EB"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=50, r=40, t=60, b=80),
        height=650
    )
    
    return fig


def plot_cyclic_quadrilateral(quad: CyclicQuadrilateral) -> go.Figure:
    """
    Plot 2D dynamic cyclic quadrilateral with circumcircle, diagonals x & y,
    altitudes AE & CF, and interstice segment EF.
    """
    fig = go.Figure()
    
    if not quad.is_valid:
        fig.add_annotation(
            text=f"<b>Invalid Cyclic Quadrilateral:</b><br>{quad.validation_message}",
            showarrow=False,
            font=dict(size=16, color="#EF4444"),
            x=0.5, y=0.5, xref="paper", yref="paper"
        )
        fig.update_layout(paper_bgcolor=COLOR_BG, plot_bgcolor=COLOR_BG)
        return fig
        
    pts = quad.compute_vertex_coordinates()
    r = quad.circum_radius
    
    # 1. Circumcircle
    circle_theta = np.linspace(0, 2 * np.pi, 250)
    fig.add_trace(go.Scatter(
        x=r * np.cos(circle_theta),
        y=r * np.sin(circle_theta),
        mode="lines",
        line=dict(color="rgba(156, 163, 175, 0.4)", width=2, dash="dash"),
        name=f"Circumcircle (r = {r:.2f})",
        hoverinfo="skip"
    ))
    
    # Center O
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode="markers+text",
        marker=dict(size=6, color="#9CA3AF"),
        text=["O"], textposition="bottom right",
        showlegend=False
    ))
    
    # Quadrilateral sides A -> B -> C -> D -> A
    xA, yA = pts["A"]
    xB, yB = pts["B"]
    xC, yC = pts["C"]
    xD, yD = pts["D"]
    
    poly_x = [xA, xB, xC, xD, xA]
    poly_y = [yA, yB, yC, yD, yA]
    
    fig.add_trace(go.Scatter(
        x=poly_x, y=poly_y,
        mode="lines+markers",
        fill="toself",
        fillcolor="rgba(0, 212, 255, 0.08)",
        line=dict(color=COLOR_PRIMARY, width=3),
        marker=dict(size=10, color=COLOR_PRIMARY),
        name="Cyclic Quadrilateral ABCD",
        hoverinfo="text",
        hovertext=[
            f"Vertex A: ({xA:.1f}, {yA:.1f})",
            f"Vertex B: ({xB:.1f}, {yB:.1f})",
            f"Vertex C: ({xC:.1f}, {yC:.1f})",
            f"Vertex D: ({xD:.1f}, {yD:.1f})",
            "Vertex A"
        ]
    ))
    
    # Vertex Labels
    fig.add_trace(go.Scatter(
        x=[xA, xB, xC, xD],
        y=[yA, yB, yC, yD],
        mode="text",
        text=["<b>A</b>", "<b>B</b>", "<b>C</b>", "<b>D</b>"],
        textposition=["middle right", "top right", "top left", "bottom left"],
        textfont=dict(color="#FFFFFF", size=15),
        showlegend=False
    ))
    
    # Diagonal x = BD (Base)
    fig.add_trace(go.Scatter(
        x=[xB, xD], y=[yB, yD],
        mode="lines",
        line=dict(color=COLOR_ACCENT, width=3),
        name=f"1st Diagonal x (BD) = {quad.diagonal_x:.2f}"
    ))
    
    # Diagonal y = AC
    fig.add_trace(go.Scatter(
        x=[xA, xC], y=[yA, yC],
        mode="lines",
        line=dict(color=COLOR_PURPLE, width=2, dash="dash"),
        name=f"2nd Diagonal y (AC) = {quad.diagonal_y:.2f}"
    ))
    
    # Altitudes AE and CF onto BD
    xE, yE = pts["E"]
    xF, yF = pts["F"]
    
    fig.add_trace(go.Scatter(
        x=[xA, xE], y=[yA, yE],
        mode="lines+markers",
        line=dict(color=COLOR_GREEN, width=2, dash="dot"),
        marker=dict(size=7, color=COLOR_GREEN),
        name=f"Altitude AE = {quad.altitude_ae:.2f}"
    ))
    
    fig.add_trace(go.Scatter(
        x=[xC, xF], y=[yC, yF],
        mode="lines+markers",
        line=dict(color=COLOR_GREEN, width=2, dash="dot"),
        marker=dict(size=7, color=COLOR_GREEN),
        name=f"Altitude CF = {quad.altitude_cf:.2f}"
    ))
    
    # Interstice segment EF (Lamba-nipatanantara)
    fig.add_trace(go.Scatter(
        x=[xE, xF], y=[yE, yF],
        mode="lines+markers",
        line=dict(color=COLOR_SECONDARY, width=5),
        marker=dict(size=8, color=COLOR_SECONDARY),
        name=f"Interstice EF = {quad.lamba_nipatanantara:.2f}"
    ))
    
    # Altitude feet labels
    fig.add_trace(go.Scatter(
        x=[xE, xF], y=[yE, yF],
        mode="text",
        text=["<b>E</b>", "<b>F</b>"],
        textposition="top center",
        textfont=dict(color=COLOR_SECONDARY, size=12),
        showlegend=False
    ))
    
    margin_lim = r * 1.25
    fig.update_layout(
        title=dict(
            text="<b>Cyclic Quadrilateral Geometric Decomposition (Brahmagupta & Mādhava)</b>",
            font=dict(size=16, color="#FFFFFF"),
            x=0.5
        ),
        xaxis=dict(
            range=[-margin_lim, margin_lim],
            scaleanchor="y", scaleratio=1,
            gridcolor=COLOR_GRID,
            zeroline=False
        ),
        yaxis=dict(
            range=[-margin_lim, margin_lim],
            gridcolor=COLOR_GRID,
            zeroline=False
        ),
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(color="#E5E7EB", size=11)
        ),
        margin=dict(l=40, r=40, t=60, b=80),
        height=550
    )
    
    return fig


def plot_sphere_dissection_3d(radius: float = 10.0, n_slices: int = 30) -> go.Figure:
    """
    Plotly 3D visualization of transparent sphere with stacked cylindrical slices.
    """
    fig = go.Figure()
    r = float(radius)
    n = max(5, int(n_slices))
    
    # 1. Wireframe / Mesh Sphere (translucent)
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 25)
    xs = r * np.outer(np.cos(u), np.sin(v))
    ys = r * np.outer(np.sin(u), np.sin(v))
    zs = r * np.outer(np.ones(np.size(u)), np.cos(v))
    
    fig.add_trace(go.Surface(
        x=xs, y=ys, z=zs,
        opacity=0.2,
        colorscale="Blues",
        showscale=False,
        name=f"Sphere (r={r})",
        hoverinfo="skip"
    ))
    
    # 2. Add horizontal disks/rings for slices
    delta = (2.0 * r) / n
    theta_ring = np.linspace(0, 2 * np.pi, 50)
    
    # Limit number of rendered rings for smooth UI responsiveness
    step = max(1, n // 30)
    for j in range(1, n + 1, step):
        z_mid = -r + (j - 0.5) * delta
        bj = math.sqrt(max(0.0, r**2 - z_mid**2))
        
        rx = bj * np.cos(theta_ring)
        ry = bj * np.sin(theta_ring)
        rz = np.full_like(rx, z_mid)
        
        fig.add_trace(go.Scatter3d(
            x=rx, y=ry, z=rz,
            mode="lines",
            line=dict(
                color=COLOR_PRIMARY,
                width=3
            ),
            showlegend=(j == 1),
            name=f"Slice Slices (N={n})",
            hoverinfo="text",
            hovertext=f"Slice #{j}: Height z = {z_mid:.2f}, Radius B_j = {bj:.2f}"
        ))
        
    fig.update_layout(
        title=dict(
            text=f"<b>3D Sphere Slicing & Pre-Calculus Integration (N = {n} Slices)</b>",
            font=dict(size=16, color="#FFFFFF"),
            x=0.5
        ),
        scene=dict(
            xaxis=dict(title="X", backgroundcolor=COLOR_BG, gridcolor=COLOR_GRID, showbackground=True),
            yaxis=dict(title="Y", backgroundcolor=COLOR_BG, gridcolor=COLOR_GRID, showbackground=True),
            zaxis=dict(title="Z (Height)", backgroundcolor=COLOR_BG, gridcolor=COLOR_GRID, showbackground=True),
            aspectmode="cube"
        ),
        paper_bgcolor=COLOR_BG,
        margin=dict(l=20, r=20, t=50, b=20),
        height=550
    )
    
    return fig


def plot_unrolled_slices_2d(radius: float = 10.0, n_slices: int = 30) -> go.Figure:
    """
    2D unrolled rectangular strip representation of spherical slices (Section 7.18 / Fig 7.21).
    """
    res = compute_sphere_slices(radius, n_slices)
    df = res["slices_df"]
    
    fig = go.Figure()
    
    # Plot bar chart representing the unrolled strips of length C_j and height Delta
    fig.add_trace(go.Bar(
        x=df["slice_index"],
        y=df["slice_circumference"],
        marker=dict(
            color=df["slice_circumference"],
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Slice Circumference", tickfont=dict(color="#FFFFFF"))
        ),
        name="Unrolled Strip Length",
        hovertext=[
            f"Slice {row.slice_index}: Circumference = {row.slice_circumference:.2f}, Strip Area = {row.surface_strip_area:.2f}"
            for _, row in df.iterrows()
        ],
        hoverinfo="text"
    ))
    
    fig.update_layout(
        title=dict(
            text="<b>Unrolled Spherical Surface Strips (Yuktibhāṣā Fig. 7.21)</b>",
            font=dict(size=15, color="#FFFFFF"),
            x=0.5
        ),
        xaxis=dict(
            title="Slice Index (j)",
            gridcolor=COLOR_GRID,
            tickfont=dict(color="#9CA3AF")
        ),
        yaxis=dict(
            title="Unrolled Length (Perimeter 2π·B_j)",
            gridcolor=COLOR_GRID,
            tickfont=dict(color="#9CA3AF")
        ),
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        margin=dict(l=40, r=40, t=50, b=50),
        height=400
    )
    
    return fig

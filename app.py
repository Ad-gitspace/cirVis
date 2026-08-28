"""
Kerala School of Mathematics - Chapter 7: Derivation of Sines (Yuktibhāṣā)
Interactive Simulation & Mathematical Computing Suite in Streamlit
"""

import math
import streamlit as st
import pandas as pd
import numpy as np

# Engine imports
from src.engine_trig import (
    TOTAL_CIRCUMFERENCE,
    RADIUS_EXACT,
    RADIUS_KATAPAYADI,
    ARC_BIT_ALPHA,
    deg_min_sec_to_minutes,
    minutes_to_deg_min_sec,
    format_sexagesimal,
    minutes_to_radians,
    radians_to_minutes,
    jya,
    koti_jya,
    sara,
    compute_24_tabular_rsines,
    interpolate_sista_capa,
    jive_paraspara_nyaya,
)
from src.engine_sankalita import (
    sankalita_1,
    sankalita_2,
    sankalita_k,
    madhava_rsine_series_terms,
    madhava_rversine_series_terms,
    discrete_sankalita_step_derivation,
    generate_series_convergence_curves,
)
from src.engine_quadrilaterals import CyclicQuadrilateral
from src.engine_sphere import (
    compute_sphere_slices,
    generate_sphere_convergence_data,
)
from src.visualizers import (
    plot_trig_circle,
    plot_sankalita_convergence,
    plot_cyclic_quadrilateral,
    plot_sphere_dissection_3d,
    plot_unrolled_slices_2d,
)

# Page configuration
st.set_page_config(
    page_title="Kerala Mathematics: Yuktibhāṣā Simulation Suite",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00D4FF, #9B5DE5, #FF6B6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #9CA3AF;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #1F2937;
        border: 1px solid #374151;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #9CA3AF;
        text-transform: uppercase;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.4rem;
        color: #00D4FF;
        font-weight: 700;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #D1D5DB;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #111827;
        border-radius: 6px 6px 0 0;
        padding: 10px 16px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.markdown("## ⚙️ Global Configuration")
radius_option = st.sidebar.radio(
    "Radius Definition (r):",
    ["Exact (21600 / 2π ≈ 3437.7468')", "Katapayadi Verse (3437' 44'' 48''' ≈ 3437.7467')"],
    index=0
)
current_radius = RADIUS_EXACT if "Exact" in radius_option else RADIUS_KATAPAYADI

st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Historical Context")
st.sidebar.info(
    "**Yuktibhāṣā (c. 1530 CE)** by *Jyeṣṭhadeva*\n\n"
    "Rationales for the Kerala School discoveries (Mādhava of Saṅgamagrāma, Nīlakaṇṭha Somayājī, Parameśvara):\n"
    "- 24 Tabular Sines (*Paṭhita-jyā*)\n"
    "- Infinite Series via *Saṅkalita* (Pre-Newton/Leibniz Calculus)\n"
    "- Cyclic Quadrilateral 3 Diagonals & Circum-Radius\n"
    "- Spherical Slicing Integration"
)

# Header Section
st.markdown('<div class="main-header">Kerala School of Mathematics Simulation Suite</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive 2D/3D Mathematical Visualization & Computing Platform based on <b>Yuktibhāṣā (Chapter 7: Derivation of Sines)</b></div>', unsafe_allow_html=True)

# 4 Main Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📐 1. 24 Tabular Sines & Trigonometry",
    "♾️ 2. Calculus via Saṅkalita (Madhava Series)",
    "🔷 3. Cyclic Quadrilaterals (Brahmagupta & Mādhava)",
    "🌐 4. 3D Sphere Pre-Calculus Integration"
])

# ---------------------------------------------------------
# TAB 1: 24 Tabular Sines & Trigonometry
# ---------------------------------------------------------
with tab1:
    st.markdown("### 1. Ancient Trigonometry: Tabular Rsines (*Paṭhita-jyā*) & Angle Addition (*Jīve-paraspara-nyāya*)")
    
    sub_tab1, sub_tab2, sub_tab3 = st.tabs([
        "Interactive Circle & Śiṣṭa-cāpa Interpolation",
        "24 Tabular Sines Master Table",
        "Jīve-paraspara-nyāya (Angle Addition)"
    ])
    
    with sub_tab1:
        c1, c2 = st.columns([1, 1.4])
        with c1:
            st.markdown("#### Input Arc / Angle")
            input_mode = st.radio("Input Format:", ["Arcminutes (s)", "Degrees (°)", "DMS (Deg, Min, Sec)"], horizontal=True)
            
            if input_mode == "Arcminutes (s)":
                s_input = st.slider("Arc length $s$ (minutes):", min_value=0.0, max_value=5400.0, value=1125.0, step=15.0)
            elif input_mode == "Degrees (°)":
                deg_val = st.slider("Angle $\\theta$ (degrees):", min_value=0.0, max_value=90.0, value=18.75, step=0.25)
                s_input = deg_val * 60.0
            else:
                col_d, col_m, col_s = st.columns(3)
                with col_d:
                    d_in = st.number_input("Deg", min_value=0, max_value=90, value=18)
                with col_m:
                    m_in = st.number_input("Min", min_value=0, max_value=59, value=45)
                with col_s:
                    s_sec_in = st.number_input("Sec", min_value=0.0, max_value=59.9, value=0.0)
                s_input = deg_min_sec_to_minutes(d_in, m_in, s_sec_in)
                
            interp_order = st.selectbox("Interpolation Order (Taylor-Madhava):", [1, 2, 3], index=1)
            interp_res = interpolate_sista_capa(s_input, r=current_radius, order=interp_order)
            
            st.markdown("#### Live Computed Values")
            mc1, mc2 = st.columns(2)
            with mc1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Jyā (Rsine)</div>
                    <div class="metric-value">{interp_res['approx_rsine']:.3f}'</div>
                    <div class="metric-sub">Sexagesimal: {format_sexagesimal(interp_res['approx_rsine'])}</div>
                    <div class="metric-sub">Abs Error: {interp_res['error_rsine']:.3e}'</div>
                </div>
                """, unsafe_allow_html=True)
            with mc2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Koṭi-jyā (Rcosine)</div>
                    <div class="metric-value">{interp_res['approx_rcosine']:.3f}'</div>
                    <div class="metric-sub">Sexagesimal: {format_sexagesimal(interp_res['approx_rcosine'])}</div>
                    <div class="metric-sub">Abs Error: {interp_res['error_rcosine']:.3e}'</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Śiṣṭa-cāpa (Remainder Arc Δ)</div>
                <div class="metric-value">{interp_res['sista_capa_delta']:+.2f}'</div>
                <div class="metric-sub">Nearest Tabular Node: #{interp_res['nearest_tabular_index']} ({interp_res['nearest_tabular_arc']:.0f}')</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.latex(r"R\sin(s_i + \Delta) \approx R\sin(s_i) + \left(\frac{\Delta}{r}\right) R\cos(s_i) - \frac{1}{2}\left(\frac{\Delta}{r}\right)^2 R\sin(s_i)")

        with c2:
            fig_trig = plot_trig_circle(s_input, r=current_radius)
            st.plotly_chart(fig_trig, use_container_width=True)

    with sub_tab2:
        st.markdown("#### The 24 Canonical Tabular Rsines (*Paṭhita-jyā*) of Kerala Astronomy")
        st.caption("Each step is $\\alpha = 225' = 3^\\circ 45'$. Tabulated up to $90^\\circ$ ($5400'$).")
        df_24 = compute_24_tabular_rsines(r=current_radius)
        st.dataframe(df_24, use_container_width=True, hide_index=True)
        
        st.download_button(
            "📥 Export Tabular Sines to CSV",
            data=df_24.to_csv(index=False).encode("utf-8"),
            file_name="kerala_24_tabular_sines.csv",
            mime="text/csv"
        )
        
        st.markdown("""
        **Second-Order Difference Relation (Khaṇḍa-jyāntara):**
        $$\\Delta_j - \\Delta_{j+1} = \\left(\\frac{\\alpha}{r}\\right)^2 B_j$$
        *(Aryabhaṭīya Ganita 12, Tantrasaṅgraha 2.4, Yuktibhāṣā 7.50)*
        """)

    with sub_tab3:
        st.markdown("#### Mādhava's Addition Theorem (*Jīve-paraspara-nyāya*)")
        st.latex(r"R\sin(s_1 \pm s_2) = \frac{1}{r} [R\sin(s_1) R\cos(s_2) \pm R\cos(s_1) R\sin(s_2)]")
        
        jc1, jc2 = st.columns([1, 1.4])
        with jc1:
            s1_val = st.slider("Arc $s_1$ (arcminutes):", 0.0, 3600.0, 1800.0, step=75.0, help="1800' = 30°")
            s2_val = st.slider("Arc $s_2$ (arcminutes):", 0.0, 1800.0, 900.0, step=75.0, help="900' = 15°")
            op_val = st.radio("Operation:", ["add (+)", "subtract (-)"], horizontal=True)
            op_key = "add" if "add" in op_val else "sub"
            
            jive_res = jive_paraspara_nyaya(s1_val, s2_val, operation=op_key, r=current_radius)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Computed Combined Rsine</div>
                <div class="metric-value">{jive_res['computed_rsine']:.3f}'</div>
                <div class="metric-sub">Target Arc: {jive_res['target_arc']:.1f}' ({jive_res['target_arc']/60.0:.2f}°)</div>
                <div class="metric-sub">Modern Exact: {jive_res['exact_rsine']:.3f}'</div>
                <div class="metric-sub">Precision Error: {jive_res['error_rsine']:.2e}'</div>
            </div>
            """, unsafe_allow_html=True)
        with jc2:
            fig_jive = plot_trig_circle(s1_val, s2_val, mode="jive_paraspara", r=current_radius)
            st.plotly_chart(fig_jive, use_container_width=True)

# ---------------------------------------------------------
# TAB 2: Calculus via Saṅkalita (Madhava Series)
# ---------------------------------------------------------
with tab2:
    st.markdown("### 2. Derivation of Power Series via Saṅkalita (Repeated Summations)")
    
    sc1, sc2 = st.columns([1, 1.4])
    with sc1:
        st.markdown("#### Parameters for Series Expansion")
        s_sank_deg = st.slider("Test Angle $\\theta$ (degrees):", 1.0, 90.0, 45.0, step=1.0)
        s_sank = s_sank_deg * 60.0
        n_part = st.slider("Partitions for Discrete Summation ($n$):", 5, 200, 50, step=5)
        
        discrete_res = discrete_sankalita_step_derivation(s_sank, n_partitions=n_part, r=current_radius)
        terms = madhava_rsine_series_terms(s_sank, r=current_radius, max_order=9)
        exact_val = current_radius * math.sin(s_sank / current_radius)
        
        st.markdown("#### Mādhava Polynomial Terms at Selected Point")
        st.markdown(f"""
        - **Order 1 ($s$):** `{terms[1]:.4f}'` (Error: `{abs(terms[1]-exact_val):.2e}`)
        - **Order 3 ($s - s^3/6r^2$):** `{terms[3]:.4f}'` (Error: `{abs(terms[3]-exact_val):.2e}`)
        - **Order 5 ($+ s^5/120r^4$):** `{terms[5]:.4f}'` (Error: `{abs(terms[5]-exact_val):.2e}`)
        - **Order 7 ($- s^7/5040r^6$):** `{terms[7]:.4f}'` (Error: `{abs(terms[7]-exact_val):.2e}`)
        - **Order 9 ($+ s^9/362880r^8$):** `{terms[9]:.4f}'` (Error: `{abs(terms[9]-exact_val):.2e}`)
        """)
        
        st.markdown("#### Saṅkalita Asymptotics ($n \\to \\infty$)")
        st.latex(r"V_n^{(1)} = \sum_{j=1}^n j = \frac{n(n+1)}{2} \approx \frac{n^2}{2}")
        st.latex(r"V_n^{(2)} = \sum_{j=1}^n V_j^{(1)} = \frac{n(n+1)(n+2)}{6} \approx \frac{n^3}{6}")
        st.latex(r"V_n^{(k)} \approx \frac{n^{k+1}}{(k+1)!}")
        
    with sc2:
        fig_sank = plot_sankalita_convergence(s_selected_min=s_sank, r=current_radius)
        st.plotly_chart(fig_sank, use_container_width=True)

# ---------------------------------------------------------
# TAB 3: Cyclic Quadrilaterals
# ---------------------------------------------------------
with tab3:
    st.markdown("### 3. Cyclic Quadrilateral Mechanics (Brahmagupta, Mādhava & Parameśvara)")
    
    qc1, qc2 = st.columns([1, 1.4])
    with qc1:
        st.markdown("#### Quadrilateral Sides ($a, b, c, d$)")
        
        preset = st.selectbox("Preset Configurations:", ["Līlāvatī 171 Problem", "Symmetric Kite", "Custom"], index=0)
        
        if preset == "Līlāvatī 171 Problem":
            def_a, def_b, def_c, def_d = 75.0, 40.0, 51.0, 68.0
        elif preset == "Symmetric Kite":
            def_a, def_b, def_c, def_d = 60.0, 60.0, 40.0, 40.0
        else:
            def_a, def_b, def_c, def_d = 50.0, 40.0, 30.0, 45.0
            
        side_a = st.number_input("Side a (AB):", min_value=1.0, max_value=200.0, value=def_a, step=1.0)
        side_b = st.number_input("Side b (BC):", min_value=1.0, max_value=200.0, value=def_b, step=1.0)
        side_c = st.number_input("Side c (CD):", min_value=1.0, max_value=200.0, value=def_c, step=1.0)
        side_d = st.number_input("Side d (DA):", min_value=1.0, max_value=200.0, value=def_d, step=1.0)
        
        quad = CyclicQuadrilateral(side_a, side_b, side_c, side_d)
        
        if quad.is_valid:
            st.markdown("#### Computed Invariants")
            q_col1, q_col2 = st.columns(2)
            with q_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Brahmagupta Area</div>
                    <div class="metric-value">{quad.area:.3f}</div>
                    <div class="metric-sub">Semi-perimeter s = {quad.s:.1f}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">1st Diagonal x (BD)</div>
                    <div class="metric-value">{quad.diagonal_x:.3f}</div>
                </div>
                """, unsafe_allow_html=True)
            with q_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Parameśvara Radius (r)</div>
                    <div class="metric-value">{quad.circum_radius:.3f}</div>
                    <div class="metric-sub">Circum-diameter d = {quad.circum_diameter:.3f}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">2nd Diagonal y (AC)</div>
                    <div class="metric-value">{quad.diagonal_y:.3f}</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Lamba-nipātāntara (Altitude Interstice EF)</div>
                <div class="metric-value">{quad.lamba_nipatanantara:.3f}</div>
                <div class="metric-sub">Altitudes: AE = {quad.altitude_ae:.2f}, CF = {quad.altitude_cf:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.latex(r"EF = \frac{(a^2 + c^2) - (b^2 + d^2)}{2x}")
            st.latex(r"A = \sqrt{(s-a)(s-b)(s-c)(s-d)}")
            st.latex(r"r = \frac{1}{4}\sqrt{\frac{(ab+cd)(ac+bd)(ad+bc)}{(s-a)(s-b)(s-c)(s-d)}}")
        else:
            st.error(quad.validation_message)
            
    with qc2:
        fig_quad = plot_cyclic_quadrilateral(quad)
        st.plotly_chart(fig_quad, use_container_width=True)

# ---------------------------------------------------------
# TAB 4: 3D Sphere Slicing & Pre-Calculus Integration
# ---------------------------------------------------------
with tab4:
    st.markdown("### 4. Surface Area & Volume of Sphere via Pre-Calculus Slicing (Yuktibhāṣā 7.18 - 7.19)")
    
    spc1, spc2 = st.columns([1, 1.4])
    with spc1:
        st.markdown("#### Slicing Configuration")
        sp_r = st.slider("Sphere Radius ($R$):", 1.0, 50.0, 10.0, step=1.0)
        sp_n = st.slider("Number of Cylindrical Slices ($N$):", 5, 200, 30, step=5)
        
        sp_res = compute_sphere_slices(sp_r, sp_n)
        
        st.markdown("#### Integration Convergence Metrics")
        sm1, sm2 = st.columns(2)
        with sm1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Discrete Surface Area</div>
                <div class="metric-value">{sp_res['discrete_surface_area']:.2f}</div>
                <div class="metric-sub">Exact (4πR²): {sp_res['exact_surface_area']:.2f}</div>
                <div class="metric-sub">Error: {sp_res['sa_relative_error_pct']:.3f}%</div>
            </div>
            """, unsafe_allow_html=True)
        with sm2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Discrete Volume</div>
                <div class="metric-value">{sp_res['discrete_volume']:.2f}</div>
                <div class="metric-sub">Exact (4/3 πR³): {sp_res['exact_volume']:.2f}</div>
                <div class="metric-sub">Error: {sp_res['vol_relative_error_pct']:.3f}%</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("#### Analytical Theorems")
        st.latex(r"S = \sum_{j=1}^N \left(\frac{C}{r}\right) B_j \Delta \xrightarrow{N \to \infty} C \times d = 4\pi r^2")
        st.latex(r"V = \frac{1}{2} \sum_{j=1}^N \left(\frac{C}{r}\right) B_j^2 \Delta \xrightarrow{N \to \infty} \frac{1}{6} C d^2 = \frac{4}{3}\pi r^3")
        
    with spc2:
        fig_sp3d = plot_sphere_dissection_3d(sp_r, sp_n)
        st.plotly_chart(fig_sp3d, use_container_width=True)
        
        fig_strip = plot_unrolled_slices_2d(sp_r, sp_n)
        st.plotly_chart(fig_strip, use_container_width=True)
        
    st.markdown("#### Convergence Analysis Table ($N = 5 \\dots 1000$)")
    df_conv = generate_sphere_convergence_data(sp_r)
    st.dataframe(df_conv, use_container_width=True, hide_index=True)

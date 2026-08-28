You are an expert mathematical computing and scientific visualization engineer. Your task is to build a complete, production-grade interactive simulation and visualization suite in Python based on the Kerala School of Mathematics (Chapter 7: Derivation of Sines from Yuktibhāṣā).

### Core Goals:
1. High numerical accuracy using exact sexagesimal units (degrees, arcminutes, arcseconds) and standard floating-point precision.
2. Highly responsive 2D and 3D interactive visualizations using Plotly and Streamlit.
3. Modular, readable, and clean Python code with step-by-step mathematical validations.

---

### Implementation Requirements:

#### Module 1: `src/engine_trig.py` (Ancient Trigonometry Engine)
- Radius definition: R = 3437.74677 arcminutes (circumference = 21600 arcminutes).
- Implement sexagesimal converters: (degrees, minutes, seconds) <-> radians <-> arcminutes.
- Compute the 24 tabular Rsines (Pathita-jyā) for increments of 225' (3°45') using:
  1. Base values: R*sin(30°) = R/2, R*sin(45°) = sqrt(R^2/2).
  2. Half-arc and complementary-arc formulas:
     R*sin(s/2) = 0.5 * sqrt(R*sin(s)^2 + R*vers(s)^2)
     R*cos(s) = sqrt(R^2 - R*sin(s)^2)
- Implement interpolation for arbitrary arcs (śiṣṭa-cāpa) up to 2nd order Taylor-Madhava corrections:
  R*sin(s_i + Δ) ≈ R*sin(s_i) + (Δ/R)*R*cos(s_i) - 0.5*(Δ/R)^2 * R*sin(s_i)

#### Module 2: `src/engine_sankalita.py` (Calculus & Repeated Summations)
- Implement discrete Saṅkalita functions:
  - 1st summation: V_n^(1) = n(n+1)/2 ≈ n^2/2
  - 2nd summation: V_n^(2) = n(n+1)(n+2)/6 ≈ n^3/6
  - k-th summation: V_n^(k) ≈ n^(k+1)/(k+1)!
- Implement the recursive derivation of the Madhava-Taylor power series for Rsine and Rversine:
  - Step 1: Arc approximation B_j ≈ j*s/n
  - Step 2: 1st Śara correction S ≈ (1/R) * s^2 / 2!
  - Step 3: 1st Jyā-cāpāntara correction B ≈ s - (1/R^2) * s^3 / 3!
  - Step 4: Higher-order terms up to s^7/7! and s^6/6!
- Output real-time residual error curves comparing Madhava series (order 1 to 5) against modern `numpy.sin(x)`.

#### Module 3: `src/engine_quadrilaterals.py` (Cyclic Quadrilateral Solver)
- Given four cyclic sides a, b, c, d:
  - Calculate semi-perimeter s = (a+b+c+d)/2.
  - Calculate 3 diagonals:
    x = sqrt(((a*b + c*d)*(a*c + b*d)) / (a*d + b*c))
    y = sqrt(((a*c + b*d)*(a*d + b*c)) / (a*b + c*d))
    z = sqrt(((a*b + c*d)*(a*d + b*c)) / (a*c + b*d))
  - Compute Brahmagupta Area: A = sqrt((s-a)(s-b)(s-c)(s-d)).
  - Compute Parameśvara Circum-radius: r = 0.25 * sqrt(((a*b+c*d)*(a*c+b*d)*(a*d+b*c)) / ((s-a)*(s-b)*(s-c)*(s-d))).
  - Compute altitude intercepts (ābādhā) and interstice between altitudes (lamba-nipātāntara):
    EF = 0.5 * ((a^2 + c^2) - (b^2 + d^2)) / x.

#### Module 4: `src/engine_sphere.py` (3D Slicing & Pre-Calculus Integration)
- Discretize a sphere of radius R into N horizontal cylindrical slices.
- Compute for each slice j:
  - Height z_j, slice radius B_j = sqrt(R^2 - z_j^2), thickness Δ = 2R/N.
  - Surface trapezoid unrolling into rectangular strips: Area_j ≈ (C/R) * B_j * Δ.
  - Sliced volume sum: V_N = 0.5 * (C/R) * sum(B_j^2) * Δ.
- Provide theoretical vs discrete convergence data:
  - Volume error: |V_N - (4/3)*pi*R^3| as N -> 1000.
  - Surface area error: |S_N - 4*pi*R^2| as N -> 1000.

#### Module 5: `src/visualizers.py` & `app.py` (Interactive Dashboard)
- Build a polished Streamlit application with a sidebar containing 4 core tabs:
  1. Tab 1: **24-Tabular Sines & Jīve-paraspara-nyāya**
     - Interactive circle with movable arc points (s1, s2).
     - Visual chord segments, Rsine, Rcosine, and Rversine arrows.
     - Live readout comparing ancient tabular values against modern trigonometric evaluations.
  2. Tab 2: **Calculus via Saṅkalita (Series Convergence)**
     - Sliders for arc length `s` and number of partitions `n`.
     - Real-time Plotly graph showing step-by-step convergence of Madhava polynomial terms to sin(x).
  3. Tab 3: **Cyclic Quadrilateral Visual Prover**
     - Sliders for 4 side lengths (validating triangle inequality for cyclic embedding).
     - Plotly dynamic cyclic polygon with drawn diagonals, altitudes, and circumcircle.
     - Data table displaying Brahmagupta area, 3 diagonals, and circum-radius.
  4. Tab 4: **3D Sphere Dissection & Integration**
     - Plotly 3D scatter/mesh showing transparent sphere with N stacked cylindrical disks.
     - Slider for N (5 to 200).
     - Animated/toggled flat projection of the unrolled surface slices proving S = 4*pi*R^2.

---

### Step-by-Step Build Order:
1. Create `requirements.txt` (`streamlit`, `plotly`, `numpy`, `sympy`, `mpmath`).
2. Write unit-tested math engine modules in `src/`.
3. Create Plotly visual rendering pipelines in `src/visualizers.py`.
4. Assemble the UI layout in `app.py`.
5. Run tests to confirm zero precision errors.
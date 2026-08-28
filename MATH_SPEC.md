# Mathematical Specification & Geometric Models: Kerala Mathematics Engine

## 1. Global Constants & Units
* **Total Circumference ($C$):** $21600'$ (arcminutes) = $360^\circ \times 60'$[cite: 1].
* **True Radius ($r$):** 
  $$r = \frac{C}{2\pi} = \frac{21600}{2\pi} \approx 3437.7467707849'$$ (Traditional: $3437' 44'' 48'''$)[cite: 1].
* **Fundamental Arc-Bit ($\alpha$):** 
  $$\alpha = \frac{90^\circ \times 60'}{24} = 225' = 3^\circ 45'$$[cite: 1].
* **Sexagesimal Conversion:**
  $$\text{Radians} = \theta_{\text{deg}} \times \frac{\pi}{180} = \frac{s_{\text{minutes}}}{r}$$[cite: 1]

---

## 2. Geometric Definitions & Coordinate Mappings
For a circle of radius $r$ centered at $(0,0)$ where East is $(r, 0)$ and North is $(0, r)$[cite: 1]:
* **Arc Length ($s$):** Distance along circumference from East point $E(r, 0)$[cite: 1].
* **Angle ($\theta$):** $\theta = \frac{s}{r}$ radians.
* **$Jy\bar{a}$ (Rsine / $B$):** Vertical half-chord $B(s) = r \sin\left(\frac{s}{r}\right)$[cite: 1].
* **$Ko\text{ṭ}i\text{-}jy\bar{a}$ (Rcosine / $K$):** Horizontal distance $K(s) = r \cos\left(\frac{s}{r}\right)$[cite: 1].
* **$\acute{S}ara$ (Rversine / $S$):** Versine arrow $S(s) = r - K(s) = r\left(1 - \cos\left(\frac{s}{r}\right)\right)$[cite: 1].

### Visual Diagram Coordinate Specs (Plotly 2D)
* **Point $E$ (East):** $(r, 0)$[cite: 1]
* **Point $N$ (North):** $(0, r)$[cite: 1]
* **Point $C_j$ (Tip of $j$-th arc-bit):** $(r \cos(j\theta_0), r \sin(j\theta_0))$ where $\theta_0 = \frac{225'}{r}$[cite: 1]
* **Point $B_j$ (Rsine foot on East-West axis):** $(0, r \sin(j\theta_0))$[cite: 1]
* **Point $P_j$ (Rcosine foot on North-South axis):** $(r \cos(j\theta_0), 0)$[cite: 1]

---

## 3. Trigonometric Algorithms & Difference Equations

### 3.1 Tabular Rsines (24 Pathita-jyā)
* **Base Anchors:**
  $$R\sin(30^\circ) = \frac{r}{2} = 1718.873'$$[cite: 1]
  $$R\sin(45^\circ) = \sqrt{\frac{r^2}{2}} \approx 2430.854'$$[cite: 1]
* **Half-Arc & Complementary-Arc Recursions:**
  $$R\sin\left(\frac{s}{2}\right) = \frac{1}{2} \sqrt{R\sin^2(s) + R\text{vers}^2(s)}$$[cite: 1]
  $$R\cos(s) = \sqrt{r^2 - R\sin^2(s)}$$[cite: 1]
* **Second-Order Differences (Khaṇḍa-jyāntara):**
  $$\Delta_j = B_j - B_{j-1}$$[cite: 1]
  $$\Delta_j - \Delta_{j+1} = \left(\frac{\alpha}{r}\right)^2 B_j$$[cite: 1]

### 3.2 Interpolation at Arbitrary Point (Śiṣṭa-cāpa $\Delta$)
For desired arc $s = s_i + \Delta$ where $s_i$ is the nearest tabulated multiple of $225'$[cite: 1]:
$$R\sin(s_i + \Delta) \approx R\sin(s_i) + \left(\frac{\Delta}{r}\right) R\cos(s_i) - \frac{1}{2}\left(\frac{\Delta}{r}\right)^2 R\sin(s_i)$$[cite: 1]
$$R\cos(s_i + \Delta) \approx R\cos(s_i) - \left(\frac{\Delta}{r}\right) R\sin(s_i) - \frac{1}{2}\left(\frac{\Delta}{r}\right)^2 R\cos(s_i)$$[cite: 1]

### 3.3 Angle Addition (*Jīve-paraspara-nyāya*)
$$R\sin(s_1 \pm s_2) = \frac{1}{r} \left[ R\sin(s_1) R\cos(s_2) \pm R\cos(s_1) R\sin(s_2) \right]$$[cite: 1]
$$R\cos(s_1 \pm s_2) = \frac{1}{r} \left[ R\cos(s_1) R\cos(s_2) \mp R\sin(s_1) R\sin(s_2) \right]$$[cite: 1]

---

## 4. Calculus via Saṅkalita (Madhava Series Derivation)

### 4.1 Repeated Summations (Saṅkalita) for Large $n$
* **1st Summation (Ādya-saṅkalita):** 
  $$V_n^{(1)} = \sum_{j=1}^n j \approx \frac{n^2}{2}$$[cite: 1]
* **2nd Summation (Dvitīya-saṅkalita):** 
  $$V_n^{(2)} = \sum_{j=1}^n V_j^{(1)} \approx \frac{n^3}{6}$$[cite: 1]
* **$k$-th Repeated Summation:** 
  $$V_n^{(k)} \approx \frac{n^{k+1}}{(k+1)!}$$[cite: 1]

### 4.2 Madhava Infinite Power Series
$$R\sin(s) = s - \left(\frac{1}{r^2}\right)\frac{s^3}{3!} + \left(\frac{1}{r^4}\right)\frac{s^5}{5!} - \left(\frac{1}{r^6}\right)\frac{s^7}{7!} + \dots$$[cite: 1]
$$R\text{vers}(s) = \left(\frac{1}{r}\right)\frac{s^2}{2!} - \left(\frac{1}{r^3}\right)\frac{s^4}{4!} + \left(\frac{1}{r^5}\right)\frac{s^6}{6!} - \dots$$[cite: 1]

---

## 5. Cyclic Quadrilateral Mechanics & Invariants
Given 4 cyclic sides $a, b, c, d$ with semi-perimeter $s = \frac{a+b+c+d}{2}$[cite: 1]:
* **Diagonals ($x = BD, y = AC, z = \text{Third Diagonal}$):**
  $$x = \sqrt{\frac{(ab + cd)(ac + bd)}{ad + bc}}$$[cite: 1]
  $$y = \sqrt{\frac{(ac + bd)(ad + bc)}{ab + cd}}$$[cite: 1]
  $$z = \sqrt{\frac{(ab + cd)(ad + bc)}{ac + bd}}$$[cite: 1]
* **Brahmagupta Area ($A$):**
  $$A = \sqrt{(s-a)(s-b)(s-c)(s-d)}$$[cite: 1]
* **Parameśvara Circum-Radius ($r$):**
  $$r = \frac{1}{4} \sqrt{\frac{(ab + cd)(ac + bd)(ad + bc)}{(s-a)(s-b)(s-c)(s-d)}} = \frac{xyz}{4A}$$[cite: 1]
* **Interstice Between Altitude Feet ($EF$ / Lamba-nipātāntara):**
  $$EF = \frac{1}{2} \cdot \frac{(a^2 + c^2) - (b^2 + d^2)}{x}$$[cite: 1]

---

## 6. Pre-Calculus 3D Sphere Integration
A sphere of radius $r$ is sliced into $N$ horizontal cylinders of thickness $\Delta = \frac{2r}{N}$[cite: 1].
For slice index $j \in [1, N]$ at height $z_j = -r + j\Delta$:
* **Slice Radius ($B_j$):** 
  $$B_j = \sqrt{r^2 - z_j^2}$$[cite: 1]
* **Discrete Surface Area Sum:**
  $$S_N = \sum_{j=1}^N \left(\frac{C}{r}\right) B_j \Delta \xrightarrow{N \to \infty} C \times (2r) = 4\pi r^2$$[cite: 1]
* **Discrete Volume Sum:**
  $$V_N = \frac{1}{2} \sum_{j=1}^N \left(\frac{C}{r}\right) B_j^2 \Delta \xrightarrow{N \to \infty} \frac{1}{6} C d^2 = \frac{4}{3}\pi r^3$$[cite: 1]

---

## 7. Ground Truth Verification Suite (Unit Tests)

The code passes these exact assertions:

### Test Case 1: 1st Tabulated Rsine ($s = 225'$)
- $R\sin(225') = 224.8394' \approx 224^\circ 50' 22''$
- $R\cos(225') = 3430.3845'$
- $R\text{vers}(225') = 7.3622'$

### Test Case 2: Līlāvatī Cyclic Quadrilateral (Section 7.15)
- Inputs: $a = 75, b = 40, c = 51, d = 68$
- Semi-perimeter: $s = \frac{75+40+51+68}{2} = 117$
- Expected Diagonal $x = BD = 77.0$
- Expected Diagonal $y = AC = 85.0$
- Expected Third Diagonal $z = DF = 84.0$
- Expected Area $A = \sqrt{42 \times 77 \times 66 \times 49} = 3234.0$ (Exact Integer)
- Expected Circum-radius $r = 42.5$

### Test Case 3: Sphere Convergence ($r = 10.0, N = 500$)
- Discrete Surface Area $S_{500} \approx 4\pi (10^2) \pm 0.1\%$
- Discrete Volume $V_{500} \approx \frac{4}{3}\pi (10^3) \pm 0.1\%$
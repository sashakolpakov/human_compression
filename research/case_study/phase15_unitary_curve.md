# A twisted elliptic curve for primitive middle rotations

10 October 2026. Original phase-fifteen proposed argument. This note gives the geometric and character-sieve inequality; the all-field arithmetic completion and independent reviews are separate companion records.

Let $q\equiv3\pmod4$ and $N=q^2-1$. We seek a primitive $\lambda\in\mathbb F_{q^2}^*$ with

$$\operatorname{Norm}_{q^2/q}(\lambda-\lambda^{-1})=-2.$$

The preceding [parameter reduction](phase15_unitary_parameter_reduction.md) turns such a solution into a rank-four string C-group for $\operatorname{PSU}_4(q)$ whenever $q\ge27$.

## 1. The genus-one curve and its field structure

Over the algebraic closure, put

$$F(x,y)=(x^2-1)(y^2-1)+2xy.$$

Its closure in $\mathbb P^1\times\mathbb P^1$ has bidegree $(2,2)$. Give it the $\mathbb F_q$-structure whose geometric Frobenius on coordinates interchanges the two factors and raises their entries to the $q$th power. Its rational points satisfy $y=x^q$, and hence the displayed equation is exactly the required norm equation when $x\ne0,\infty$.

For characteristic other than two or three this curve is smooth. On the affine chart the derivative equations are

$$x(y^2-1)+y=0,\qquad y(x^2-1)+x=0.$$

Neither coordinate can be zero at an affine singular point. Adding the derivative equations gives $xy(x+y)=0$, hence $y=-x$. The first derivative equation then gives $x^2=2$, and substitution in $F$ gives $-3=0$. Thus singularities occur only in characteristic three. The four boundary pairs are also smooth: at $x=0$ or infinity one has $y=\pm1$, and the derivative in the transverse $y$ direction is nonzero; likewise with $x,y$ exchanged. A smooth bidegree $(2,2)$ curve is geometrically connected and has genus one. Thus Hasse–Weil gives

$$\bigl|\#C(\mathbb F_q)-(q+1)\bigr|\le2\sqrt q.$$

The complement of the open torus consists of eight distinct points:

$$x=0,\infty,\ y=\pm1;\qquad y=0,\infty,\ x=\pm1.$$

Every zero and pole of $x$ or $y$ is simple, and the supports for the two functions are disjoint. None of these eight points is rational in the twisted field structure: the condition $y=x^q$ would require a zero coordinate to be paired with zero, or infinity with infinity, neither of which occurs. Consequently every rational point contributes an element $x\in\mathbb F_{q^2}^*$; there is no rational boundary correction.

## 2. Exact order of the character local systems

Let $T=\operatorname{Res}_{\mathbb F_{q^2}/\mathbb F_q}\mathbb G_m$. Geometrically $T=\mathbb G_m^2$, with Frobenius $(x,y)\mapsto(y^q,x^q)$. Its Lang isogeny has exponent matrix

$$\begin{pmatrix}1&-q\\-q&1\end{pmatrix}.$$

The kernel is $T(\mathbb F_q)=\mathbb F_{q^2}^*$, a cyclic group of order $N$. In the cokernel of the exponent matrix, the two coordinate classes differ by multiplication by $q$, and each generates the cyclic group of order $N$. Therefore the character sheaf associated to a character $\chi$ of $\mathbb F_{q^2}^*$ has geometric local monodromies of exact order $\operatorname{ord}(\chi)$ on both coordinate factors. Equivalently the two characters are $\chi$ and $\chi^q$, up to inverses depending on the Lang convention; none of this changes their orders.

Pull back this local system along the curve. If $\chi$ is nontrivial, the eight simple zeros and poles in §1 are all genuinely ramified: the two supports are disjoint, and their multiplicity one does not kill any character order, including even orders. The sheaf is rank one, tame, finite-monodromy and geometrically nonconstant. On a genus-one curve with eight punctures, $H_c^0=H_c^2=0$ and the compactly supported Euler characteristic is $-8$. Hence $\dim H_c^1=8$. The trace formula and weight bound yield

$$\left|\sum_{P\in C(\mathbb F_q)}\chi(x(P))\right|\le8\sqrt q\qquad(\chi\ne1).$$

The retained input is the same rank-one tame trace/Euler/weight machinery directly inspected in the earlier phases: [Katz, *Gauss Sums, Kloosterman Sums, and Monodromy Groups*](https://web.math.princeton.edu/~nmk/Katz-GKM.pdf), §§2.3.1–2.3.2, §3.6.1 and its proof, and §4.3. The Lang-lattice calculation and the eight ramification points are the present application; the Weil bound is not reproved here.

## 3. Primitive and core-sieve bounds

Write $W(n)=2^{\omega(n)}$ and $\theta(n)=\varphi(n)/n$. The standard primitive-character identity on the cyclic group of order $N$ gives, for the number $P_N$ of primitive values at rational points,

$$P_N\ge\theta(N)\bigl(q+1-(8W(N)-6)\sqrt q\bigr).$$

Indeed, the principal term is at least $q+1-2\sqrt q$, while the total absolute coefficient mass of all nonprincipal terms is $W(N)-1$. Positivity is therefore a sufficient existence criterion.

More economically, let $a$ be a squarefree product of some prime divisors of $N$, and list the omitted primes as $p_1,\ldots,p_s$. Put

$$\delta=1-\sum_{j=1}^s1/p_j>0.$$

The elementary lower sieve for being a non-power for every prime gives positivity whenever

$$q+1>\left[8W(a)\left(2+\frac{s-1}{\delta}\right)-6\right]\sqrt q.$$

The case $s=0$ means the previous bound with all prime divisors included. The derivation is identical to the prime-by-prime subtraction in [phase13_unitary_sieve.md](phase13_unitary_sieve.md): normalized mixed differences have absolute error at most $8W(a)\sqrt q$, while the normalized base count has error at most $(8W(a)-6)\sqrt q$. Here there is no subtraction of four rational boundary points, and the prime two is included in the cyclic order $N$.

## 4. Characteristic three: a rational twist

In characteristic three the curve factors into two components,

$$y=(1-x)/(x+1),\qquad y=(x+1)/(x-1).$$

Each Möbius transformation is an involution, so each component is preserved by the twisted field structure. Work with the first one. Its rational points satisfy

$$x^q=(1-x)/(x+1).$$

This is a genus-zero curve over $\mathbb F_q$ with $q+1$ rational points. For a direct count, let $\alpha,\beta\in\mathbb F_{q^2}$ be the two fixed points of the displayed involution. Its fixed-point discriminant is $-1$, a nonsquare since $q=3^e$ with $e$ odd. The cross ratio $w=(x-\alpha)/(x-\beta)$ transforms the involution into $w\mapsto-w$, and the rational-point condition becomes $w^{q+1}=-1$. That norm equation has exactly $q+1$ solutions.

The zeros and poles of $x$ and $y$ are the four distinct points $0,\infty,1,-1$, none rational in the twisted structure. The same Lang argument has four genuinely ramified simple points and genus zero, giving $\dim H_c^1=2$. Therefore every nontrivial character sum has absolute value at most $2\sqrt q$. The primitive criterion improves to

$$q+1>2(W(N)-1)\sqrt q,$$

or, with the same core-sieve notation,

$$q+1>\left[2W(a)\left(2+\frac{s-1}{\delta}\right)-2\right]\sqrt q.$$

The two intersection points of the original components are harmless: the calculation is on one smooth component, and these are ordinary rational points there. They have $x$ of order four, so never contribute primitive values for $q\ge27$.

## 5. The separate arithmetic completion

The inequalities give all sufficiently large fields by the usual elementary estimate $W(N)=O_\varepsilon(N^\varepsilon)$. The explicit cutoff, complete finite-field intake and coordinate witnesses are supplied in [phase15_unitary_sieve.md](phase15_unitary_sieve.md). This curve note does not replace those exact arithmetic certificates. No claim about current publication priority is made.

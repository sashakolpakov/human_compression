# Reducing the second unitary family to one large middle rotation

10 October 2026. Original phase-fifteen proposed conditional reduction. The uniform parameter-existence proof and its independent reviews are separate companion records.

**Reduction theorem.** Let $q=p^e\equiv3\pmod4$ and $q\ge27$. Suppose $a\in\mathbb F_{q^2}$ has $\bar a=-a$ and that

$$P_a(X)=X^4+aX^3-aX+1$$

has four distinct eigenvalues whose projective order is $m=(q^2-1)/2$ or $(q^2+1)/2$. Here projective order means the least positive exponent making all four eigenvalues equal. Then the sphere template admits a choice of $b$ satisfying both the generation criterion and the full intersection criterion, and hence gives a rank-four string C-group for $\operatorname{PSU}_4(q)$.

The argument separates the eigenvalue problem from the two-dimensional choice of $b$. It also explains why a special unsuccessful choice such as $a=b$ does not obstruct existence.

## 1. Large projective order forces the full square field

The assumed order is prime to $p$. If the polynomial did not have four distinct roots, its discriminant

$$4(a^2-8)^2(a^2+1)$$

would vanish. Distinctness is included in the hypothesis. Also $a\ne0$: when $a=0$, the polynomial is $X^4+1$, whose eigenvalues have projective order at most four, whereas $m>4$. Thus $a^2$ is a nonzero nonsquare in $\mathbb F_q$: if it were a square, $a$ would lie in $\mathbb F_q$ and trace zero would force $a=0$.

Suppose $\mathbb F_p(a^2)=\mathbb F_{q_0}$ is proper. The extension degree $[\mathbb F_q:\mathbb F_{q_0}]$ is odd and at least three, and $q_0\equiv3\pmod4$. We have $a\in\mathbb F_{q_0^2}$, with trace zero over $\mathbb F_{q_0}$. The norm map supplies $b_0\in\mathbb F_{q_0^2}^*$ with norm $1+a^2\ne0$. The same four-by-four matrix template over this smaller field has characteristic polynomial $P_a$ and belongs to $\operatorname{SU}_4(q_0)$.

A semisimple unitary element in dimension four has order at most $(q_0+1)^4$. One elementary proof groups its eigenvalues into orbits of $z\mapsto z^{-q_0}$: an orbit of length $d$ has order dividing $q_0^d-(-1)^d$, and the sum of the orbit lengths is four. The least common multiple is bounded by their product, in turn at most $(q_0+1)^4$. The matrix just constructed is semisimple because its characteristic polynomial has distinct roots. Its projective eigenvalue order is the same $m$, so

$$m\le(q_0+1)^4.$$

But

$$m\ge(q^2-1)/2\ge(q_0^6-1)/2>(q_0+1)^4\qquad(q_0\ge3),$$

a contradiction. The final inequality follows at $q_0=3$ from $364>256$, and for $q_0\ge4$ from $(q_0+1)^4\le(5q_0/4)^4<q_0^6/2-1/2$. Hence $\mathbb F_p(a^2)=\mathbb F_q$.

## 2. There are uniformly enough choices of the second block

Choose $i^2=-1$ and write $a=it$, where $t\in\mathbb F_q^*$. The nonzero norm value $1-t^2$ has exactly $q+1$ representations

$$b=x+iy,\qquad x^2+y^2=1-t^2,$$

because the norm map $\mathbb F_{q^2}^*\to\mathbb F_q^*$ has kernel of order $q+1$. The cases $x=0$ or $y=0$ remove at most four points. The extra alternating-form degeneracy

$$h=t^2+2y+2=0$$

fixes $y$ and removes at most two more points. For composite $q$, the generation theorem needs no further exclusion. Thus every such $q\ge27$ has a valid choice of $b$.

For prime $q\ge31$, require additionally that $RS$ have projective order greater than five. Its determinant is one and its trace is $-2y$. A two-by-two semisimple matrix of projective order $r$ has trace-square invariant

$$\tau=2+\zeta+\zeta^{-1},$$

where $\zeta$ is a primitive $r$th root of unity. For $r\le5$, the possible values are

$$4,\quad0,\quad1,\quad2,\quad(3+\sqrt5)/2,\quad(3-\sqrt5)/2.$$

For $q\ge31$ prime the characteristic exceeds five, so no additional unipotent order at most five occurs. The equation $4y^2=\tau$ for this list has at most eleven solutions for $y$: the value zero has one solution and each of the other five values has at most two. Every fixed $y$ has at most two possible $x$, giving at most twenty-two sphere points. This already includes $y=0$. Removing $x=0$ and $h=0$ costs at most four more. Since $q+1>26$, an admissible $b$ remains.

All prime powers $q\equiv3\pmod4$, $q\ge27$, are either composite or prime at least 31, proving the reduction. The smaller fields $7,11,19,23$ require separate finite witnesses; the frozen q=7 certificate and a fresh q=11 certificate already exist, and the remaining two have exact direct-parameter certificates in the companion finite package.

## 3. A sufficient one-variable condition

Let $\lambda\in\mathbb F_{q^2}^*$ be primitive and satisfy

$$\operatorname{Norm}_{q^2/q}(\lambda-\lambda^{-1})=-2.$$

Put $u=\lambda-\lambda^{-1}$ and $a=\bar u-u$. Since $u\bar u=-2$, one has $u-\bar u=-a$ and $u(-\bar u)=2$. Therefore

$$P_a(X)=(X^2-uX-1)(X^2+\bar uX-1),$$

whose roots are

$$\lambda,\quad-\lambda^{-1},\quad-\lambda^q,\quad\lambda^{-q}.$$

They are distinct for $q\ge7$. Any coincidence would force the primitive $\lambda$ to have order dividing one of $4$, $q+1$, or $2(q-1)$, all smaller than $q^2-1$. With $N=q^2-1$, their exponents relative to $\lambda$ are

$$1,\quad N/2-1,\quad N/2+q,\quad-q.$$

The greatest common divisor of their differences with $N$ is exactly two: all differences are even, while a common divisor divides $q+1$ and $N/2-2$, whose gcd is two. Their projective order is therefore $N/2$. Thus a primitive solution of the displayed norm equation suffices for every $q\ge27$; no second primitive condition on $b$ is needed.

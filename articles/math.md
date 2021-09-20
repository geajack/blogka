**Theorem.** The GCD of $1+a+...+a^n$ and $1+a+...+a^m$ is $1+a+...+a^s$, where $s=\gcd(n+1, m+1)-1$.

**Proof.** Let $A_k=1+a+...+a^k$. We know from the previous argument that any common divisor of $A_n$ and $A_m$ divides $A_s$. It remains to be shown that $A_s$ itself is a divisor of $A_n$ and $A_m$. But we have the identity
$$
A_s+a^{s+1}A_s+a^{2(s+1)}A_s+...+a^{k(s+1)}A_s=A_{(k+1)s+k}=A_{s+k(s+1)}
$$
Which can be seen through simple algebra. Therefore, with an appropriate choice of $s$, we can show that $A_s$ divides $A_r$, where $r$ is any number congruent to $s$ modulo $s+1$, such as $n$ and $m$. ∎

In particular, we have, in any base:
$$
\gcd(\underbrace{111...1}_n, \underbrace{111...1}_m)=\underbrace{111...1}_{\gcd(n, m)}
$$
This is very like the result for the Fibonacci numbers that says that $\gcd(F_n, F_m)=F_{\gcd(n, m)}$. A sequence satisfying this identity is called a [strong divisibility sequence](https://en.wikipedia.org/wiki/Divisibility_sequence).
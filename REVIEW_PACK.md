# Akshat Prime Cipher (APC) — Peer Review & KPA Package

Author: Akshat Dhabalia
Version: Experimental Review Build
Year: 2026

---

# 1. Purpose of This Package

This package is intended for:

* Cryptanalysis
* Peer review
* Structural evaluation
* Known Plaintext Attack (KPA) testing
* Educational cryptographic analysis

The cipher is experimental and not intended for production security.

---

# 2. Cipher Overview

The Akshat Prime Cipher (APC) is a deterministic master-key driven hybrid cipher system combining:

* Printable ASCII substitution
* Case-sensitive dual grouping
* Stateful pivot chaining
* Repeat-aware transformations
* Affine encryption
* Double Myszkowski transposition
* Double Columnar transposition
* Multi-layer padding

The system operates over the full printable ASCII range (ASCII 32–126).

---

# 3. Cipher Pipeline

Encryption order:

1. Split plaintext into words
2. Pre-padding for small words
3. Pivot transformation
4. Pivot chaining
5. Repeat transformation
6. Affine transformation
7. Double Myszkowski transposition
8. Double Columnar transposition
9. Final padding

---

# 4. Review Objectives

Reviewers are encouraged to:

* Analyze statistical leakage
* Attempt known plaintext attacks
* Attempt chosen plaintext attacks
* Analyze transposition isolation
* Recover affine structure
* Evaluate diffusion
* Evaluate avalanche effect
* Analyze deterministic behavior
* Evaluate padding predictability
* Test structural separability

---

# 5. System Inputs

The system accepts:

| Input        | Purpose                          |
| ------------ | -------------------------------- |
| MASTER_KEY   | Derives deterministic parameters |
| PRIME_NUMBER | Pivot initialization/chaining    |
| THRESHOLD    | Small-word pre-padding rule      |

---

# 6. Parameters NOT Provided to Reviewers

The following are intentionally hidden:

* Derived affine parameters
* Derived grouping values
* Derived transposition keys
* Internal deterministic seed
* Expanded key schedule

---

# 7. Publicly Known Rules

The following are public:

* Padding position logic
* Pivot chaining formula
* ASCII domain
* Transformation order
* Case-sensitive indexing
* Prime-based transformations

---

# 8. Padding Rules

Padding uses pair-of-pairs insertion.

Positions are deterministic.

Padding values themselves are random.

Padding characters use the printable ASCII range.

---

# 9. Pivot Chaining Formula

For word n:

X = i(n-1) × L(n)

p = next_prime(X)

Y = X + p + i(n-1)

i(n) = Y mod L(n)

---

# 10. Known Plaintext Dataset

## Dataset A — Basic Words

| Plaintext | Ciphertext      |
| --------- | --------------- |
| Hello     | VFV&FpQh$ |
| WORLD     | %*CBiSnC |
| Cipher    | Ia6TEy=2<E |
| Security  | <-x9,Y=?{O6q |
| Akshat    | IjH1,%O'#X |

---

## Dataset B — Repetition Heavy

| Plaintext             | Ciphertext      |
| --------------------- | --------------- |
| HELLO HELLO HELLO     | Gs#GcQAPi >2:2Q,W{w 7,3zM7(R! |
| AAAA BBBB CCCC        | HZ0IW3+>&G6@ hKUvr5+qmd#j q[Gz1;EzwR@k |
| TESTTESTTEST          | $iu$i@t=BC;[![uM |
| repetition repetition | O.y<HS,<U:%Mp3 Fqh_NEWybK6qI? |

---

## Dataset C — Case Sensitivity

| Plaintext | Ciphertext      |
| --------- | --------------- |
| HelLo     | P7U0FhJ%$ |
| HeLLo     | P7adF7G`$ |
| hELlo     | Vh#,F7'y$ |
| AAAaaaAAA | Lq<7#o7<'oLIL |
| Gemini   | bp-|&yJ/Op |

---

## Dataset D — Mixed ASCII

| Plaintext         | Ciphertext      |
| ----------------- | --------------- |
| Hello@2026#World! | k|KyobE>J7U>xLkz%wvCT |
| $ecure_Cipher^    | ?aF,aqXl'5a[pzap@+ |
| 123ABCabc!?       | @pc]F'O.2[V%Z,h |
| <>{}[]+=-         | @X7y>[/T+O )feRVX |
| ASCII_TEST_95     | B)@@kk-\LZ)G^lB:^ |

---

## Dataset E — Small Words

| Plaintext    | Ciphertext      |
| ------------ | --------------- |
| I am at HQ   | N;EcuC) mPiXO qDIZ^+usGC "!@y}%<U-Q tC2|~ @X)}%dnX |
| to be or not | U>htychA#0 ].^pqW?# Iz^gU $6+2a_?b%D 6Iba]?}DftP |
| an ox up     | h|%\VV8^q# qdXNuzNi5< lqjH7+O,:X |
| AI is dun    | F@VQ5,{ztj g7#L>%^`+G Zf[j[Bz=#q+ |
| go do it     | <F.g.GF_jp l.E/$R{4xh wotdyq8n?3 |

---

## Dataset F — Long Sentences

| Plaintext                                                  | Ciphertext      |
| ---------------------------------------------------------- | --------------- |
| The quick brown fox jumps over the lazy dog                | xkjRa93DZ)q o;#pa:Y;? }aoG?LwsV gR3I}fvf Z/o|.^ @),;owr!M hv04%}~v:7)Y 6$77QBp|3Bz XPB7BR<5kB[q FBq3H9>h#o. |
| Cryptography is the practice of secure communication       | pEk56k[Mj^f+aP%9 l,HZ?%^r6X O?"Am*X6!T_ aa.Nc#[qgS.j o6;zUHv9=< RpV;J<K-~p ?Zp]9?U)jI#oWhaxy |
| Stateful chained pivots improve diffusion across words     | N[aVz%aXlY9X hhMYu#Hvy%j ,.pyN4J4O6 yqM1h.6FiPO =?HfOr.#7qT#6 XyDB!]-_q< aN 3HV@iN |
| This cipher combines substitution and transposition layers | aaCF0R%vcR[z _[zS$pl(p# Kx2z sHOEaaV EjYy%qQu<T|j0Z5y VqaF@RIq[Nq Xq4k6qn aMFg8Hfv< qaK;`pNKHh |
| Experimental ciphers require extensive peer review         | hfjhzpuKEH#Yx._E a6h8.a?%c]q H.vBI?<H@.X yV?h$3_O(|M6c yC1_(^ H%jGVboC6 @[h,(y4LoX |

---

# 11. Deterministic Repeatability Tests

Encrypt the SAME plaintext multiple times with the SAME MASTER_KEY.

Example plaintext:

```text
Hello WORLD I am ChatGPT
```

Expected observation:

* Structural layers remain deterministic
* Padding characters vary
* Padding positions remain deterministic

---

## Repeatability Run 1

Ciphertext:

```text
G,4-I%03: _^56i$@M+ p=31F7~U% lup!(Pl 7* Qb@mhI]Uhgg
```

---

## Repeatability Run 2

Ciphertext:

```text
G-})D%Ct: o^oqi$7u+ 6=|jF7?.| lfpp3P.<7* =Nx&Qb]U|g%
```

---

## Repeatability Run 3

Ciphertext:

```text
GoJ)K%,m: 3^^Bi$Bp+ }=^\F7sUs l|pG\P{@7* 9kpH E]U&N?
```

---

# 12. Suggested Cryptanalysis Directions

Reviewers may attempt:

* Affine reduction attacks
* Frequency analysis
* Padding stripping
* Pivot prediction
* Known plaintext reconstruction
* Transposition reversal
* Structural decomposition
* Differential analysis
* Statistical analysis
* Entropy estimation

---

# 13. Questions for Reviewers

1. Are the layers cryptographically entangled or separable?
2. Can affine parameters be isolated?
3. Does pivot chaining significantly improve diffusion?
4. Can padding be reliably removed?
5. Does the system leak structural information?
6. How resistant is the system to known plaintext attacks?
7. Does the system exhibit meaningful avalanche effect?
8. Are there exploitable deterministic patterns?
9. Can transposition layers be independently reversed?
10. Does the system preserve frequency characteristics?

---

# 14. Intended Use Cases

Suitable for:

* CTF systems
* Educational cryptography
* Experimental cryptographic design
* Puzzle systems
* Adversarial testing

Not suitable for:

* Banking
* Password protection
* Production encryption
* Military/security communications
* High-value confidential data

---

# 15. GitHub Release Checklist

Before release:

* Include full source code
* Include algorithm specification
* Include this review package
* Include license
* Include disclaimer
* Include reproducible examples

---

# 16. Suggested License

MIT License with attribution requirement.

---

# 17. Suggested Disclaimer

This cipher is experimental.

It has not been formally peer-reviewed or proven secure.

Use only for:

* educational purposes
* experimentation
* cryptographic learning
* CTFs and puzzle systems

---

# 18. Final Notes

This package is intended to encourage:

* constructive criticism
* cryptanalysis
* discussion
* experimentation
* iterative improvement

Reviewers are encouraged to:

* publish findings
* propose attacks
* identify weaknesses
* suggest improvements

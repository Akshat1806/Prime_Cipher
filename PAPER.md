# PAPER.md

# Prime Cipher (PC)

## Experimental Hybrid Cryptographic Architecture

Author: Akshat Dhabalia
Year: 2026

---

# Abstract

The Prime Cipher (PC) is an experimental deterministic hybrid cipher architecture combining substitution, affine transformation, stateful pivot chaining, transposition systems, and adaptive padding mechanisms over the printable ASCII domain.

The system explores the interaction between:

* deterministic master-key generation
* chained pivot evolution
* case-sensitive indexing
* global and local transposition layers
* structured randomized padding

This cipher is intended for:

* educational cryptography
* adversarial experimentation
* cryptanalysis research
* CTF systems

It is NOT intended for production security use.

---

# 1. Character Domain

The system operates on printable ASCII:

ASCII range:
32–126

Total domain:
95 characters

---

# 2. Master Key System

The system accepts:

* MASTER_KEY
* PRIME_NUMBER
* THRESHOLD

The MASTER_KEY is hashed using SHA-256.

The resulting digest is converted into a deterministic integer seed.

Using:

```python
rng = random.Random(seed)
```

the system deterministically derives:

* grouping values
* affine parameters
* transposition key lengths
* transposition keys

---

# 3. Dual Grouping System

Two independent grouping values are generated:

* upper_grp
* lower_grp

Range:
2–94

These grouping values create transposed ASCII mappings.

---

# 4. Transposed ASCII Mapping

Printable ASCII is arranged into rows of length grp and read column-wise.

This produces:

* value_map
* reverse_map

Used for:

* substitution
* affine transformation

---

# 5. Case-Sensitive Indexing

Uppercase and lowercase indices are tracked independently.

Example:

```text
HelLo
```

Uppercase:
H(1), L(2)

Lowercase:
e(1), l(2), o(3)

---

# 6. Pre-padding System

For words where:

L < THRESHOLD

one deterministic padding layer is applied before encryption.

Purpose:

* avoid small-word weakness
* improve pivot diffusion

---

# 7. Pivot Transformation

Applied before all other ciphering.

---

## First Word

For first word:

i₁ = (P − L₁) mod L₁

Where:

* P = PRIME_NUMBER
* L₁ = length of first word

---

## Pivot Value

Pivot character:

word[iₙ]

Pivot value:

pivot = ASCII(word[iₙ]) − 32

---

## Transformation

For every character:

new = (value + pivot) mod 95

---

# 8. Pivot Chaining

For word n > 1:

X = i(n−1) × L(n)

p = next_prime(X)

Y = X + p + i(n−1)

i(n) = Y mod L(n)

This creates stateful dependency between words.

---

# 9. Repeat Transformation

Repeated letters are processed using:

product = index × value

prime = next_prime(product)

difference = prime − product

value = (value + difference) mod 95

The process is case-sensitive.

---

# 10. Affine Transformation

Formula:

E(x) = (ax + b) mod 95

Where:

* gcd(a,95)=1

Affine parameters are derived from MASTER_KEY.

---

# 11. Double Myszkowski Transposition

Applied globally across the full message.

Features:

* two keys
* variable key lengths (3–16)
* deterministic generation

Spaces are preserved.

---

# 12. Double Columnar Transposition

Applied per word.

Features:

* two keys
* variable key lengths (3–16)
* deterministic generation

---

# 13. Final Padding

After encryption, pair-of-pairs padding is applied.

Padding characters:

* full printable ASCII

Padding positions:

* deterministic

Padding values:

* random each run

---

# 14. Randomness Model

Deterministic:

* grouping
* affine parameters
* transposition keys
* key lengths

Random:

* padding values only

---

# 15. Security Goals

The system attempts to provide:

* layered obfuscation
* stateful transformations
* partial diffusion
* structural complexity

---

# 16. Known Weaknesses

* no formal proof of security
* affine layer remains linear
* transposition layers are classical
* no authentication mechanism
* limited avalanche effect
* partially separable layers

---

# 17. Intended Applications

Suitable for:

* CTF systems
* educational cryptography
* adversarial analysis
* experimental research

Not suitable for:

* financial systems
* military/security communication
* password protection
* production encryption

---

# 18. Conclusion

The Prime Cipher represents an experimental exploration into deterministic hybrid cipher architecture combining:

* substitution
* chained state evolution
* transposition
* adaptive padding

Its primary value lies in:

* educational experimentation
* cryptanalysis practice
* adversarial research
* custom cipher architecture exploration

# README.md

# Prime Cipher (PC)

Experimental deterministic hybrid cryptographic system designed by Akshat Dhabalia.

---

## ⚠️ Disclaimer

This cipher is experimental.

It has:

* NOT been formally peer-reviewed
* NOT been mathematically proven secure
* NOT been tested against advanced modern cryptanalysis

DO NOT use this system for:

* banking
* passwords
* confidential communications
* production encryption

Intended only for:

* cryptography learning
* experimentation
* CTF challenges
* adversarial testing
* educational research

---

# Overview

The Prime Cipher (PC) is a deterministic master-key driven hybrid encryption architecture combining:

* Printable ASCII substitution
* Case-sensitive dual grouping
* Stateful pivot chaining
* Prime-based transformations
* Affine encryption
* Double Myszkowski transposition
* Double Columnar transposition
* Adaptive multi-layer padding

The system operates over the full printable ASCII range (ASCII 32–126).

---

# Features

* Full printable ASCII support
* Deterministic master-key architecture
* Cross-word pivot chaining
* Case-sensitive indexing
* Variable-length transposition keys
* Global and local scrambling
* Multi-stage padding system
* Stateful encryption flow

---

# Encryption Pipeline

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

# Inputs

The system requires:

* Plaintext
* MASTER_KEY
* PRIME_NUMBER
* THRESHOLD

---

# Example Usage

```bash
python cipher.py
```

Example:

```text
Enter MASTER plaintext: Hello WORLD I am ChatGPT
Enter MASTER_KEY: AKSHAT2026
Enter PRIME_NUMBER: 101
Enter THRESHOLD: 5
```

---

# Repository Structure

```text
Prime-Cipher/
│
├── README.md
├── PAPER.md
├── LICENSE
├── SECURITY.md
├── REVIEW_PACK.md
│
├── implementation/
│   └── cipher.py
│
└── examples/
```

---

# Intended Use Cases

Suitable for:

* cryptography learning
* experimental cipher design
* CTF systems
* adversarial analysis
* educational demonstrations

Not suitable for:

* production encryption
* financial systems
* military/security communications

---

# Peer Review

This repository is open for:

* cryptanalysis
* known plaintext attacks
* structural analysis
* entropy analysis
* differential analysis

Constructive criticism and attack attempts are encouraged.

---

# Known Limitations

* No formal security proof
* Limited avalanche effect
* Classical transposition layers
* No integrity/authentication mechanism
* Not resistant to modern nation-state cryptanalysis

---

# License

MIT License with attribution requirement.

---

# Author

Akshat Dhabalia
2026

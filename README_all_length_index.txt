All-length/index-spectrum research note

Files:
- all-length-index-spectrum.md: theorem, proof, examples, limitations
- verify_all_length_index_pairs.py: exact verifier for five explicit cases

Run:
  python verify_all_length_index_pairs.py

The script checks exact arithmetic, primality, primitive roots, all signed
vectors, all proper projected subsequences, all generators of C_m, and the
Egyptian-fraction identity. It does not implement the Dirichlet prime search
used in the general existence proof.

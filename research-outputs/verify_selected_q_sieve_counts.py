#!/usr/bin/env python3
"""Exact q-divisor Jacobi-filter counts for selected t values; requires SymPy."""
from sympy import divisors,legendre_symbol
from survey_jacobi_rank import analyze

def check(t):
    row=analyze(t);D=row["D"];ps=row["h_prime_factors"]
    target=tuple(0 if legendre_symbol(-D,p)==1 else 1 for p in ps)
    count=sum(1 for q in divisors(D)
              if tuple(0 if legendre_symbol(q,p)==1 else 1 for p in ps)==target)
    tau=row["tau_D"];rank=row["rank"]
    bound=(tau+(1<<rank)-1)//(1<<rank)
    assert count<=bound
    if rank==len(ps):assert count==tau//(1<<rank)
    return row,count,bound
def main():
    for t in (3,7,17,69,137,185,609,1105,1285,1457,5957,6215,6657):
        row,count,bound=check(t)
        print(f"t={t}: omega(h)={row['omega_h']} rank={row['rank']} tau(D)={row['tau_D']} passing={count} bound={bound}")
    print("SELECTED_EXACT_JACOBI_COUNTS: PASS")
if __name__=="__main__":main()

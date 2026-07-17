# mech_verify.py -- grade MECH_PREDECL M1-M4 against banked fold data (pin c413c3f8)
import mpmath as mp, re, hashlib
mp.mp.dps=50
L=open('runF_a.log').read()
us={}; th={}
for m in re.finditer(r"k=(\d) th\*=([-\d.]+) u\*=([\d.]+)",L):
    k=int(m.group(1)); th[k]=mp.mpf(m.group(2)); us[k]=mp.mpf(m.group(3))*4000
OUT=[]
def emit(s): print(s,flush=True); OUT.append(s)
def fit_even(vals,ks):
    # a + b k^2 + c k^4 least squares (exact normal equations at dps 50)
    import itertools
    A=[[mp.mpf(1),mp.mpf(k)**2,mp.mpf(k)**4] for k in ks]
    y=[vals[k] for k in ks]
    AT=[[A[r][c] for r in range(len(ks))] for c in range(3)]
    M=[[sum(AT[i][r]*A[r][j] for r in range(len(ks))) for j in range(3)] for i in range(3)]
    b=[sum(AT[i][r]*y[r] for r in range(len(ks))) for i in range(3)]
    # solve 3x3
    for i in range(3):
        p=max(range(i,3),key=lambda r:abs(M[r][i])); M[i],M[p]=M[p],M[i]; b[i],b[p]=b[p],b[i]
        for r in range(i+1,3):
            f=M[r][i]/M[i][i]; b[r]-=f*b[i]
            for c in range(i,3): M[r][c]-=f*M[i][c]
    x=[mp.mpf(0)]*3
    for i in (2,1,0): x[i]=(b[i]-sum(M[i][j]*x[j] for j in range(i+1,3)))/M[i][i]
    return x
ks=[1,2,3,4,5]
a,b,c=fit_even({k:us[k]/k**2 for k in ks},ks)
T1=mp.mpf(6.25)/mp.sqrt(2)
emit(f"M1: a={mp.nstr(a,12)} target={mp.nstr(T1,12)} |diff|={mp.nstr(abs(a-T1),4)} band=3e-3 -> {'PASS' if abs(a-T1)<=mp.mpf('3e-3') else 'FAIL'}")
at,bt,ct=fit_even({k:th[k] for k in ks},ks)
T2=-mp.acos(mp.mpf(1)/3)/2
emit(f"M2: a_theta={mp.nstr(at,10)} target={mp.nstr(T2,10)} |diff|={mp.nstr(abs(at-T2),4)} band=1e-3 -> {'PASS' if abs(at-T2)<=mp.mpf('1e-3') else 'FAIL'}")
emit(f"M3: b={mp.nstr(b,8)} negative -> {'PASS' if b<0 else 'FAIL'}")
for k in (6,7):
    pred=(a+b*k**2+c*k**4)*k**2
    emit(f"M4: k={k} fit-extrapolated 4000u*={mp.nstr(pred,10)} banked={mp.nstr(us[k],10)} resid={mp.nstr(us[k]-pred,4)}")
blob="\n".join(OUT).encode()
print("RESULTS-SHA256:",hashlib.sha256(blob).hexdigest())

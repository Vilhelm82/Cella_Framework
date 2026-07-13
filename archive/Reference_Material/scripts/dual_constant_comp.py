import sys

try:
    import mpmath
except ImportError:
    print("Error: The 'mpmath' library is not installed.")
    print("On Fedora, you can install it via your terminal:")
    print("sudo dnf install python3-mpmath")
    sys.exit(1)


# Set arbitrary precision to 65 decimal places
mpmath.mp.dps = 65

# 1. Define the algebraic components
sqrt2 = mpmath.sqrt(2)

# Conjugate Parameters
k_sq = (2 + sqrt2) / 4
n = (4 + 3*sqrt2) / 8

# Conjugate Weights
w_Pi = 3 - 2*sqrt2
w_K = 2 - 2*sqrt2

# Global scale factor
scale = -(2**(mpmath.mpf(7)/4))

# 2. Evaluate the Elliptic Integrals
# mpmath.ellipk(m) computes the 1st kind with parameter m = k^2
K_val = mpmath.ellipk(k_sq)

# mpmath.ellippi(n, m) computes the 3rd kind
# Note: Because n > 1, this evaluates the complex/Cauchy principal value
Pi_val = mpmath.ellippi(n, k_sq)
Pi_val_real = Pi_val.real

# 3. Calculate the Dual Constant
dual_constant = scale * (w_Pi * Pi_val_real - w_K * K_val)

print("Target 1 (Dual Constant) Cauchy Principal Value computed to 65 digits:")
print(dual_constant)

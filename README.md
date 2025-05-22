Solves linear program using the dual simplex method with fractional arithmetic. Tableau updated by row operations and all numbers are printed as fractions
Inputs: A: 2D list (m x n) of coefficients (constraints in equality form), b: 1D list (length m) of right-hand side values, c: 1D list (length n) of objective function coefficients
basic_vars: list of indices (length m) indicating which variables are currently basic.
basic_vars[0] = 0 so  first row corresponds to x1)

import numpy as np
from fractions import Fraction

def print_tableau(tableau, basic_vars, c, m, n):
    """
    Prints the current tableau 
    teableau rows 0..m-1 correspond to constraint rows.
    row m is  z_j row and row m+1 is the (z_j - c_j) row
    all numbers printed as fractions
    """
    col_width = 12
    header = ["C_B", "Basis"] + [f"x{j+1}" for j in range(n)] + ["x_B"]
    header_line = "".join(word.ljust(col_width) for word in header)
    print(header_line)
    print("-" * len(header_line))
    
    for i in range(m):
        cb = c[basic_vars[i]]
        basis = f"x{basic_vars[i]+1}"
        row_entries = [str(cb), basis] + [str(tableau[i][j]) for j in range(n)] + [str(tableau[i][n])]
        print("".join(entry.ljust(col_width) for entry in row_entries))
    
    # z_j 
    zj_row = ["", "z_j"] + [str(tableau[m][j]) for j in range(n)] + [str(tableau[m][n])]
    # (z_j - c_j)
    zj_cj_row = ["", "z_j-c_j"] + [str(tableau[m+1][j]) for j in range(n)] + [str(tableau[m+1][n])]
    print("".join(entry.ljust(col_width) for entry in zj_cj_row))
    print()  

def dual_simplex(A, b, c, basic_vars):
    """
    solves linear program using the dual simplex method with fractional arithmetic
    Tableau  updated by row operations and all numbers are printed as fractions
    Inputs:
      A: 2D list (m x n) of coefficients (constraints in equality form)
      b: 1D list (length m) of right-hand side values
      c: 1D list (length n) of objective function coefficients
      basic_vars: list of indices (length m) indicating which variables are currently basic.
                 basic_vars[0] = 0 so  first row corresponds to x1)
    """
    m = len(A)
    n = len(A[0])
    A = [[Fraction(x) for x in row] for row in A]
    b = [Fraction(x) for x in b]
    c = [Fraction(x) for x in c]
    
    
    tableau = [[Fraction(0) for _ in range(n+1)] for _ in range(m+2)]
    for i in range(m):
        for j in range(n):
            tableau[i][j] = A[i][j]
        tableau[i][n] = b[i]
    
    c_B = [c[i] for i in basic_vars]
    
    # Compute the z_j row.
    for j in range(n):
        tableau[m][j] = sum(c_B[i] * A[i][j] for i in range(m))
    tableau[m][n] = sum(c_B[i] * b[i] for i in range(m))
    
    # z_j - c_j) row.
    for j in range(n):
        tableau[m+1][j] = tableau[m][j] - c[j]
    tableau[m+1][n] = tableau[m][n]
    
    print("Initial Tableau:")
    print_tableau(tableau, basic_vars, c, m, n)
    
    iteration = 0
    while True:
        if all(tableau[i][n] >= 0 for i in range(m)):
            print("Final Tableau (Feasible solution reached):")
            print_tableau(tableau, basic_vars, c, m, n)
            print("Basic solution:")
            for i in range(m):
                print(f"  x{basic_vars[i]+1} = {tableau[i][n]}")
            print(f"Final objective value: {tableau[m][n]}")
            return
        
        pivot_row_index = min(range(m), key=lambda i: tableau[i][n])
        print(f"Iteration {iteration+1}:")
        print(f"Pivot row selected: R{pivot_row_index+1} (RHS = {tableau[pivot_row_index][n]})")
        
        if all(tableau[pivot_row_index][j] >= 0 for j in range(n)):
            print("No feasible solution exists: all entries in the pivot row are non-negative.")
            return
        
        candidate_columns = []
        ratios = []
        for j in range(n):
            if tableau[pivot_row_index][j] < 0:
                ratio = tableau[m+1][j] / tableau[pivot_row_index][j]
                candidate_columns.append(j)
                ratios.append(ratio)
        
        if len(ratios) == 0:
            print("No feasible solution exists: No pivot column found (all entries are non-negative in the pivot row).")
            return
        
        max_ratio_index = max(range(len(ratios)), key=lambda i: ratios[i])
        pivot_col_index = candidate_columns[max_ratio_index]
        print(f"Pivot column selected: x{pivot_col_index+1}")
        
        operations_log = []
        pivot_element = tableau[pivot_row_index][pivot_col_index]
        op_str = f"R{pivot_row_index+1} / ({pivot_element}) -> R{pivot_row_index+1}"
        operations_log.append(op_str)
        
        tableau[pivot_row_index] = [elem / pivot_element for elem in tableau[pivot_row_index]]
        
        # for every other row, remove pivot col entry 
        for i in range(m+2):
            if i != pivot_row_index:
                factor = tableau[i][pivot_col_index]
                op_str = f"R{i+1} - ({factor})*R{pivot_row_index+1} -> R{i+1}"
                operations_log.append(op_str)
                tableau[i] = [ tableau[i][j] - factor * tableau[pivot_row_index][j] for j in range(n+1) ]
        
        old_var = basic_vars[pivot_row_index]
        basic_vars[pivot_row_index] = pivot_col_index
        print(f"Leaving variable: x{old_var+1} replaced by entering variable: x{pivot_col_index+1}")
        
        c_B = [c[i] for i in basic_vars]
        for j in range(n):
            tableau[m][j] = sum(c_B[i] * tableau[i][j] for i in range(m))
        tableau[m][n] = sum(c_B[i] * tableau[i][n] for i in range(m))
        for j in range(n):
            tableau[m+1][j] = tableau[m][j] - c[j]
        tableau[m+1][n] = tableau[m][n]
        
        print("Row operations performed:")
        for op in operations_log:
            print(" ", op)
        print("\nUpdated Tableau:")
        print_tableau(tableau, basic_vars, c, m, n)
        
        iteration += 1

#sample input
if __name__ == '__main__':
    A = [
        [1, 0, 3, -1, 0],
        [0, 1, -5, 2, 0],
        [0, 0, 18, -7, 1],
    ]
    b = [1, 2, -3]
    c = [7, 4, 0, 0, 0]
    basic_vars = [0, 1, 4]



dual_simplex(A, b, c, basic_vars)

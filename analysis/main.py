import calculations as calc
from data_loader import load_data
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from visualize import scatter_plot_3, fitted_plot

path_in1 = 'data/clean_diod_k_1.csv'
path_in2 = 'data/clean_diod_k_2.csv'
path_in3 = 'data/clean_diod_k_3.csv'
path_figures = 'raport/figures'
path_results = 'analysis/results.txt'

R = 1000  #Ohms
T = 300 #K
k = 1.38e-23  #J/K
e = 1.6e-19  #C
I_P = 1e-4  #A


if __name__ == "__main__":
    with open(path_results, 'w') as f:
        f.write("")

    df1 = load_data(path_in1, decimal=',')
    df2 = load_data(path_in2, decimal=',')
    df3 = load_data(path_in3, decimal=',')

    df1 = calc.add_column_I_D(df1, R)
    df1 = calc.add_column_U_D(df1) 

    df2 = calc.add_column_I_D(df2, R)
    df2 = calc.add_column_U_D(df2) 

    df3 = calc.add_column_I_D(df3, R)
    df3 = calc.add_column_U_D(df3) 

    scatter_plot_3(df1, df2, df3, path_figures)

    df2["u_I_D"] = abs(df2['I_D'])*0.03/np.sqrt(3)/50
    df2["u_U_D"] = abs(df2['U_D'])*0.03/np.sqrt(3)

    results2 = calc.calc_parameters(df2, T=T)

    exp_U_p = results2["M"]*k*T/e * np.log(I_P/results2["I_g"]+1)

    with open(path_results, 'a') as f:
        f.write("Results for diod k 1:\n")
        f.write(f"I_g = {results2['I_g']:.1E} +- {results2['u_I_g']:.1E}\n")
        f.write(f"M = {results2['M']:.4f} +- {results2['u_M']:.4f}\n")
        f.write(f"chi2_red = {results2['chi2_red']:.8f}\n\n")
        f.write("Mulitimeter U_p = 0.53 V\n")
        f.write(f"experimental U_p = {exp_U_p:.4f} +- {results2['u_M']:.4f}\n")

    fitted_plot(df2, path_figures, T, results2["I_g"], results2["M"])




    












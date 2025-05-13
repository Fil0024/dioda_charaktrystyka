import seaborn as sns
import matplotlib.pyplot as plt
import calculations as calc

def scatter_plot_3(df1, df2, df3, path_figures):
    x_col = 'U_D'
    y_col = 'I_D'

    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df1, x=x_col, y=y_col, label='Pomiary 1', color='blue')
    sns.scatterplot(data=df2, x=x_col, y=y_col, label='Pomiary 2', color='orange')
    sns.scatterplot(data=df3, x=x_col, y=y_col, label='Pomiary 3', color='green')
    plt.xlabel('$U_D$ (V)', fontsize=12)
    plt.ylabel('$I_D$ (A)', fontsize=12)
    plt.legend()
    
    plt.savefig(f"{path_figures}/comparison.pdf", dpi=300)

def fitted_plot(df, path_figures, T, I_g, M):
    x_col = 'U_D'
    y_col = 'I_D'
    u_x_col = 'u_U_D'
    u_y_col = 'u_I_D'

    x = df[x_col].to_numpy()
    y = df[y_col].to_numpy()
    u_x = df[u_x_col].to_numpy()
    u_y = df[u_y_col].to_numpy()

    def model(U_D, I_g, M):
        return calc.function_I_D(U_D, I_g, M, T)

    plt.figure(figsize=(8, 6))

    plt.errorbar(x, y, xerr=u_x, yerr=u_y, fmt=' ', color='black', label='Błąd pomiaru', elinewidth=0.8)
    sns.scatterplot(data=df, x=x_col, y=y_col, label='Dane', color='black')

    plt.plot(x, model(x, I_g, M), label='Dopasowanie', color='red')
    
    plt.xlabel(r'$U_D$ (V)', fontsize=12)
    plt.ylabel(r'$I_D$ (A)', fontsize=12)
    plt.legend()
    
    plt.savefig(f"{path_figures}/fitted.pdf", dpi=300)
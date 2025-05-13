import numpy as np
from scipy.optimize import curve_fit
from scipy.odr import ODR, Model, RealData

def add_column_I_D(df, R=1000):
    df['I_D'] = df['U_R'] / R
    return df

def add_column_U_D(df):
    df['U_GEN'] = df['U_D'] + df['U_R']
    return df

def function_I_D(U_D, I_g, M, T, k=1.38e-23, e=1.6e-19):
    return I_g * (np.exp(e * U_D / (M * k * T)) - 1)

def fit_I_D(U_D, I_D, u_I_D, u_U_D, T,
                p0=(1e-12, 1.2),
                k=1.38e-23, e=1.6e-19):
    data = RealData(
        x=U_D,
        y=I_D,
        sx=u_U_D,
        sy=u_I_D
    )

    # 2) Definicja funkcji modelu dla ODR: B = [I_g, M]
    def odr_model(B, x):
        I_g, M = B
        # zakładamy calc.function_I_D(U_D, I_g, M, T) → I_D
        return function_I_D(x, I_g, M, T)

    model = Model(odr_model)

    # 3) Ustawienie ODR
    odr = ODR(data, model, beta0=p0)

    # 4) Uruchomienie fitu
    out = odr.run()

    # 5) Pobranie wyników
    popt = out.beta          # optymalne [I_g, M]
    perr = out.sd_beta       # sigma I_g, sigma M
    chi2_red = out.res_var   # reduced variance ≈ χ²_red

    return popt, perr, chi2_red

def calc_parameters(df, T = 300, x_axis='U_D', y_axis='I_D', u_x_axis='u_U_D', u_y_axis = 'u_I_D'):
    x, u_x = df[x_axis].to_numpy(), df[u_x_axis].to_numpy()

    y, u_y = df[y_axis].to_numpy(), df[u_y_axis].to_numpy()

    (I_g, M),  (u_I_g, u_M), chi2_red  = fit_I_D(x, y, u_x, u_y, T)

    return {
        "I_g": I_g,
        "M": M,
        "u_I_g": u_I_g,
        "u_M": u_M,
        "chi2_red": chi2_red,
    }
    
    
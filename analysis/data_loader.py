import pandas as pd

def load_data(path, sep=',', decimal=','):
    df = pd.read_csv(path, sep=sep, decimal=decimal, skiprows=[1, 2])
    df = df.drop(columns=['Komentarze'], errors='ignore')
    return df

if __name__ == "__main__":
    path = 'data/diod_k_1.csv'
    df = load_data(path)
    print(f"{path}: {df.shape} wczytane.")
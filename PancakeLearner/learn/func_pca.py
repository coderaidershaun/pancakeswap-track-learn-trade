import pandas as pd
import numpy as np
from sklearn.decomposition import PCA


def provide_pca(df):

  # Initialize PCA with 5 components
  pca = PCA(n_components=3)

  # Fit PCA on the dataframe
  pca.fit(df)

  # transform the dataframe using PCA
  df_pca = pd.DataFrame(pca.transform(df), columns=['PCA1', 'PCA2', 'PCA3'], index=df.index)

  # print the transformed dataframe
  print("Explained PCA: ", round(sum(pca.explained_variance_ratio_), 2))
  return df_pca

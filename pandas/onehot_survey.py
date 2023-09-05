import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import hstack

def onehot_multichoices(
    data: pd.DataFrame, multichoice_cols: list[str], pattern: str
) -> pd.DataFrame:
    sparse_matrix_list = []
    feature_name_list = []

    # Convert only necessary columns to Pandas Series
    pd_df = data.loc[:, multichoice_cols]

    for col in multichoice_cols:
        vectorizer = CountVectorizer(token_pattern=pattern)
        X = vectorizer.fit_transform(pd_df[col])
        feature_names = vectorizer.get_feature_names_out()

        # Keep track of sparse matrices and feature names
        sparse_matrix_list.append(X)
        feature_name_list.extend([f"{col}__{i}" for i in feature_names])

    # Concatenate sparse matrices horizontally
    combined_sparse_matrix = hstack(sparse_matrix_list)

    # Convert the combined sparse matrix to a dense Pandas DataFrame
    combined_df = pd.DataFrame(
        combined_sparse_matrix.toarray(), columns=feature_name_list, index=pd_df.index
    ).astype("int8")

    return data.drop(columns=multichoice_cols).join(combined_df)

# import polars as pl

# df = pl.from_repr("""shape: (20, 5)
# ┌────────────────┬──────────────────────┬────────────┬──────────────────┬────────────┐
# │ 選擇本院的原因 ┆ 請注意               ┆ A.口腔檢查 ┆ B.治療疼痛       ┆ C.醫療諮詢 │
# │ ---            ┆ ---                  ┆ ---        ┆ ---              ┆ ---        │
# │ str            ┆ str                  ┆ str        ┆ str              ┆ str        │
# ╞════════════════╪══════════════════════╪════════════╪══════════════════╪════════════╡
# │ 未填           ┆ 未填                 ┆ 洗牙       ┆ 未填             ┆ 未填       │
# │ 親友           ┆ 未填                 ┆ 未填       ┆ 未填             ┆ 未填       │
# │ 其他           ┆ 未填                 ┆ 蛀牙       ┆ 牙齒痛, 根管治療 ┆ 未填       │
# │ 親友           ┆ 本人非常怕痛         ┆ 蛀牙       ┆ 牙齒痛           ┆ 牙周病     │
# │ …              ┆ …                    ┆ …          ┆ …                ┆ …          │
# │ 親友           ┆ 未填                 ┆ 未填       ┆ 牙肉腫           ┆ 未填       │
# │ 親友           ┆ 未填                 ┆ 洗牙       ┆ 未填             ┆ 未填       │
# │ 住家           ┆ 本人非常怕痛, 很緊張 ┆ 未填       ┆ 牙齒痛           ┆ 未填       │
# │ 未填           ┆ 未填                 ┆ 未填       ┆ 未填             ┆ 未填       │
# └────────────────┴──────────────────────┴────────────┴──────────────────┴────────────┘
# """).to_pandas()

# df.pipe(onehot_multichoices, df.columns, r"[^, ]+")

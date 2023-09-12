import polars as pl


def onehot_multichoices(
    data: pl.DataFrame, multichoice_pat: str
) -> pl.DataFrame:
    multichoice_cols = data.select(
        col
        for col in data.select(pl.col(pl.Utf8)).columns
        if data[col].str.contains(multichoice_pat).any()
    ).columns
    multichoice_dfs = []
    for col in multichoice_cols:
        col_df = data.select(pl.col(col).str.split(multichoice_pat))
        multichoice_dfs.append(
            col_df.select(
                pl.col(col).list.contains(val).cast(pl.Int8).suffix(f"__{val}")
                for val in col_df.explode(col)[col].unique().to_list()
            )
        )
    return pl.concat(
        [data.select(pl.all().exclude(multichoice_cols))] + multichoice_dfs,
        how="horizontal",
    )


# (
#     df
#     .pipe(onehot_multichoices, "id", ["multichoice_col1", "multichoice_col2"], "\n")
# )

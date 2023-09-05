import polars as pl

def onehot_multichoices(
    data: pl.DataFrame, index_col: str, multichoice_cols: list[str], pattern: str
) -> pl.DataFrame:
    multichoice_dfs = []
    for col in multichoice_cols:
        exploded_df = data.select(
            index_col,
            pl.col(col).str.split(pattern)
        )
        multichoice_dfs.append(
            exploded_df
            .group_by(index_col)
            .agg(
                pl.col(col).list.contains(val).first().cast(pl.Int8).suffix(f"__{val}")
                for val in exploded_df.explode(col)[col].unique().to_list()
            )
            .select(pl.all().exclude(index_col))
        )
    return pl.concat([data] + multichoice_dfs, how="horizontal")


# (
#     df
#     .pipe(onehot_multichoices, "id", ["multichoice_col1", "multichoice_col2"], "\n")
# )
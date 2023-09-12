import polars as pl
import pandas as pd
from onehot_survey import onehot_multichoices


def from_dummies(
    df: pl.DataFrame, cols: list[str], separator: str = "_"
) -> pl.DataFrame:
    col_exprs: dict = {}

    for col in cols:
        name, value = col.rsplit(separator, maxsplit=1)
        expr = (
            pl.when(pl.col(col) == 1)
            .then(pl.lit(value))
            .otherwise(
                pl.when(pl.col(col).ne(0)).then(
                    raise ValueError(
                            "Dummy DataFrame contains multi-assignments"
                        )
                )
            )
        )
        col_exprs.setdefault(name, []).append(expr)

    return df.select(
        [pl.col("*").exclude(cols)]
        + [
            pl.coalesce(exprs).alias(
                name
            )  # keep the first non-null expression value by row
            for name, exprs in col_exprs.items()
        ]
    )


# df = pl.from_repr(
#     """shape: (20, 5)
#     ┌────────────────┬──────────────────────┬────────────┬──────────────────┬────────────┐
#     │ 選擇本院的原因 ┆ 請注意               ┆ A.口腔檢查 ┆ B.治療疼痛       ┆ C.醫療諮詢 │
#     │ ---            ┆ ---                  ┆ ---        ┆ ---              ┆ ---        │
#     │ str            ┆ str                  ┆ str        ┆ str              ┆ str        │
#     ╞════════════════╪══════════════════════╪════════════╪══════════════════╪════════════╡
#     │ 未填           ┆ 未填                 ┆ 洗牙       ┆ 未填             ┆ 未填       │
#     │ 親友           ┆ 未填                 ┆ 未填       ┆ 未填             ┆ 未填       │
#     │ 其他           ┆ 未填                 ┆ 蛀牙       ┆ 牙齒痛, 根管治療 ┆ 未填       │
#     │ 親友           ┆ 本人非常怕痛         ┆ 蛀牙       ┆ 牙齒痛           ┆ 牙周病     │
#     │ …              ┆ …                    ┆ …          ┆ …                ┆ …          │
#     │ 親友           ┆ 未填                 ┆ 未填       ┆ 牙肉腫           ┆ 未填       │
#     │ 親友           ┆ 未填                 ┆ 洗牙       ┆ 未填             ┆ 未填       │
#     │ 住家           ┆ 本人非常怕痛, 很緊張 ┆ 未填       ┆ 牙齒痛           ┆ 未填       │
#     │ 未填           ┆ 未填                 ┆ 未填       ┆ 未填             ┆ 未填       │
#     └────────────────┴──────────────────────┴────────────┴──────────────────┴────────────┘
#     """
# )
# print(
#     (
#         onehot_df := df.pipe(onehot_multichoices, r", ").select(
#             pl.col(pl.Int8)
#         )
#     ).pipe(from_dummies, onehot_df.columns, separator="__")
# )

# for i in pl.col("^請注意__.*$"):
#     print(i)
# print(df.select(pl.col('選擇本院的原因').cast(pl.Categorical).lengths()))

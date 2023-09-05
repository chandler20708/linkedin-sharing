import polars as pl
from polars.testing import assert_frame_equal

# ANCHOR -  Columns in the left frame, but not in the right and visa versa:
left = pl.DataFrame({
    "A": [1, 2, 3],
    "B": [4, 5, 6]
})

right = pl.DataFrame({
    "A": [1, 2, 3]
})

# assert_frame_equal(left, right)

# ANCHOR -  Columns are not in the same order:
left = pl.DataFrame({
    "A": [1, 2, 3],
    "B": [4, 5, 6]
})

right = pl.DataFrame({
    "B": [4, 5, 6],
    "A": [1, 2, 3]
})

# assert_frame_equal(left, right)

# ANCHOR -  Values for a column are different:
left = pl.DataFrame({
    "A": [1, 2, 3]
})

right = pl.DataFrame({
    "A": [1, 2, 4]
})

# assert_frame_equal(left, right)




import numpy as np
from numpy.testing import assert_array_equal

from advent_of_code.helpers import to_numpy_array


def test_to_numpy_array():
    input = "ab \n12Y"
    expected = np.array(
        [
            ["a", "b", " "],
            ["1", "2", "Y"],
        ],
        dtype="U1",
    )
    assert_array_equal(to_numpy_array(input), expected)

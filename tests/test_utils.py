import pytest
import numpy as np
from moments.utils import TH1R


def test_th1r():
    with pytest.raises(TypeError):
        TH1R("hist", "title")  # ROOT doesn't support this

    basic = TH1R("hist", "title", 100, 0, 100)
    assert basic is not None
    assert TH1R(basic)

    intended = TH1R.form(np.array([1, 1]), np.array([0, 1, 2]))
    assert intended is not None

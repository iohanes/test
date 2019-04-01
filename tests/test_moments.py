import pytest
import numpy as np
from moments.utils import TH1R
from moments.models import BinMoment


@pytest.fixture
def data():
    size = 100
    data = np.random.uniform(10, 10000, size)
    edges = np.linspace(0, 100, size + 1)
    return TH1R.form(data, edges)


def test_calculates_moments(data):
    moment = BinMoment(data).moments()
    assert type(moment) == np.ndarray
    assert moment.shape[0] > 0

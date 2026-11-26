import pytest

from src.manager import Manager
from src.models import Parameters


def test_rozliczenie_mieszkania():
    manager = Manager(Parameters())
    r = manager.rozliczenie_mieszkania('apart-polanka', 2025, 1)
    assert r.apartment == 'apart-polanka'
    assert r.year == 2025
    assert r.month == 1
    assert r.total_bills_pln == 910.0
    assert r.total_rent_pln == 0.0
    assert r.total_due_pln == -910.0

    r = manager.rozliczenie_mieszkania('apart-polanka', 2025, 2)
    assert r.month == 2
    assert r.total_bills_pln == 0.0
    assert r.total_rent_pln == 0.0
    assert r.total_due_pln == 0.0

    assert manager.rozliczenie_mieszkania('brak', 2025, 1) is None

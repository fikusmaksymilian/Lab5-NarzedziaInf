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


def test_rozliczenia_najemcow():
    manager = Manager(Parameters())
    r = manager.rozliczenie_mieszkania('apart-polanka', 2025, 1)

    wynik = manager.rozliczenia_najemcow(r)
    assert len(wynik) == 3
    assert wynik[0].bills_pln == pytest.approx(910.0 / 3)
    assert wynik[1].bills_pln == pytest.approx(910.0 / 3)
    assert wynik[2].bills_pln == pytest.approx(910.0 / 3)
    assert wynik[0].month == 1
    assert wynik[0].year == 2025

    del manager.tenants['tenant-3']
    wynik = manager.rozliczenia_najemcow(r)
    assert len(wynik) == 2
    assert wynik[0].bills_pln == 455.0
    assert wynik[1].bills_pln == 455.0

    del manager.tenants['tenant-2']
    wynik = manager.rozliczenia_najemcow(r)
    assert len(wynik) == 1
    assert wynik[0].tenant == 'tenant-1'
    assert wynik[0].bills_pln == 910.0

    manager.tenants = {}
    assert manager.rozliczenia_najemcow(r) == []

from src.manager import Manager
from src.models import Parameters


def test_koszty_mieszkania():
    manager = Manager(Parameters())
    assert manager.get_apartment_costs('brak', 2025, 1) is None
    assert manager.get_apartment_costs('apart-polanka', 2025, 2) == 0.0
    assert manager.get_apartment_costs('apart-polanka', 2024, 1) == 0.0
    assert manager.get_apartment_costs('apart-polanka', 2025, 1) == 910.0

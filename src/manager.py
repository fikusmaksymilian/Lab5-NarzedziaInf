from src.models import Apartment, ApartmentSettlement, Bill, Parameters, Tenant, TenantSettlement, Transfer


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True
    def get_apartment_costs(self, apartment_key, year=None, month=None):
        if month is not None and (month < 1 or month > 12):
            raise ValueError("zly miesiac")
        if apartment_key not in self.apartments:
            return None
        suma = 0.0
        for rachunek in self.bills:
            if rachunek.apartment != apartment_key:
                continue
            if year is not None and rachunek.settlement_year != year:
                continue
            if month is not None and rachunek.settlement_month != month:
                continue
            suma += rachunek.amount_pln
        return suma

    def rozliczenie_mieszkania(self, apartment_key, year, month):
        rachunki = self.get_apartment_costs(apartment_key, year, month)
        if rachunki is None:
            return None
        return ApartmentSettlement(
            apartment=apartment_key,
            year=year,
            month=month,
            total_rent_pln=0.0,
            total_bills_pln=rachunki,
            total_due_pln=0.0 - rachunki
        )

    def rozliczenia_najemcow(self, rozliczenie):
        najemcy = []
        for klucz, najemca in self.tenants.items():
            if najemca.apartment == rozliczenie.apartment:
                najemcy.append(klucz)
        wynik = []
        for klucz in najemcy:
            czesc = rozliczenie.total_bills_pln / len(najemcy)
            wynik.append(TenantSettlement(
                tenant=klucz,
                apartment_settlement=rozliczenie.apartment,
                month=rozliczenie.month,
                year=rozliczenie.year,
                rent_pln=0.0,
                bills_pln=czesc,
                total_due_pln=czesc,
                balance_pln=0.0 - czesc
            ))
        return wynik

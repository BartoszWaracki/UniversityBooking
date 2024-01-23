from repos import UzytkownikRepository  # Upewnij się, że importujesz klasę a nie moduł
from repos import RezerwacjaRepository
from Uzytkownik import Rezerwacja
from extensions import db
from flask import session
from datetime import datetime


class AuthService:
    def __init__(self, db):
        self.uzytkownik_repository = UzytkownikRepository(db)

    def zaloguj_przez_baze_danych(self, username, password):
        user = self.uzytkownik_repository.znajdz_po_loginie_i_hasle(username, password)
        return user


class RezerwacjaService:
    def __init__(self, db):
        self.rezerwacja_repository = RezerwacjaRepository(session)

    def anuluj_rezerwacje(self, rezerwacja_id):
        self.rezerwacja_repository.usun(rezerwacja_id)
        # self, sala_id, czas_start, czas_koniec, wykladowca_id, tytul, student_id=None
    def zarezerwuj_sala(self,tytul, czas_start, czas_koniec, wykladowca_id,sala):
    
        try:
            nowa_rezerwacja = Rezerwacja(
                czas_start=czas_start,
                czas_koniec=czas_koniec,
                data=czas_start.date(),  # Założenie, że data rezerwacji to data rozpoczęcia
                czas_trwania=(czas_koniec - czas_start).seconds // 3600,
                tytul=tytul,
                wykladowca_id=wykladowca_id,
                sala_id=sala,
                # student_id=student_id  # Opcjonalne
            )
            self.rezerwacja_repository.dodaj(nowa_rezerwacja)
            return True
        except Exception as e:
            print(f"Wystąpił błąd: {e}")
            return False

    def edytuj_rezerwacje(self, rezerwacja_id, nowe_dane):
        pass

    def dodaj_sprzet_do_rezerwacji(self, rezerwacja_id, sprzet_id):
        pass













# ⠀⢀⣤⡀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⣿⠉⢻⠟⢹⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⢀⣿⡄⠀⠀⣼⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣄⣠⣤⣄⠀⠀⠀⠀
# ⠀⠀⣰⡿⠋⠀⣀⣀⠈⣿⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣇⠘⠋⠀⣿⠇⠀⠀⠀
# ⠀⣠⡟⠀⢀⣾⠟⠻⠿⠿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⡀⠀⠀⣾⠋⢀⣀⠈⠻⢶⣄⠀⠀
# ⢠⣿⠁⣰⡿⠁⠀⣀⣤⣶⣶⡶⢶⣤⣄⡀⢀⣠⠴⠚⠉⠉⠉⠉⠉⠙⢶⡄⠛⠒⠛⠙⢳⣦⡀⠹⣆⠀
# ⢸⡇⢠⣿⣠⣴⣿⡟⢉⣠⠤⠶⠶⠾⠯⣿⣿⣧⣀⣤⣶⣾⣿⡿⠿⠛⠋⢙⣛⡛⠳⣄⡀⠙⣷⡀⢹⡆
# ⢸⠀⢸⣿⣿⣿⣿⠞⠉⠀⠀⠀⠀⣀⣤⣤⠬⠉⠛⠻⠿⠟⠉⢀⣠⢞⣭⣤⣤⣍⠙⠺⢷⡀⢸⡇⠀⣿
# ⢸⠀⢸⣿⣿⡟⠀⠀⠀⢀⣠⠞⣫⢗⣫⢽⣶⣤⣀⠉⠛⣶⠖⠛⠀⣾⡷⣾⠋⣻⡆⠀⠀⡇⣼⠇⠀⣿
# ⢸⠀⠀⣿⣿⡇⢠⡤⠔⣋⡤⠞⠁⢸⣷⣾⣯⣹⣿⡆⢀⣏⠀⠈⠈⣿⣷⣼⣿⠿⠷⣴⡞⠀⣿⠀⠀⣿
# ⢸⠀⠀⢿⣿⡇⠀⠀⠘⠻⠤⣀⡀⠸⣿⣯⣿⣿⡿⠷⠚⠉⠛⠛⠛⠛⠉⠉⠀⣠⡾⠛⣦⢸⡏⠀⠀⣿
# ⢸⠀⠀⢸⣿⡇⠀⣠⠶⠶⠶⠶⠿⣿⣭⣭⣁⣀⣠⣤⣤⣤⣤⣤⣤⡶⠶⠛⠋⢁⣀⣴⠟⣽⠇⠀⠀⣿
# ⢸⠀⠀⢸⣿⡇⢾⣅⠀⠀⠶⠶⢦⣤⣤⣀⣉⣉⣉⣉⣁⣡⣤⣤⣴⡶⠶⠶⠚⠉⢉⡿⣠⠟⠀⠀⣰⡟
# ⢸⡀⠀⠀⢿⣇⠀⠈⠛⠳⠶⠤⠤⢤⣀⣉⣉⣉⣉⣉⣉⣁⣀⣠⣤⡤⠤⠤⠶⠞⢻⡟⠃⠀⠀⣰⠟⠀
# ⢸⣧⠀⠀⠘⣿⣦⣄⡀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⣠⣤⣶⣿⣧⣀⣴⠟⠃⠀⠀
# ⠀⢻⣆⠀⠀⠈⢻⣿⣿⣷⣶⣤⣄⣀⣀⣀⣠⣤⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣟⡉⠀⠀⠀⠀⠀
# ⠀⠀⢻⣦⡄⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀
# ⠀⢀⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡧⠀⠀⠀


# class AuthService:
#     def __init__(self, db):
#         self.uzytkownik_repository = UzytkownikRepository(db)

#     def zaloguj_przez_baze_danych(self, username, password):
#         user = self.uzytkownik_repository.znajdz_po_loginie_i_hasle(username, password)
#         return user


# class RezerwacjaService:
#     def __init__(self, db):
#         self.rezerwacja_repository = RezerwacjaRepository(session)

#     def anuluj_rezerwacje(self, rezerwacja_id):
#         self.rezerwacja_repository.usun(rezerwacja_id)
#         # self, sala_id, czas_start, czas_koniec, wykladowca_id, tytul, student_id=None
#     def zarezerwuj_sala(self,tytul, czas_start, czas_koniec, wykladowca_id):
    
#         try:
#             nowa_rezerwacja = Rezerwacja(
#                 czas_start=czas_start,
#                 czas_koniec=czas_koniec,
#                 data=czas_start.date(),  # Założenie, że data rezerwacji to data rozpoczęcia
#                 czas_trwania=(czas_koniec - czas_start).seconds // 3600,
#                 tytul=tytul,
#                 wykladowca_id=wykladowca_id,
#                 # sala_id=sala_id,
#                 # student_id=student_id  # Opcjonalne
#             )
#             self.rezerwacja_repository.dodaj(nowa_rezerwacja)
#             return True
#         except Exception as e:
#             print(f"Wystąpił błąd: {e}")
#             return False

#     def edytuj_rezerwacje(self, rezerwacja_id, nowe_dane):
#         pass

#     def dodaj_sprzet_do_rezerwacji(self, rezerwacja_id, sprzet_id):
#         pass
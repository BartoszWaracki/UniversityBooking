from Uzytkownik import Uzytkownik, Wykladowca,Rezerwacja,Sala,Budynek
from sqlalchemy.orm import Session
from extensions import db
from flask import request, redirect, url_for, flash, session, render_template
from sqlalchemy import and_, or_, not_
from dateutil import parser
from sqlalchemy.sql import exists
from datetime import datetime


class UzytkownikRepository:
    def __init__(self, db):
        self.db = db
        self.session = session
        uzytkownik = Uzytkownik

    def znajdz_po_loginie_i_hasle(self, login, haslo):
        return Uzytkownik.query.filter_by(login=login, haslo=haslo).first() 
        

    def znajdz_wszystkich(self):
        return Uzytkownik.query.all()

    def znajdz_po_id(self, id):
        return Uzytkownik.query.get(id)

    def dodaj(self, uzytkownik):
        self.db.session.add(uzytkownik)
        self.db.session.commit()

    def aktualizuj(self, uzytkownik):
        self.db.session.commit()

    def usun(self, id):
        uzytkownik = self.znajdz_po_id(id)
        if uzytkownik:
            self.db.session.delete(uzytkownik)
            self.db.session.commit()


    def pobierz_rezerwacje_uzytkownika(self, user_id):
        wykladowca = Wykladowca.query.filter_by(uzytkownik_id=user_id).first()
        if wykladowca:
            return Rezerwacja.query.filter_by(wykladowca_id=wykladowca.wykladowca_id).all()
        return []

class RezerwacjaRepository:
    def __init__(self, session):
        self.db = db
        self.session = session

    def znajdz_wszystkie(self):
        return Rezerwacja.query.all()

    def znajdz_po_id(self, id):
        return Rezerwacja.query.get(id)

    def dodaj(self, rezerwacja):
        self.db.session.add(rezerwacja)
        self.db.session.commit()

    def aktualizuj(self, rezerwacja):
        self.db.session.commit()

    def usun(self, id):
        rezerwacja = self.znajdz_po_id(id)
        if rezerwacja:
            self.db.session.delete(rezerwacja)
            self.db.session.commit()
            return True
        return False
    
class SalaRepository:
    def __init__(self, session, db):
        self.db = db
        self.session = session

    def znajdz_wszystkie(self):
        return self.session.query(Sala).all()

    def znajdz_po_numerze_sali(self, numer_sali):
        return self.session.query(Sala).filter_by(numer_sali=numer_sali).first()

    def dodaj(self, sala):
        self.session.add(sala)
        self.session.commit()

    def aktualizuj(self, sala):
        self.session.commit()

    def usun(self, numer_sali):
        sala = self.znajdz_po_numerze_sali(numer_sali)
        if sala:
            self.session.delete(sala)
            self.session.commit()
            return True
        return False
    def znajdz_wszystkie_budynki(self):
        return self.session.query(Budynek).all()

    def sprawdz_dostepnosc(self, budynek_id, czas_start_str, czas_koniec_str):
    # Convert strings to datetime objects
       
        date_part, time_part = czas_start_str.split('T')
        time_part = time_part.split(' ')[0]  # Keep only the time part without timezone offset              
        formatted_str = f'{date_part} {time_part}'     
        czas_start = datetime.strptime(formatted_str, '%Y-%m-%d %H:%M:%S')

        date_part, time_part = czas_koniec_str.split('T')
        time_part = time_part.split(' ')[0]  # Keep only the time part without timezone offset              
        formatted_str = f'{date_part} {time_part}'     
        czas_koniec = datetime.strptime(formatted_str, '%Y-%m-%d %H:%M:%S')
        print(czas_start)
        print(czas_koniec)

        # Find rooms in the specified building, filter by budynek_id
        dostepne_sale = self.session.query(Sala).join(Budynek).filter(Budynek.budynek_id == budynek_id)
        
        # Check which rooms are NOT occupied within the given time range
        dostepne_sale = dostepne_sale.filter(
            ~exists().where(
                and_(
                    Rezerwacja.sala_id == Sala.numer_sali,  # Assuming Sala.id is the primary key
                    # Check for any overlap in reservations
                    not_(or_(
                        Rezerwacja.czas_koniec <= czas_start,
                        Rezerwacja.czas_start >= czas_koniec,
                    ))
                )
            )
        )

        return dostepne_sale.all()





















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


# class UzytkownikRepository:
#     def __init__(self, db):
#         self.db = db

#     def znajdz_po_loginie_i_hasle(self, login, haslo):
#         return Uzytkownik.query.filter_by(login=login, haslo=haslo).first() 
        

#     def znajdz_wszystkich(self):
#         return Uzytkownik.query.all()

#     def znajdz_po_id(self, id):
#         return Uzytkownik.query.get(id)

#     def dodaj(self, uzytkownik):
#         self.db.session.add(uzytkownik)
#         self.db.session.commit()

#     def aktualizuj(self, uzytkownik):
#         self.db.session.commit()

#     def usun(self, id):
#         uzytkownik = self.znajdz_po_id(id)
#         if uzytkownik:
#             self.db.session.delete(uzytkownik)
#             self.db.session.commit()


#     def pobierz_rezerwacje_uzytkownika(self, user_id):
#         wykladowca = Wykladowca.query.filter_by(uzytkownik_id=user_id).first()
#         if wykladowca:
#             return Rezerwacja.query.filter_by(wykladowca_id=wykladowca.wykladowca_id).all()
#         return []

# class RezerwacjaRepository:
#     def __init__(self, session):
#         self.db = db
#         self.session = session

#     def znajdz_wszystkie(self):
#         return Rezerwacja.query.all()

#     def znajdz_po_id(self, id):
#         return Rezerwacja.query.get(id)

#     def dodaj(self, rezerwacja):
#         self.db.session.add(rezerwacja)
#         self.db.session.commit()

#     def aktualizuj(self, rezerwacja):
#         self.db.session.commit()

#     def usun(self, id):
#         rezerwacja = self.znajdz_po_id(id)
#         if rezerwacja:
#             self.db.session.delete(rezerwacja)
#             self.db.session.commit()
#             return True
#         return False
    
# class SalaRepository:
#     def __init__(self, session, db):
#         self.db = db
#         self.session = session

#     def znajdz_wszystkie(self):
#         return self.session.query(Sala).all()

#     def znajdz_po_numerze_sali(self, numer_sali):
#         return self.session.query(Sala).filter_by(numer_sali=numer_sali).first()

#     def dodaj(self, sala):
#         self.session.add(sala)
#         self.session.commit()

#     def aktualizuj(self, sala):
#         self.session.commit()

#     def usun(self, numer_sali):
#         sala = self.znajdz_po_numerze_sali(numer_sali)
#         if sala:
#             self.session.delete(sala)
#             self.session.commit()
#             return True
#         return False

#     def sprawdz_dostepnosc(self, budynek_nazwa, czas_start, czas_koniec):
#         # Znajdź sale w określonym budynku
#         dostepne_sale = self.session.query(Sala).join(Budynek).filter(Budynek.nazwa == budynek_nazwa)
        
#         # Teraz sprawdź, które sale są dostępne w podanym przedziale czasowym
#         dostepne_sale = dostepne_sale.outerjoin(Rezerwacja, and_(
#             Rezerwacja.sala_id == Sala.numer_sali,
#             or_(
#                 and_(Rezerwacja.czas_start < czas_koniec, Rezerwacja.czas_koniec > czas_start),
#                 and_(Rezerwacja.czas_start == czas_start, Rezerwacja.czas_koniec == czas_koniec)
#             )
#         )).filter(Rezerwacja.rezerwacja_id == None)

#         return dostepne_sale.all()

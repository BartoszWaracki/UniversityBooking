# from extensions import db

# class Uzytkownik(db.Model):
#     __tablename__ = 'uzytkownicy'
#     id = db.Column(db.Integer, primary_key=True)
#     imie = db.Column(db.String(80))
#     nazwisko = db.Column(db.String(80))
#     login = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=False)
#     haslo = db.Column(db.String(80), nullable=False)

#     def __repr__(self):
#         return '<Uzytkownik %r>' % self.login
from extensions import db
from flask import session

from datetime import datetime

# Definicje klas
class Uzytkownik(db.Model):
    __tablename__ = 'uzytkownicy'
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(80))
    nazwisko = db.Column(db.String(80))
    login = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    haslo = db.Column(db.String(80), nullable=False)
    # Relacje ORM
    wykladowca = db.relationship("Wykladowca", back_populates="uzytkownik", uselist=False)
    student = db.relationship("Student", back_populates="uzytkownik", uselist=False)

    def __repr__(self):
        return '<Uzytkownik %r>' % self.login

class Wykladowca(db.Model):
    __tablename__ = 'wykladowcy'
    wykladowca_id = db.Column(db.Integer, primary_key=True)
    wydzial = db.Column(db.String(80))
    uzytkownik_id = db.Column(db.Integer, db.ForeignKey('uzytkownicy.id'))
    # Relacje ORM
    uzytkownik = db.relationship("Uzytkownik", back_populates="wykladowca")
    zajecia = db.relationship("Zajecia", back_populates="wykladowca")
    rezerwacje = db.relationship("Rezerwacja", back_populates="wykladowca")

class Student(db.Model):
    __tablename__ = 'studenci'
    student_id = db.Column(db.Integer, primary_key=True)
    uzytkownik_id = db.Column(db.Integer, db.ForeignKey('uzytkownicy.id'))
    # Relacje ORM
    uzytkownik = db.relationship("Uzytkownik", back_populates="student")
    zapisane_przedmioty = db.relationship("Przedmiot", secondary='zapisy', back_populates="zapisani_studenci")
    rezerwacje = db.relationship('Rezerwacja', back_populates='student')

class Przedmiot(db.Model):
    __tablename__ = 'przedmioty'
    przedmiot_id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(80))
    # Relacje ORM
    zapisani_studenci = db.relationship("Student", secondary='zapisy', back_populates="zapisane_przedmioty")

class Sala(db.Model):
    __tablename__ = 'sale'
    numer_sali = db.Column(db.String(80), primary_key=True)
    pojemnosc = db.Column(db.Integer)
    budynek_id = db.Column(db.Integer, db.ForeignKey('budynki.budynek_id'))
    # Relacje ORM
    
    budynek = db.relationship('Budynek', back_populates='sale')
    lista_sprzetu = db.relationship("Sprzet", back_populates="sala")
    zajecia = db.relationship("Zajecia", back_populates="sala")
    rezerwacje = db.relationship("Rezerwacja", back_populates="sala")
class Budynek(db.Model):
    __tablename__ = 'budynki'
    budynek_id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(80), nullable=False)
    adres = db.Column(db.String(120), nullable=False)
    sale = db.relationship('Sala', back_populates='budynek')

    

class Rezerwacja(db.Model):
    __tablename__ = 'rezerwacje'
    rezerwacja_id = db.Column(db.Integer, primary_key=True)
    czas_start = db.Column(db.DateTime)
    czas_koniec = db.Column(db.DateTime)
    data = db.Column(db.Date)
    czas_trwania = db.Column(db.Integer)
    tytul = db.Column(db.String(80))
    wykladowca_id = db.Column(db.Integer, db.ForeignKey('wykladowcy.wykladowca_id'))
    sala_id = db.Column(db.String(80), db.ForeignKey('sale.numer_sali'))
    student_id = db.Column(db.Integer, db.ForeignKey('studenci.student_id'))
    
    # Relacje ORM
    wykladowca = db.relationship("Wykladowca", back_populates="rezerwacje")
    sala = db.relationship("Sala", back_populates="rezerwacje")
    student = db.relationship('Student', back_populates='rezerwacje')

    def to_dict(self):
        return {
            'id': self.rezerwacja_id,
            'title': f"{self.tytul} - Sala {self.sala.numer_sali}, {self.sala.budynek.nazwa}" if self.sala else self.tytul,
            'start': self.czas_start.isoformat() if self.czas_start else None,
            'end': self.czas_koniec.isoformat() if self.czas_koniec else None,
            'date': self.data.isoformat() if self.data else None,
            'duration': self.czas_trwania,
            'room_number': self.sala_id,
            'teacher_id': self.wykladowca_id,
            'student_id': self.student_id
        }


class Zajecia(db.Model):
    __tablename__ = 'zajecia'
    zajecia_id = db.Column(db.Integer, primary_key=True)
    czas_start = db.Column(db.DateTime)
    czas_koniec = db.Column(db.DateTime)
    wykladowca_id = db.Column(db.Integer, db.ForeignKey('wykladowcy.wykladowca_id'))
    przedmiot_id = db.Column(db.Integer, db.ForeignKey('przedmioty.przedmiot_id'))
    sala_numer = db.Column(db.String(80), db.ForeignKey('sale.numer_sali'))
    # Relacje ORM
    wykladowca = db.relationship("Wykladowca", back_populates="zajecia")
    przedmiot = db.relationship("Przedmiot")
    lista_studentow = db.relationship("Student", secondary='obecnosci')
    sala = db.relationship("Sala", back_populates="zajecia")

class Sprzet(db.Model):
    __tablename__ = 'sprzet'
    sprzet_id = db.Column(db.Integer, primary_key=True)
    typ = db.Column(db.String(80))
    status = db.Column(db.String(80))
    sala_numer = db.Column(db.String(80), db.ForeignKey('sale.numer_sali'))
    # Relacje ORM
    sala = db.relationship("Sala", back_populates="lista_sprzetu")

# Tabele pomocnicze dla relacji many-to-many
zapisy = db.Table('zapisy',
    db.Column('student_id', db.Integer, db.ForeignKey('studenci.student_id')),
    db.Column('przedmiot_id', db.Integer, db.ForeignKey('przedmioty.przedmiot_id'))
)

obecnosci = db.Table('obecnosci',
    db.Column('student_id', db.Integer, db.ForeignKey('studenci.student_id')),
    db.Column('zajecia_id', db.Integer, db.ForeignKey('zajecia.zajecia_id'))
)




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

# # Definicje klas
# class Uzytkownik(db.Model):
#     __tablename__ = 'uzytkownicy'
#     id = db.Column(db.Integer, primary_key=True)
#     imie = db.Column(db.String(80))
#     nazwisko = db.Column(db.String(80))
#     login = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True)
#     haslo = db.Column(db.String(80), nullable=False)
#     # Relacje ORM
#     wykladowca = db.relationship("Wykladowca", back_populates="uzytkownik", uselist=False)
#     student = db.relationship("Student", back_populates="uzytkownik", uselist=False)

#     def __repr__(self):
#         return '<Uzytkownik %r>' % self.login

# class Wykladowca(db.Model):
#     __tablename__ = 'wykladowcy'
#     wykladowca_id = db.Column(db.Integer, primary_key=True)
#     wydzial = db.Column(db.String(80))
#     uzytkownik_id = db.Column(db.Integer, db.ForeignKey('uzytkownicy.id'))
#     # Relacje ORM
#     uzytkownik = db.relationship("Uzytkownik", back_populates="wykladowca")
#     zajecia = db.relationship("Zajecia", back_populates="wykladowca")
#     rezerwacje = db.relationship("Rezerwacja", back_populates="wykladowca")

# class Student(db.Model):
#     __tablename__ = 'studenci'
#     student_id = db.Column(db.Integer, primary_key=True)
#     uzytkownik_id = db.Column(db.Integer, db.ForeignKey('uzytkownicy.id'))
#     # Relacje ORM
#     uzytkownik = db.relationship("Uzytkownik", back_populates="student")
#     zapisane_przedmioty = db.relationship("Przedmiot", secondary='zapisy', back_populates="zapisani_studenci")
#     rezerwacje = db.relationship('Rezerwacja', back_populates='student')

# class Przedmiot(db.Model):
#     __tablename__ = 'przedmioty'
#     przedmiot_id = db.Column(db.Integer, primary_key=True)
#     nazwa = db.Column(db.String(80))
#     # Relacje ORM
#     zapisani_studenci = db.relationship("Student", secondary='zapisy', back_populates="zapisane_przedmioty")

# class Sala(db.Model):
#     __tablename__ = 'sale'
#     numer_sali = db.Column(db.String(80), primary_key=True)
#     pojemnosc = db.Column(db.Integer)
#     budynek_id = db.Column(db.Integer, db.ForeignKey('budynki.budynek_id'))
#     # Relacje ORM
    
#     budynek = db.relationship('Budynek', back_populates='sale')
#     lista_sprzetu = db.relationship("Sprzet", back_populates="sala")
#     zajecia = db.relationship("Zajecia", back_populates="sala")
#     rezerwacje = db.relationship("Rezerwacja", back_populates="sala")
# class Budynek(db.Model):
#     __tablename__ = 'budynki'
#     budynek_id = db.Column(db.Integer, primary_key=True)
#     nazwa = db.Column(db.String(80), nullable=False)
#     adres = db.Column(db.String(120), nullable=False)
#     sale = db.relationship('Sala', back_populates='budynek')

    

# class Rezerwacja(db.Model):
#     __tablename__ = 'rezerwacje'
#     rezerwacja_id = db.Column(db.Integer, primary_key=True)
#     czas_start = db.Column(db.DateTime)
#     czas_koniec = db.Column(db.DateTime)
#     data = db.Column(db.Date)
#     czas_trwania = db.Column(db.Integer)
#     tytul = db.Column(db.String(80))
#     wykladowca_id = db.Column(db.Integer, db.ForeignKey('wykladowcy.wykladowca_id'))
#     sala_id = db.Column(db.String(80), db.ForeignKey('sale.numer_sali'))
#     student_id = db.Column(db.Integer, db.ForeignKey('studenci.student_id'))
    
#     # Relacje ORM
#     wykladowca = db.relationship("Wykladowca", back_populates="rezerwacje")
#     sala = db.relationship("Sala", back_populates="rezerwacje")
#     student = db.relationship('Student', back_populates='rezerwacje')

#     def to_dict(self):
#         return {
#             'id': self.rezerwacja_id,
#             'title': f"{self.tytul} - Sala {self.sala.numer_sali}, {self.sala.budynek.nazwa}" if self.sala else self.tytul,
#             'start': self.czas_start.isoformat() if self.czas_start else None,
#             'end': self.czas_koniec.isoformat() if self.czas_koniec else None,
#             'date': self.data.isoformat() if self.data else None,
#             'duration': self.czas_trwania,
#             'room_number': self.sala_id,
#             'teacher_id': self.wykladowca_id,
#             'student_id': self.student_id
#         }


# class Zajecia(db.Model):
#     __tablename__ = 'zajecia'
#     zajecia_id = db.Column(db.Integer, primary_key=True)
#     czas_start = db.Column(db.DateTime)
#     czas_koniec = db.Column(db.DateTime)
#     wykladowca_id = db.Column(db.Integer, db.ForeignKey('wykladowcy.wykladowca_id'))
#     przedmiot_id = db.Column(db.Integer, db.ForeignKey('przedmioty.przedmiot_id'))
#     sala_numer = db.Column(db.String(80), db.ForeignKey('sale.numer_sali'))
#     # Relacje ORM
#     wykladowca = db.relationship("Wykladowca", back_populates="zajecia")
#     przedmiot = db.relationship("Przedmiot")
#     lista_studentow = db.relationship("Student", secondary='obecnosci')
#     sala = db.relationship("Sala", back_populates="zajecia")

# class Sprzet(db.Model):
#     __tablename__ = 'sprzet'
#     sprzet_id = db.Column(db.Integer, primary_key=True)
#     typ = db.Column(db.String(80))
#     status = db.Column(db.String(80))
#     sala_numer = db.Column(db.String(80), db.ForeignKey('sale.numer_sali'))
#     # Relacje ORM
#     sala = db.relationship("Sala", back_populates="lista_sprzetu")

# # Tabele pomocnicze dla relacji many-to-many
# zapisy = db.Table('zapisy',
#     db.Column('student_id', db.Integer, db.ForeignKey('studenci.student_id')),
#     db.Column('przedmiot_id', db.Integer, db.ForeignKey('przedmioty.przedmiot_id'))
# )

# obecnosci = db.Table('obecnosci',
#     db.Column('student_id', db.Integer, db.ForeignKey('studenci.student_id')),
#     db.Column('zajecia_id', db.Integer, db.ForeignKey('zajecia.zajecia_id'))
# )

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import declarative_base
Base = declarative_base()


# Definicje klas
class Uzytkownik(Base):
    __tablename__ = 'uzytkownicy'
    id = Column(Integer, primary_key=True)
    imie = Column(String)
    nazwisko = Column(String)
    login = Column(String)
    email = Column(String)
    haslo = Column(String)
    # Relacje ORM
    wykladowca = relationship("Wykladowca", back_populates="uzytkownik", uselist=False)
    student = relationship("Student", back_populates="uzytkownik", uselist=False)

class Wykladowca(Base):
    __tablename__ = 'wykladowcy'
    wykladowca_id = Column(Integer, primary_key=True)
    wydzial = Column(String)
    uzytkownik_id = Column(Integer, ForeignKey('uzytkownicy.id'))
    # Relacje ORM
    uzytkownik = relationship("Uzytkownik", back_populates="wykladowca")
    zajecia = relationship("Zajecia", back_populates="wykladowca")
    rezerwacje = relationship("Rezerwacja", back_populates="wykladowca")

class Student(Base):
    __tablename__ = 'studenci'
    student_id = Column(Integer, primary_key=True)
    uzytkownik_id = Column(Integer, ForeignKey('uzytkownicy.id'))
    # Relacje ORM
    uzytkownik = relationship("Uzytkownik", back_populates="student")
    rezerwacje = relationship("Rezerwacja", back_populates="student")
    zapisane_przedmioty = relationship("Przedmiot", secondary='zapisy', back_populates="zapisani_studenci")

class Przedmiot(Base):
    __tablename__ = 'przedmioty'
    przedmiot_id = Column(Integer, primary_key=True)
    nazwa = Column(String)
    # Relacje ORM
    zapisani_studenci = relationship("Student", secondary='zapisy', back_populates="zapisane_przedmioty")

class Sala(Base):
    __tablename__ = 'sale'
    numer_sali = Column(String, primary_key=True)
    pojemnosc = Column(Integer)
    budynek_id = Column(Integer, ForeignKey('budynki.budynek_id'))  # Foreign key reference
    # Relacje ORM
    lista_sprzetu = relationship("Sprzet", back_populates="sala")
    zajecia = relationship("Zajecia", back_populates="sala")
    rezerwacje = relationship("Rezerwacja", back_populates="sala")
    budynek = relationship("Budynek", back_populates="sale")  # Relationship to Budynek

class Budynek(Base):
    __tablename__ = 'budynki'
    budynek_id = Column(Integer, primary_key=True)
    nazwa = Column(String)
    adres = Column(String)
    sale = relationship("Sala", back_populates="budynek")  # One-to-many relationship



class Rezerwacja(Base):
    __tablename__ = 'rezerwacje'
    rezerwacja_id = Column(Integer, primary_key=True)
    czas_start = Column(DateTime)
    czas_koniec = Column(DateTime)
    data = Column(Date)
    czas_trwania = Column(Integer)
    tytul = Column(String)  # Add this line to include the 'tytul' column
    wykladowca_id = Column(Integer, ForeignKey('wykladowcy.wykladowca_id'))
    student_id = Column(Integer, ForeignKey('studenci.student_id'))
    sala_id = Column(String, ForeignKey('sale.numer_sali'))

    # Relacje ORM
    wykladowca = relationship("Wykladowca", back_populates="rezerwacje")
    student = relationship("Student", back_populates="rezerwacje")
    sala = relationship("Sala", back_populates="rezerwacje")




class Zajecia(Base):
    __tablename__ = 'zajecia'
    zajecia_id = Column(Integer, primary_key=True)
    czas_start = Column(DateTime)
    czas_koniec = Column(DateTime)
    wykladowca_id = Column(Integer, ForeignKey('wykladowcy.wykladowca_id'))
    przedmiot_id = Column(Integer, ForeignKey('przedmioty.przedmiot_id'))
    sala_numer = Column(String, ForeignKey('sale.numer_sali'))
    # Relacje ORM
    wykladowca = relationship("Wykladowca", back_populates="zajecia")
    przedmiot = relationship("Przedmiot")
    lista_studentow = relationship("Student", secondary='obecnosci')
    sala = relationship("Sala", back_populates="zajecia")

class Sprzet(Base):
    __tablename__ = 'sprzet'
    sprzet_id = Column(Integer, primary_key=True)
    typ = Column(String)
    status = Column(String)
    sala_numer = Column(String, ForeignKey('sale.numer_sali'))
    # Relacje ORM
    sala = relationship("Sala", back_populates="lista_sprzetu")

# Tabele pomocnicze dla relacji many-to-many
zapisy = Table('zapisy', Base.metadata,
    Column('student_id', Integer, ForeignKey('studenci.student_id')),
    Column('przedmiot_id', Integer, ForeignKey('przedmioty.przedmiot_id'))
)

obecnosci = Table('obecnosci', Base.metadata,
    Column('student_id', Integer, ForeignKey('studenci.student_id')),
    Column('zajecia_id', Integer, ForeignKey('zajecia.zajecia_id'))
)

# Tabela pośrednicząca dla relacji wiele-do-wielu
student_rezerwacja = Table('student_rezerwacja', Base.metadata,
    Column('student_id', Integer, ForeignKey('studenci.student_id')),
    Column('rezerwacja_id', Integer, ForeignKey('rezerwacje.rezerwacja_id'))
)


# Tworzenie bazy danych
engine = create_engine('sqlite:///uniwersytet.db')
Base.metadata.create_all(engine)

# Dodawanie przykładowych danych
Session = sessionmaker(bind=engine)
session = Session()

# Przykładowi użytkownicy
uzytkownik1 = Uzytkownik(imie='Jan', nazwisko='Kowalski', login='jkowalski', email='jan.kowalski@example.com', haslo='haslo123')
uzytkownik2 = Uzytkownik(imie='Anna', nazwisko='Nowak', login='anowak', email='anna.nowak@example.com', haslo='haslo321')

session.add(uzytkownik1)
session.add(uzytkownik2)

# Przykładowi wykładowcy
wykladowca1 = Wykladowca(wydzial='Informatyka', uzytkownik=uzytkownik1)
wykladowca2 = Wykladowca(wydzial='Matematyka', uzytkownik=uzytkownik2)

session.add(wykladowca1)
session.add(wykladowca2)

# Przykładowi studenci
student1 = Student(uzytkownik=Uzytkownik(imie='Tomasz', nazwisko='Borowski', login='tborowski', email='tomasz.borowski@example.com', haslo='haslo456'))
student2 = Student(uzytkownik=Uzytkownik(imie='Katarzyna', nazwisko='Zielińska', login='kzielinska', email='katarzyna.zielinska@example.com', haslo='haslo654'))

session.add(student1)
session.add(student2)

# Przykładowe przedmioty
przedmiot1 = Przedmiot(nazwa='Programowanie Obiektowe')
przedmiot2 = Przedmiot(nazwa='Analiza Matematyczna')

session.add(przedmiot1)
session.add(przedmiot2)

# Przykładowe sale
budynek1 = Budynek(nazwa='Główny budynek', adres='ul. Akademicka 1')
budynek2 = Budynek(nazwa='Budynek sportowy', adres='ul. Sportowa 2')

session.add(budynek1)
session.add(budynek2)

# Dodawanie sali z przypisaniem do budynku
sala1 = Sala(numer_sali='101', pojemnosc=30, budynek=budynek1)
sala2 = Sala(numer_sali='102', pojemnosc=20, budynek=budynek1)
sala3 = Sala(numer_sali='201', pojemnosc=25, budynek=budynek2)

session.add(sala1)
session.add(sala2)
session.add(sala3)

# Przykładowe rezerwacje
rezerwacja1 = Rezerwacja(czas_start=datetime(2024, 2, 15, 8, 0), czas_koniec=datetime(2024, 2, 15, 10, 0), data=datetime(2024, 2, 15).date(), czas_trwania=2, wykladowca=wykladowca1, sala=sala1, student=student1)
rezerwacja2 = Rezerwacja(czas_start=datetime(2024, 3, 1, 10, 0), czas_koniec=datetime(2024, 3, 1, 12, 0), data=datetime(2024, 3, 1).date(), czas_trwania=2, wykladowca=wykladowca2, sala=sala2, student=student2)


rezerwacja3 = Rezerwacja(czas_start=datetime(2024, 2, 13, 10, 0), czas_koniec=datetime(2024, 2, 13, 12, 0), data=datetime(2024, 3, 1).date(), czas_trwania=2, wykladowca=wykladowca1, sala=sala2,student=student2)
session.add(rezerwacja1)
session.add(rezerwacja2)
session.add(rezerwacja3)

# Przykładowe zajęcia
zajecia1 = Zajecia(czas_start=datetime(2024, 2, 16, 8, 0), czas_koniec=datetime(2024, 2, 16, 10, 0), wykladowca=wykladowca1, przedmiot=przedmiot1, sala=sala1)
zajecia2 = Zajecia(czas_start=datetime(2024, 3, 2, 10, 0), czas_koniec=datetime(2024, 3, 2, 12, 0), wykladowca=wykladowca2, przedmiot=przedmiot2, sala=sala2)

session.add(zajecia1)
session.add(zajecia2)

# Przykładowy sprzęt
sprzet1 = Sprzet(typ='Projektor', status='Dostępny', sala=sala1)
sprzet2 = Sprzet(typ='Komputer', status='Niedostępny', sala=sala2)

session.add(sprzet1)
session.add(sprzet2)

# Zapisanie wszystkich zmian
session.commit()




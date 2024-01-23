from flask import request, redirect, url_for, flash, session, render_template
from Uzytkownik import Uzytkownik  # Załóżmy, że Uzytkownik.py jest w tym samym katalogu
from repos import UzytkownikRepository, RezerwacjaRepository,SalaRepository  # Upewnij się, że importujesz klasę a nie moduł
from Services import AuthService,RezerwacjaService
from flask import jsonify
from datetime import datetime
from dateutil import parser

class UserController:
    def __init__(self, db):
        self.uzytkownik_repository = UzytkownikRepository(db)
        self.auth_service = AuthService(db)  
        self.rezerwacja_service = RezerwacjaService(RezerwacjaRepository(session))
        self.sala_repository = SalaRepository(db.session, db) 
    def login(self):
        if request.method == 'POST':
            username = request.form["login"]
            password = request.form['haslo']
            
            user = self.auth_service.zaloguj_przez_baze_danych(username, password)
            if user:
                session['logged_in'] = True
                session['user_id'] = user.id  # Ustawienie identyfikatora użytkownika w sesji
                return redirect(url_for('calendar'))
            else:
                flash('Invalid username or password')
        return render_template("login.html")

    def logoff(self):
        flash('You have been logged off')
        return redirect(url_for('login'))
    
    def on_click_anuluj_rezerwacje(self, rezerwacja_id):
        if 'logged_in' in session:
            if self.rezerwacja_service.anuluj_rezerwacje(rezerwacja_id):
                flash('Rezerwacja anulowana')
                return redirect(url_for('calendar'))
            else:
                flash('Rezerwacja nie istnieje')
                return redirect(url_for('calendar'))
        else:
            flash('User not logged in')
            return redirect(url_for('login'))



    def calendar(self):
        if 'logged_in' in session and 'user_id' in session:
            user_id = session['user_id']
            rezerwacje = self.uzytkownik_repository.pobierz_rezerwacje_uzytkownika(user_id)
            rezerwacje_dict = [rez.to_dict() for rez in rezerwacje]
            return render_template("calendar.html", rezerwacje=rezerwacje_dict)
        else:
            flash('Please log in to view this page')
            return redirect(url_for('login'))

        
    def zarezerwuj_sala(self):
        
        if 'logged_in' in session:
            
            data = request.get_json()
            tytul = data.get('title')
            start = data.get('start')
            end = data.get('end')
            wykladowca_id = session['user_id']
            sala = data.get('roomId')
            budynek = data.get('buildingId')
            
            try:
                
                czas_start = parser.parse(start)
                czas_koniec = parser.parse(end)

                zarezerwowano = self.rezerwacja_service.zarezerwuj_sala(tytul, czas_start, czas_koniec, wykladowca_id,sala)
                print(zarezerwowano)
                if zarezerwowano:
                    return jsonify({'status': 'success', 'message': 'Rezerwacja została dodana'})
                    
                else:
                    return jsonify({'status': 'error', 'message': 'Nie udało się zarezerwować sali'})
                

            except Exception as e:
                flash(f'Wystąpił błąd: {e}')
            
            return redirect(url_for('calendar'))
        else:
            flash('User not logged in')
            return redirect(url_for('login'))
    def get_buildings(self):
        buildings = self.sala_repository.znajdz_wszystkie_budynki()
        buildings_list = [{'id': budynek.budynek_id, 'nazwa': budynek.nazwa} for budynek in buildings]
        return jsonify(buildings_list)

    def get_available_rooms(self):
        budynek_id = int(request.args.get('budynek_id'))  # Cast to int if necessary
        czas_start = request.args.get('czas_start')
        czas_koniec = request.args.get('czas_koniec')

        available_rooms = self.sala_repository.sprawdz_dostepnosc(budynek_id, czas_start, czas_koniec)
        rooms_list = [{'numer_sali': sala.numer_sali, 'nazwa': sala.budynek.nazwa} for sala in available_rooms]

        return jsonify(rooms_list)
        


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
      
# class UserController:
#     def __init__(self, db):
#         self.uzytkownik_repository = UzytkownikRepository(db)
#         self.auth_service = AuthService(db)  
#         self.rezerwacja_service = RezerwacjaService(RezerwacjaRepository(session))

#     def login(self):
#         if request.method == 'POST':
#             username = request.form["login"]
#             password = request.form['haslo']
            
#             user = self.auth_service.zaloguj_przez_baze_danych(username, password)
#             if user:
#                 session['logged_in'] = True
#                 session['user_id'] = user.id  # Ustawienie identyfikatora użytkownika w sesji
#                 return redirect(url_for('calendar'))
#             else:
#                 flash('Invalid username or password')
#         return render_template("login.html")

#     def logoff(self):
#         flash('You have been logged off')
#         return redirect(url_for('login'))
    
#     def on_click_anuluj_rezerwacje(self, rezerwacja_id):
#         if 'logged_in' in session:
#             if self.rezerwacja_service.anuluj_rezerwacje(rezerwacja_id):
#                 flash('Rezerwacja anulowana')
#                 return redirect(url_for('calendar'))
#             else:
#                 flash('Rezerwacja nie istnieje')
#                 return redirect(url_for('calendar'))
#         else:
#             flash('User not logged in')
#             return redirect(url_for('login'))



#     def calendar(self):
#         if 'logged_in' in session and 'user_id' in session:
#             user_id = session['user_id']
#             rezerwacje = self.uzytkownik_repository.pobierz_rezerwacje_uzytkownika(user_id)
#             rezerwacje_dict = [rez.to_dict() for rez in rezerwacje]
#             return render_template("calendar.html", rezerwacje=rezerwacje_dict)
#         else:
#             flash('Please log in to view this page')
#             return redirect(url_for('login'))

        
#     def zarezerwuj_sala(self):
        
#         if 'logged_in' in session:
            
#             data = request.get_json()
#             tytul = data.get('title')
#             start = data.get('start')
#             end = data.get('end')
#             wykladowca_id = session['user_id']
            
#             try:
                
#                 czas_start = parser.parse(start)
#                 czas_koniec = parser.parse(end)

#                 zarezerwowano = self.rezerwacja_service.zarezerwuj_sala(tytul, czas_start, czas_koniec, wykladowca_id)
#                 print(zarezerwowano)
#                 if zarezerwowano:
#                     return jsonify({'status': 'success', 'message': 'Rezerwacja została dodana'})
                    
#                 else:
#                     return jsonify({'status': 'error', 'message': 'Nie udało się zarezerwować sali'})
                

#             except Exception as e:
#                 flash(f'Wystąpił błąd: {e}')
            
#             return redirect(url_for('calendar'))
#         else:
#             flash('User not logged in')
#             return redirect(url_for('login'))
        





    # def zarezerwuj_sala(self):
    #     if 'logged_in' in session:
    #         data = request.get_json()  # Pobierz dane w formacie JSON z żądania
    #         title = data.get('title')
    #         start = data.get('start')
    #         end = data.get('end')
    #         wykladowca_id = session['user_id']  # Używamy zalogowanego ID wykładowcy


    #         start_datetime = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
    #         end_datetime = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S%z')


    #         new_rezerwacja = Rezerwacja(
    #             title=title,
    #             czas_start=start_datetime,
    #             czas_koniec=end_datetime,
    #             wykladowca_id=wykladowca_id
    #         )


    #         db.session.add(new_rezerwacja)
    #         db.session.commit()

    #         return jsonify({'status': 'success', 'message': 'Rezerwacja została dodana'}), 200
    #     else:
    #         return jsonify({'status': 'error', 'message': 'Nie jesteś zalogowany'}), 401

    # def zarezerwuj_sala(self):
    #     if 'logged_in' in session:
    #         sala_id = request.form.get('sala_id')
    #         czas_start = request.form.get('czas_start')  # Pobieranie wartości z formularza
    #         czas_koniec = request.form.get('czas_koniec')

    #         # Sprawdzenie, czy wartości są dostępne
    #         if not all([sala_id, czas_start, czas_koniec]):
    #             flash('Wszystkie pola muszą być wypełnione.')
    #             return redirect(url_for('calendar'))

    #         try:
    #             # Konwersja czasów na obiekty datetime
    #             czas_start = datetime.strptime(czas_start, '%Y-%m-%dT%H:%M')
    #             czas_koniec = datetime.strptime(czas_koniec, '%Y-%m-%dT%H:%M')

    #             wykladowca_id = session['user_id']
    #             zarezerwowano = self.rezerwacja_service.zarezerwuj_sala(sala_id, czas_start, czas_koniec, wykladowca_id)
                
    #             if zarezerwowano:
    #                 flash('Sala została zarezerwowana')
    #             else:
    #                 flash('Nie udało się zarezerwować sali')
    #         except Exception as e:
    #             flash(f'Wystąpił błąd: {e}')
            
    #         return redirect(url_for('calendar'))
    #     else:
    #         flash('User not logged in')
    #         return redirect(url_for('login'))

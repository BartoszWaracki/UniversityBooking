from flask import Flask
from views import UserController
from extensions import db
from repos import UzytkownikRepository,RezerwacjaRepository
from Services import RezerwacjaService
from flask import session


# Klasa FlaskApp
class FlaskApp:
    def __init__(self, user_controller_class):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uniwersytet7.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.secret_key = 'your_secret_key'

        db.init_app(self.app)
        self.user_controller = user_controller_class(db)
        

        self.dodaj_regule_url()

    def dodaj_regule_url(self):
        self.app.add_url_rule('/', 'login', self.user_controller.login, methods=['GET', 'POST'])
        self.app.add_url_rule('/logoff', 'logoff', self.user_controller.logoff)
        self.app.add_url_rule('/calendar', 'calendar', self.user_controller.calendar)
        self.app.add_url_rule('/anuluj_rezerwacje/<int:rezerwacja_id>','anuluj_rezerwacje',self.user_controller.on_click_anuluj_rezerwacje,methods=['POST'])
        self.app.add_url_rule('/zarezerwuj_sala', 'zarezerwuj_sala', self.user_controller.zarezerwuj_sala, methods=['POST'])
        self.app.add_url_rule('/get_buildings', 'get_buildings', self.user_controller.get_buildings)
        self.app.add_url_rule('/get_available_rooms', 'get_available_rooms', self.user_controller.get_available_rooms)
        
        

    def uruchom(self):
        self.app.run(debug=True)


        
if __name__ == "__main__":
    app = FlaskApp(UserController)
    rezerwacja_repository = RezerwacjaRepository(db.session)  # Użycie db.session
    uzytkownik_repository = UzytkownikRepository(db)

    with app.app.app_context():
        db.create_all()
    rezerwacja_service = RezerwacjaService(rezerwacja_repository)
    user_controller = UserController(uzytkownik_repository)  # Przekazanie instancji repozytorium
    app.user_controller = user_controller  # Ustawienie kontrolera użytkownika w aplikacji Flask
    app.uruchom()

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

# # Klasa FlaskApp
# class FlaskApp:
#     def __init__(self, user_controller_class):
#         self.app = Flask(__name__)
#         self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uniwersytet7.db'
#         self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#         self.app.secret_key = 'your_secret_key'

#         db.init_app(self.app)
#         self.user_controller = user_controller_class(db)
        

#         self.dodaj_regule_url()

#     def dodaj_regule_url(self):
#         self.app.add_url_rule('/', 'login', self.user_controller.login, methods=['GET', 'POST'])
#         self.app.add_url_rule('/logoff', 'logoff', self.user_controller.logoff)
#         self.app.add_url_rule('/calendar', 'calendar', self.user_controller.calendar)
#         self.app.add_url_rule('/anuluj_rezerwacje/<int:rezerwacja_id>','anuluj_rezerwacje',self.user_controller.on_click_anuluj_rezerwacje,methods=['POST'])
#         self.app.add_url_rule('/zarezerwuj_sala', 'zarezerwuj_sala', self.user_controller.zarezerwuj_sala, methods=['POST'])
        
        

#     def uruchom(self):
#         self.app.run(debug=True)


        
# if __name__ == "__main__":
#     app = FlaskApp(UserController)
#     rezerwacja_repository = RezerwacjaRepository(db.session)  # Użycie db.session
#     uzytkownik_repository = UzytkownikRepository(db)

#     with app.app.app_context():
#         db.create_all()
#     rezerwacja_service = RezerwacjaService(rezerwacja_repository)
#     user_controller = UserController(uzytkownik_repository)  # Przekazanie instancji repozytorium
#     app.user_controller = user_controller  # Ustawienie kontrolera użytkownika w aplikacji Flask
#     app.uruchom()

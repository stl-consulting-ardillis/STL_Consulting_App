# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import LONGTEXT

db = SQLAlchemy()

# -------------------------------------------------------------------
# MODELO USER (MOVIDO DE ROUTES.PY PARA CÁ)
# -------------------------------------------------------------------
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relacionamento 1-para-1 com o Carometro
    # 'carometro' será o nome do atributo para acessar o perfil do usuário (ex: current_user.carometro)
    carometro = db.relationship('Carometro', back_populates='user', uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) # [cite: 108]

# -------------------------------------------------------------------
# NOVO MODELO PARA O CARÔMETRO
# -------------------------------------------------------------------
class Carometro(db.Model):
    __tablename__ = 'tbl_carometro'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    # Chave estrangeira para o usuário
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    # --- Campos do Formulário ---
    display_name = db.Column(db.String(100), nullable=False) # [cite: 19]
    current_role = db.Column(db.String(150), nullable=True)
    company = db.Column(db.String(150), nullable=True) # [cite: 20]
    start_year_company = db.Column(db.SmallInteger, nullable=True) # [cite: 21]
    city = db.Column(db.String(100), nullable=True)
    linkedin = db.Column(db.String(255), nullable=True) # [cite: 22]

    # Campos JSON
    # Usamos db.JSON para que o SQLAlchemy lide com a conversão lista/dicionário <-> string JSON
    experiences_json = db.Column(db.JSON, nullable=True)
    specialties_json = db.Column(db.JSON, nullable=True)
    achievements_json = db.Column(db.JSON, nullable=True)
    leadership_words_json = db.Column(db.JSON, nullable=True)
    values_json = db.Column(db.JSON, nullable=True) # [cite: 34]
    hobbies_json = db.Column(db.JSON, nullable=True) # [cite: 46]

    # Vida Pessoal
    marital_status = db.Column(db.Enum('Solteiro', 'Noivo', 'Casado'), nullable=True) # [cite: 38, 39, 40]
    spouse_name = db.Column(db.String(150), nullable=True) # [cite: 40]
    children_number = db.Column(db.SmallInteger, nullable=False, default=0) # [cite: 41]
    children_names_json = db.Column(db.JSON, nullable=True)
    pet_count = db.Column(db.SmallInteger, nullable=False, default=0) # [cite: 43]
    pet_species_json = db.Column(db.JSON, nullable=True) # [cite: 45]

    agree_terms = db.Column(db.Boolean, nullable=False, default=False) # [cite: 50]
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relacionamento reverso (para acessar o usuário a partir do perfil)
    user = db.relationship('User', back_populates='carometro')

    def __repr__(self):
        return f'<Carometro para {self.display_name}>'

# -------------------------------------------------------------------
# SEUS MODELOS EXISTENTES (Contact, Testimonial, Article)
# -------------------------------------------------------------------
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Contact {self.name}>'

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=True) # [cite: 120]
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Testimonial {self.name} from {self.company}>'

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=db.func.current_timestamp())
    tagline = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Article {self.title}>' # [cite: 121]

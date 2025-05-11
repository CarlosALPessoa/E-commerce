from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from models import db, User
from argon2 import PasswordHasher
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
ph = PasswordHasher()

app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/update_role", methods=["PUT"])
@jwt_required()
def update_role():
    current_user = get_jwt_identity()
    data = request.json

    if not data.get("username") or not data.get("role"):
        return jsonify({"message": "Username e novo role são obrigatórios"}), 400

    requester = User.query.filter_by(username=current_user).first()

    if requester.role != "admin":
        return jsonify({"message": "Apenas administradores podem alterar roles."}), 403

    user = User.query.filter_by(username=data["username"]).first()
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    user.role = data["role"]
    db.session.commit()

    return jsonify({"message": f"Role de {user.username} alterado para {user.role}"}), 200

@app.route("/register", methods=["POST"])
def register():
    data = request.json

    # Validações básicas
    if not data.get("username") or not data.get("password"):
        return jsonify({'message': 'Username e senha são obrigatórios.'}), 400

    # Verifica se o nome de usuário já existe
    user = User.query.filter_by(username=data["username"]).first()
    if user:
        return jsonify({'message': "Usuário já está cadastrado."}), 409

    # Cria o novo usuário com o username, senha e role (default "user")
    role = data.get("role", "user")  # Se não for fornecido, o valor padrão é "user"
    new_user = User(username=data["username"], role=role)
    new_user.set_pw(data["password"], ph)
    
    # Adiciona o novo usuário ao banco de dados
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário cadastrado com sucesso"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    # Busca o usuário no banco
    user = User.query.filter_by(username=data['username']).first()

    # Verifica a senha
    if user and user.check_pw(data["password"], ph):
        access_token = create_access_token(identity=user.username)

        # Verifica se o token está em bytes e converte
        if isinstance(access_token, bytes):
            access_token = access_token.decode('utf-8')

        return jsonify(access_token=access_token, user_id=user.id, username = user.username, role = user.role), 200

    return jsonify({"message": "Usuário e/ou senha inválidos"}), 401


@app.route("/userinfo", methods=["GET"])
@jwt_required()
def userinfo():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(username=user.username, role=user.role), 200
    return jsonify({"message": "Usuário não encontrado"}), 404

@app.route("/protected", methods=['GET'])
@jwt_required()
def protected():
    user = get_jwt_identity()
    return jsonify(logged_in_as = user), 200

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=3000)
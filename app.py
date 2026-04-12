from flask import Flask, request, render_template_string, make_response, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'  # Necesario para usar flash y manejar sesiones

# Base de datos simulada de usuarios (en un proyecto real usarías una base de datos)
usuarios = {
    'admin': {'password': generate_password_hash('1234'), 'role': 'admin'},  # Administrador predeterminado
    'user': {'password': generate_password_hash('password'), 'role': 'usuario'}  # Usuario normal
}

# Página principal
@app.route('/')
def home():
    # Verificar si la cookie "user" está presente
    user = request.cookies.get('user')
    role = request.cookies.get('role')  # Obtener el rol desde la cookie
    if user:
        if role == 'admin':
            return render_template_string('''
                <style>
                    /* Body y fondo */
                    body {
                        font-family: 'Roboto', sans-serif;
                        margin: 0;
                        padding: 0;
                        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
                        color: #fff;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }

                    /* Título */
                    h1 {
                        text-align: center;
                        font-size: 2.5rem;
                        margin-top: 20px;
                    }

                    /* Mensaje de bienvenida */
                    p {
                        text-align: center;
                        font-size: 1.2rem;
                        margin-top: 10px;
                    }

                    /* Botón de Cerrar sesión */
                    .btn-logout {
                        background-color: #f44336;
                        color: white;
                        border: none;
                        padding: 15px 30px;
                        font-size: 16px;
                        border-radius: 8px;
                        cursor: pointer;
                        transition: all 0.3s ease;
                        margin-top: 20px;
                        display: block;
                        text-decoration: none;
                    }

                    .btn-logout:hover {
                        background-color: #d32f2f;
                        transform: scale(1.05);
                    }
                </style>
                <h1>Bienvenido, {{ user }}!</h1>
                <p>¡Eres un administrador!<br><a href='/login' class="btn-logout">Cerrar sesión</a></p>
            ''', user=user)
        else:
            return render_template_string('''
                <style>
                    /* Body y fondo */
                    body {
                        font-family: 'Roboto', sans-serif;
                        margin: 0;
                        padding: 0;
                        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
                        color: #fff;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }

                    /* Título */
                    h1 {
                        text-align: center;
                        font-size: 2.5rem;
                        margin-top: 20px;
                    }

                    /* Botón de Cerrar sesión */
                    .btn-logout {
                        background-color: #f44336;
                        color: white;
                        border: none;
                        padding: 15px 30px;
                        font-size: 16px;
                        border-radius: 8px;
                        cursor: pointer;
                        transition: all 0.3s ease;
                        margin-top: 20px;
                        display: block;
                        text-decoration: none;
                    }

                    .btn-logout:hover {
                        background-color: #d32f2f;
                        transform: scale(1.05);
                    }
                </style>
                <h1>Hola, {{ user }}!</h1>
                <a href='/login' class="btn-logout">Cerrar sesión</a>
            ''', user=user)
    return render_template_string('''
        <style>
            /* Body y fondo */
            body {
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
                color: #fff;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            /* Título */
            h1 {
                text-align: center;
                font-size: 2.5rem;
                margin-top: 20px;
            }

            .btn-primary {
                background-color: #2575fc;
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 16px;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-top: 20px;
                display: block;
                text-decoration: none;
            }

            .btn-primary:hover {
                background-color: #6a11cb;
                transform: scale(1.05);
            }
        </style>
        <h1 class="welcome-title">Bienvenido, visitante!</h1>
        <a href="/login" class="btn btn-primary">Iniciar sesión</a>
    ''')

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verificar si el usuario existe y si la contraseña es correcta
        if username in usuarios and check_password_hash(usuarios[username]['password'], password):
            role = usuarios[username]['role']
            resp = make_response(f'Hola, {username}! Has iniciado sesión.<br><a href="/">Ir al inicio</a>')
            resp.set_cookie('user', username)  # Establecer la cookie 'user'
            resp.set_cookie('role', role)  # Establecer la cookie 'role'
            return resp
        else:
            flash('Usuario o contraseña incorrectos', 'error')  # Mostrar mensaje de error

    return render_template_string('''
        <style>
            /* Aquí va el código CSS */
            body {
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
                color: #000;
            }
            h1 {
                text-align: center;
                color: #000;
            }
            .form-container {
                width: 100%;
                max-width: 400px;
                margin: 50px auto;
                background-color: #fff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            input[type="text"], input[type="password"], input[type="submit"] {
                width: 100%;
                padding: 10px;
                margin: 15px 0;
                border-radius: 8px;
                border: 1px solid #ccc;
                font-size: 16px;
            }
            .btn-primary {
                background-color: #2575fc;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.3s ease;
            }
        </style>
        <div class="form-container">
            <h2>Iniciar sesión</h2>
            <form method="post">
                <label>Nombre de usuario:</label>
                <input type="text" name="username" required><br>
                <label>Contraseña:</label>
                <input type="password" name="password" required><br>
                <input type="submit" class="btn btn-primary" value="Iniciar sesión">
            </form>
            <br>
            <a href="/register" class="btn btn-secondary">Crear una nueva cuenta</a>  <!-- Enlace al registro -->
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    <ul>
                        {% for category, message in messages %}
                            <li>{{ message }}</li>
                        {% endfor %}
                    </ul>
                {% endif %}
            {% endwith %}
        </div>
    ''')

# Página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validar que las contraseñas coinciden
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('register'))

        # Verificar si el usuario ya existe
        if username in usuarios:
            flash('El nombre de usuario ya está registrado', 'error')
            return redirect(url_for('register'))

        # Asignar rol por defecto 'usuario', pero con Burp Suite se puede cambiar a 'admin'
        role = 'usuario'

        # Guardar el nuevo usuario (en un proyecto real, se guardaría en una base de datos)
        usuarios[username] = {'password': generate_password_hash(password), 'role': role}
        
        # Crear la cookie con el rol y usuario
        resp = make_response(f'Usuario {username} registrado exitosamente.<br><a href="/">Ir al inicio</a>')
        resp.set_cookie('user', username)  # Guardar el nombre de usuario en la cookie
        resp.set_cookie('role', role)  # Guardar el rol en la cookie
        
        flash('Usuario registrado exitosamente. Ahora puedes iniciar sesión.', 'success')
        return resp

    return render_template_string('''
        <style>
            /* Aquí va el código CSS */
            body {
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
                color: #000;
            }
            h2 {
                text-align: center;
                color: #000;
            }
            .form-container {
                width: 100%;
                max-width: 400px;
                margin: 50px auto;
                background-color: #fff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            input[type="text"], input[type="password"], input[type="submit"] {
                width: 100%;
                padding: 10px;
                margin: 15px 0;
                border-radius: 8px;
                border: 1px solid #ccc;
                font-size: 16px;
            }
            .btn-primary {
                background-color: #2575fc;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.3s ease;
            }
        </style>
        <div class="form-container">
            <h2>Registrar una nueva cuenta</h2>
            <form method="post">
                <label>Nombre de usuario:</label>
                <input type="text" name="username" required><br>
                <label>Contraseña:</label>
                <input type="password" name="password" required><br>
                <label>Confirmar Contraseña:</label>
                <input type="password" name="confirm_password" required><br>
                <input type="submit" class="btn btn-primary" value="Registrar cuenta">
            </form>
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    <ul>
                        {% for category, message in messages %}
                            <li>{{ message }}</li>
                        {% endfor %}
                    </ul>
                {% endif %}
            {% endwith %}
        </div>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
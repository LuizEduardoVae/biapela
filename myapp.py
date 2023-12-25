from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'

# Dados de exemplo (poderiam ser armazenados em um banco de dados)
users = {'user1': {'password': 'pass1', 'lists': {'Lista1': ['Item1', 'Item2']}}}

# Função auxiliar para verificar a autenticação do usuário
def is_authenticated(username, password):
    return users.get(username) and users[username]['password'] == password


# Rotas

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if is_authenticated(username, password):
            return redirect(url_for('dashboard', username=username))
        else:
            return render_template('login.html', error='Credenciais inválidas')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users:
            users[username] = {'password': password, 'lists': {}}
            return redirect(url_for('dashboard', username=username))
        else:
            return render_template('signup.html', error='Nome de usuário já existe')

    return render_template('signup.html')

@app.route('/dashboard/<username>')
def dashboard(username):
    user_data = users.get(username)
    if user_data:
        user_lists = user_data['lists']
        return render_template('dashboard.html', username=username, lists=user_lists)

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/create_list/<username>', methods=['GET', 'POST'])
def create_list(username):
    user_data = users.get(username)
    if user_data:
        if request.method == 'POST':
            list_name = request.form['list_name']
            user_data['lists'][list_name] = []
            return redirect(url_for('dashboard', username=username))

        return render_template('create_list.html', username=username)

    return redirect(url_for('index'))

@app.route('/add_item/<username>/<list_name>', methods=['GET', 'POST'])
def add_item(username, list_name):
    user_data = users.get(username)
    if user_data:
        if request.method == 'POST':
            item_name = request.form['item_name']
            user_data['lists'][list_name].append(item_name)
            return redirect(url_for('list_detail', username=username, list_name=list_name))

        return render_template('add_item.html', username=username, list_name=list_name)

    return redirect(url_for('index'))

@app.route('/remove_item/<username>/<list_name>/<item_name>')
def remove_item(username, list_name, item_name):
    user_data = users.get(username)
    if user_data:
        if item_name in user_data['lists'][list_name]:
            user_data['lists'][list_name].remove(item_name)

        return redirect(url_for('list_detail', username=username, list_name=list_name))

    return redirect(url_for('index'))

@app.route('/list_detail/<username>/<list_name>')
def list_detail(username, list_name):
    user_data = users.get(username)
    if user_data:
        items = user_data['lists'].get(list_name, [])
        return render_template('list_detail.html', username=username, list_name=list_name, items=items)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

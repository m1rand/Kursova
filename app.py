from flask import Flask, render_template, request, redirect, url_for
from model import DatabaseSingleton
import pypyodbc

app = Flask(__name__)
database_singleton = DatabaseSingleton()

@app.route('/')
def index():
    return render_template('index.html', table_names=database_singleton.TABLE_NAMES)

@app.route('/table', methods=['POST'])
def show_table():
    selected_table = request.form.get('table')
    columns, data = database_singleton.get_table_data(selected_table)
    return render_template('table.html', table_name=selected_table, columns=columns, data=data)

@app.route('/client', methods=['POST'])
def show_client_by_id():
    client_id = request.form.get('clientId')
    conn = pypyodbc.connect(f"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={database_singleton.DATABASE_PATH}")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM Клієнт WHERE Клієнт.ID = ?;", (client_id,))
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()

    conn.close()

    if not data:
        return render_template('index.html', table_names=database_singleton.TABLE_NAMES, client_not_found=True)

    return render_template('table.html', table_name="Клієнт", columns=columns, data=data)

if __name__ == '__main__':
    app.run(debug=True)


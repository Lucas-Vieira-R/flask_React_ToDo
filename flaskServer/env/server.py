import psycopg2
from flask import Flask, request,jsonify

def connectToDb():
    conn = psycopg2.connect(
        host="localhost",
        database="blog",
        user="blogadmin",
        password="admin")
    return conn

app = Flask(__name__)

# API para criar uma nova tarefa
@app.route('/new_todo', methods=['POST'])
def new_todo():
    # acesso a requisição para acessar os valores
    req = request.get_json()
    # conecto ao postgresql db
    conn = connectToDb()
    cursor = conn.cursor()
    # realizo a inserção
    cursor.execute("INSERT INTO todo(title,is_done,comments) VALUES('%s',false,'%s');"%(req['title'],req['comments']))
    conn.commit()
    # corto a conexao
    cursor.close()
    conn.close()
    return jsonify({f"{req['title']}": "inserted!"}),200

# API para retornar todas as tarefas
@app.route('/get_all_todos',methods = ['GET'])
def get_todos():
    conn = connectToDb()
    cursos = conn.cursor()
    cursos.execute("SELECT * FROM todo;")
    todos = cursos.fetchall()
    
    return jsonify(todos) 

# retorna um todo específico por id
@app.route('/todo/<id>', methods=['GET'])
def get_todo(id):
    conn = connectToDb()
    cursos = conn.cursor()
    cursos.execute("SELECT * FROM todo WHERE id = %i;"%(id))
    todos = cursos.fetchall() 
    return jsonify(todos)

# API para deletar todo através de id
@app.route('/delete_todo/<id>',methods = ["DELETE"])
def delete_todo(id):
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todo WHERE id=%s;"%(id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "the todo with the id %s was deleted"%(id)})

# API para atualizar o estado do todo
@app.route('/toggle_state_todo/<id>', methods= ['PATCH'])
def toggle_state_todo(id):
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todo WHERE id=%s;"%(id))
    todo = cursor.fetchone()
    if todo is None:
        return jsonify({"message":"todo not found"})
    if not todo[2]:
        cursor.execute("UPDATE todo SET is_done = true WHERE id= %s"%(id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message":"the todo with the id %s is done"%(id)})
    else:
        cursor.execute("UPDATE todo SET is_done = false WHERE id= %s"%(id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message":"the todo with the id %s is not done"%(id)})

# atualiza as informações de determinado todo
@app.route('/update_todo/<id>', methods=["POST"])
def update_todo(id):
    req = request.get_json()
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todo WHERE id=%s;"%(id))
    todo = cursor.fetchone()
    if todo is None:
        return jsonify({"message":"todo not found"})
    cursor.execute("UPDATE todo SET title = '%s', comments = '%s' WHERE id= %s"%(req['title'],req['comments'],id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message":"the todo with the id %s was updated"%(id)})


if __name__ == "__main__":
    app.run(debug=True)
# database = blog
#user = blogadmin
#password = admin
# CREATE TABLE todo(id SERIAL PRIMARY KEY, title VARCHAR(30), is_done boolean, comments VARCHAR(80));
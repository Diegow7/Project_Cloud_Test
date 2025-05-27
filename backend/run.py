# backend/run.py

from app import crear_app

app = crear_app()

if __name__ == '__main__':
    #Redireccionando al backend de AWS, evitando el local host
    #app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)
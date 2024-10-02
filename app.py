# É possível importar um txt com todas as bibliotecas já setadas. Para tal use o pip install  r arquivo.txt
from flask import Flask # Importar a classe Flask da biblioteca Flask

app = Flask(__name__) # Instancia o Aplicativo Flask

# Definir uma rota raíz (página inicial) e função que será executada ao requisitar-se essa rota
@app.route('/') # Por padrão a rota raíz é sempre / e as rotas vem chamandas com base na váriavel difinida como instância, nesse caso app
def index(): # Cria a função a ser chamada nessa rota
    return 'Hello World'



# Definir a Depuração do seu sistema
# É sempre importante checar esse arquivo está sendo executado diretamente
if __name__ == "__main__":
    app.run(debug=True) # Executa o aplicativo Flask com depuração ativada 
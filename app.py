# É possível importar um txt com todas as bibliotecas já setadas. Para tal use o pip install r arquivo.txt
from flask import Flask, request, jsonify # Importar as classes da biblioteca Flask que serão usadas
from flask_sqlalchemy import SQLAlchemy # Importa a classe da biblioteca ORM para conversar com o BD

app = Flask(__name__) # Instancia o Aplicativo Flask
# Estamos considerando criar um banco em SQLite - que seria um banco em texto, apenas para faciltar o projeto
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db' # Configura o caminho onde se encotra o Banco de Dados

db = SQLAlchemy(app) # Mapeia a conexão com o banco para uma variável

# MODELAGEM DO BANCO DE DADOS
# Produto (id, name, price, description)
class Produto(db.Model): # Cria uma classe para definir o modelo da tabela de produto
    id = db.Column(db.Integer, primary_key=True) # Definir o primeiro campo da tabela produto
    name = db.Column(db.String(100), nullable=False) # Definir o segundo campo, nullable=False significa que não pode ser Null
    price = db.Column(db.Float, nullable=False) # Definir o terceiro campo
    description = db.Column(db.Text, nullable=True) # Definir o quarto, Text é um tipo de campo que não tem um limite de caracteres
    # Agora o que é importante: Para criar a tabela abre o terminar sem executar e digita o comando flask shell. Isso vai executar
    # terminar específico do flask. Aí informe o comando db.create_all() e ENTER. Depois db.session.commit() para salvar.
    # Para sair do flask shell use o comando exit(). Tendo dado certo na aparecerá a nova base de dados

# Definir a Rota para Adicionar produtos
@app.route('/api/products/add', methods=["POST"]) 
def add_products():
    data = request.json # variável para receber os dados vindo do API via json
    # Vamos testar se os campos obrigatórios estão chegando, até para não gerar um erro no banco
    if 'name' in data and 'price' in data: # Se campo nome em data e a price em data estão não nulls  
        produto = Produto(name=data["name"],price=data["price"],description=data.get("description","")) # Instancia a classe Produto - que é o meu banco de dados...
        # ... detalhe para que se eu usar o get posso definir um valor padrão para o caso de vir vazio, o que é importante já que o campo descrição pode ser Null
        db.session.add(produto) # Comando para adiocionar um dado no banco
        db.session.commit() # Salvar os dados no banco
        return jsonify({"message":"Produto Cadastrado com Sucesso."}), 200 # O código padrão de sucesso é 200
    # Caso alguma info obrigatória não venha, montamos um json de resposta e um código do erro. Para isso usamos a classe flask jsonify
    return jsonify({"message":"Dados de Produto Inválidos."}), 400 # O código padrão de erro é 400

# DEFINIR UMA ROTA PARA DELETAR PRODUTOS
@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"]) # No delete vamos precisar receber um parametro e isso é feito com <> o tipo da variável e o nome dela
def delete_product(product_id):
    # Recuperar  o produto da base de dados
    produto = Produto.query.get(product_id)
    # Checar se ele existe
    if produto:
        # Se ele existe, apagar da base
        db.session.delete(produto)
        db.session.commit()
        return jsonify({"message":"Produto Deletado com Sucesso."}), 200
    # Se não existe, retornar 404 - não encontrado
    return jsonify({"message":"Produto não encontrado."}), 404
    
    


# Definir uma rota raíz (página inicial) e função que será executada ao requisitar-se essa rota
@app.route('/') # Por padrão a rota raíz é sempre / e as rotas vem chamandas com base na váriavel difinida como instância, nesse caso app
def index(): # Cria a função a ser chamada nessa rota
    return 'Hello World'



# Definir a Depuração do seu sistema
# É sempre importante checar esse arquivo está sendo executado diretamente
if __name__ == "__main__":
    app.run(debug=True) # Executa o aplicativo Flask com depuração ativada 
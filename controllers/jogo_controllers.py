from models.jogo_models import Jogo  # Importa o modelo Jogo
from db import db  # Importa a conexão com o banco de dados
import json
from flask import make_response, request

# Função para obter todos os jogos
def get_jogo():
    jogos = Jogo.query.all()  # Busca todos os jogos no banco de dados
    response = make_response(
        json.dumps({
            'mensagem': 'Lista de jogos.',
            'dados': [jogo.json() for jogo in jogos]  # Converte os objetos de jogo para JSON
        }, ensure_ascii=False, sort_keys=False)  # Mantém caracteres especiais corretamente formatados
    )
    response.headers['Content-Type'] = 'application/json'  # Define o tipo de conteúdo como JSON
    return response

# Função para obter um jogo específico por ID
def get_jogo_by_id(jogo_id):
    jogo = Jogo.query.get(jogo_id)  # Busca o jogo pelo ID

    if jogo:  # Verifica se o jogo foi encontrado
        response = make_response(
            json.dumps({
                'mensagem': 'Jogo encontrado.',
                'dados': jogo.json()  # Converte os dados do jogo para formato JSON
            }, ensure_ascii=False, sort_keys=False)
        )
        response.headers['Content-Type'] = 'application/json'  # Garante que o tipo da resposta seja JSON
        return response
    else:
        # Se o jogo não for encontrado, retorna erro com código 404
        response = make_response(
            json.dumps({'mensagem': 'Jogo não encontrado.', 'dados': {}}, ensure_ascii=False),
            404  # Código HTTP 404 para "Não encontrado"
        )
        response.headers['Content-Type'] = 'application/json'  # Define que a resposta é em JSON
        return response

# Função para criar um novo jogo
def create_jogo(jogo_data):
    # Valida se todos os campos obrigatórios foram fornecidos
    if not all(key in jogo_data for key in ['titulo', 'genero', 'desenvolvedor', 'plataforma']):
        response = make_response(
            json.dumps({'mensagem': 'Dados inválidos. Título, gênero, desenvolvedor e plataforma são obrigatórios.'}, ensure_ascii=False),
            400  # Código HTTP 400 para requisição inválida
        )
        response.headers['Content-Type'] = 'application/json'  # Garante que a resposta seja em JSON
        return response
    
    # Se os dados forem válidos, cria o novo jogo
    novo_jogo = Jogo(
        titulo=jogo_data['titulo'],
        genero=jogo_data['genero'],
        desenvolvedor=jogo_data['desevolvedor'],
        plataforma=jogo_data['plataforma']
    )
    
    db.session.add(novo_jogo)  # Adiciona o novo jogo ao banco de dados
    db.session.commit()  # Confirma a transação no banco

    # Resposta de sucesso com os dados do novo jogo
    response = make_response(
        json.dumps({
            'mensagem': 'Jogo cadastrado com sucesso.',
            'jogo': novo_jogo.json()  # Retorna os dados do jogo cadastrado
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'  # Define que a resposta é em JSON
    return response

# Função para atualizar um jogo por ID
def update_jogo(jogo_id, jogo_data):
    jogo = Jogo.query.get(jogo_id)  # Buscar o jogo pelo ID

    if not jogo:  # Se o jogo não for encontrado, retorna erro
        response = make_response(
            json.dumps({'mensagem': 'Jogo não encontrado.'}, ensure_ascii=False),
            404 # Código HTTP 404 para "Não encontrado"
        )
        response.headers['Content-Type'] = 'application/json'   #Garante que a resposta seja em json
        return response
    
    # Valida se todos os campos obrigatórios foram fornecidos
    if not all(key in jogo_data for key in ['titulo, genero, desevolvedor, plataforma']):
        response = make_response(
            json.dumps({'mensagem': 'Dados inválidos. Título, gênero, desenvolvedor e plataforma são obrigatórios.'}, ensure_ascii=False),
            400 # Código HTTP 400 para requisição inválida
        )
        response.headers['Content-Type'] = 'application/json'  # Define que a resposta é em JSON
        return response
        
    # Atualiza os dados do jogo
    jogo.titulo = jogo_data['titulo']
    jogo.genero = jogo_data['genero']
    jogo.desenvolvedor = jogo_data['desenvolvedor']
    jogo.plataforma = jogo_data['plataforma']

    db.session.commit()   # Confirma a atualização no banco de dados

    # Retorna a resposta com os dados do jogo atualizado
    response = make_response(
        json.dumps({
            'mensagem': 'Jogo atualizado com sucesso.',
            'jogo': jogo.json()
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'   # Define que a resposta é em JSON
    return response

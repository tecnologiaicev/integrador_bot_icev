import pandas as pd 
from app.daos.quiz_dao import buscar_select_banco
from flask import Flask, jsonify
from app.utils.nlp import limparHtml
import os
from dotenv import load_dotenv 

# Carrega variáveis de ambiente
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


def buscar_quiz(id, data_inicio, data_fim,username):
    """
    Função responsável por buscar os dados do quiz no banco de dados, tratar as informações 
    e retornar os dados formatados como JSON.

    Parâmetros:
    - id (int): ID do quiz.
    - data_inicio (str): Data de início do filtro.
    - data_fim (str): Data de fim do filtro.

    Retorno:
    - JSON contendo os dados organizados nos DataFrames (Disciplina, Questões, Pessoas e Respostas).
    """

    # 🔹 Busca os dados no banco de dados
    quiz_dict = buscar_select_banco(id, data_inicio, data_fim,username)
    # 🔹 Converte os dados para um DataFrame do Pandas
    df = pd.DataFrame(quiz_dict)

    # 🔹 Ajustes no formato do texto (remoção de quebras de linha e limpeza de HTML)
    if df.empty:
    # DataFrame vazio, retorne algo ou trate o caso
        return jsonify({"message": "Nenhum dado encontrado no período informado."}), 404

    # Só continua se houver dados
    df['enunciado'] = df['enunciado'].str.replace(r'[\r\n]', ' ', regex=True)
    df['alternativa_correta'] = df['alternativa_correta'].str.replace(r'[\r\n]', ' ', regex=True)  
    df['respostas_concatenada'] = df['respostas_concatenada'].str.replace(r'[\r\n]', ' ', regex=True)  

    # Aplicação da limpeza de HTML nos textos das questões e respostas
    df['enunciado'] = df['enunciado'].apply(limparHtml)
    df['respostas_concatenada'] = df['respostas_concatenada'].apply(limparHtml)

    # 🔹 Conversão de colunas numéricas para float e arredondamento
    df['iscerta'] = df['iscerta'].astype(float).round(1)

    # 🔹 Criação de diferentes DataFrames organizando os dados
    # DataFrame contendo informações da disciplina
    df_Disciplina = df[['nomeDisciplina', 'idDisciplina']].drop_duplicates()

    # DataFrame contendo informações dos estudantes
    df_Pessoa = df[['estudante', 'idUser', 'email']].drop_duplicates()

    # DataFrame contendo informações das questões
    df_Questoes = df[['idQuestao', 'idPergunta', 'enunciado', 'alternativa_correta', 'respostas_concatenada', 'hora_realizada']]
    df_Questoes = df_Questoes.sort_values(by='hora_realizada', ascending=False)
    df_Questoes = df_Questoes.drop_duplicates(subset=['idQuestao', 'enunciado', 'alternativa_correta', 'respostas_concatenada'], keep='first')

    # DataFrame contendo as respostas dos usuários
    df_Respostas = df[['idUser', 'idQuestao', 'idPergunta', 'iscerta']]

    # 🔹 Retorna os dados em formato JSON
    return jsonify(
        df_Disciplina.to_dict(orient='records'),
        df_Questoes.to_dict(orient='records'), 
        df_Pessoa.to_dict(orient='records'),
        df_Respostas.to_dict(orient='records')
    )


def verify_token(token):
    """
    Função para verificar se o token passado é válido.

    Parâmetro:
    - token (str): Token a ser verificado.

    Retorno:
    - (bool) True se o token for válido, False caso contrário.
    """
    return token == SECRET_KEY

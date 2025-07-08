import pandas as pd 
from app.daos.quiz_dao import buscar_select_banco
from flask import Flask, jsonify
from app.utils.nlp import limparHtml
import os
from dotenv import load_dotenv 

# Carrega variáveis de ambiente
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def buscar_quiz(id, data_inicio, data_fim, username):
    # Busca os dados do quiz e retorna no formato estruturado:
    # {
    #     "disciplina": {...},
    #     "questoes": [...]
    # }
    quiz_dict = buscar_select_banco(id, data_inicio, data_fim, username)
    df = pd.DataFrame(quiz_dict)

    #  Verifica se há dados
    if df.empty:
        return jsonify({"message": "Nenhum dado encontrado no período informado."}), 404
    
    # Agrupa e concatena respostas (answer) para cada combinação relevante
    df = (
        df.groupby([
            'nomeDisciplina', 'idDisciplina', 'quiz_name', 'estudante', 'enunciado',
            'alternativa_correta', 'resposta_sumario', 'hora_realizada', 'iscerta',
            'idUser', 'email', 'idQuestao', 'timemodified', 'idPergunta', 'sequencenumber'
        ])
        .agg({
            'respostas_concatenada': lambda x: '##@@##'.join(x.dropna().astype(str))
        })
        .reset_index()
    )

    # Ordena por estudante
    df = df.sort_values(by='estudante')

    #  Limpeza de textos e HTML
    df['enunciado'] = df['enunciado'].str.replace(r'[\r\n]', ' ', regex=True).apply(limparHtml)
    df['alternativa_correta'] = df['alternativa_correta'].str.replace(r'[\r\n]', ' ', regex=True)
    df['respostas_concatenada'] = df['respostas_concatenada'].str.replace(r'[\r\n]', ' ', regex=True).apply(limparHtml)

    #  Converte isCerta para booleano
    df['iscerta'] = df['iscerta'].astype(int).apply(lambda x: True if x == 1 else False)

    #  Pega os dados da disciplina (apenas uma)
    disciplina = df[['idDisciplina', 'nomeDisciplina']].iloc[0].to_dict()
    df = df.sort_values(by='estudante')

    # Formata hora_realizada para o formato desejado
    df['hora_realizada'] = pd.to_datetime(df['hora_realizada']).dt.strftime('%Y-%m-%d %H:%M:%S')

    
    #  Monta a lista de questões com estrutura de resposta_aluno
    questoes = []
    for _, row in df.iterrows():
        questao = {
            "alternativa_correta": row["alternativa_correta"],
            "enunciado": row["enunciado"],
            "hora_realizada": row["hora_realizada"],
            "idPergunta": row["idPergunta"],
            "idQuestao": row["idQuestao"],
            "respostas_concatenada": [res.strip() for res in row["respostas_concatenada"].split("##@@##")],             
            "resposta_aluno": {
                "idPergunta": row["idPergunta"],
                "idQuestao": row["idQuestao"],
                "idUser": row["idUser"],
                "iscerta": row["iscerta"]
            }
        }
        questoes.append(questao)

    #  Monta o dicionário final
    resultado = {
        "disciplina": disciplina,
        "questoes": questoes
    }

    return jsonify(resultado)


def verify_token(token):
    """
    Função para verificar se o token passado é válido.

    Parâmetro:
    - token (str): Token a ser verificado.

    Retorno:
    - (bool) True se o token for válido, False caso contrário.
    """
    return token == SECRET_KEY

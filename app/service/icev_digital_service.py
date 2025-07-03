import pandas as pd 
from app.daos.quiz_dao import buscar_select_banco
from flask import Flask, jsonify
from app.utils.nlp import limparHtml
import os
from dotenv import load_dotenv 

# Carrega variáveis de ambiente
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


from flask import jsonify
import pandas as pd

def buscar_quiz(id, data_inicio, data_fim, username):
    """
    Busca os dados do quiz e retorna no formato estruturado:
    {
        "disciplina": {...},
        "questoes": [...]
    }
    """
    # 🔹 Busca os dados no banco de dados
    quiz_dict = buscar_select_banco(id, data_inicio, data_fim, username)
    df = pd.DataFrame(quiz_dict)

    # 🔹 Verifica se há dados
    if df.empty:
        return jsonify({"message": "Nenhum dado encontrado no período informado."}), 404

    # 🔹 Limpeza de textos e HTML
    df['enunciado'] = df['enunciado'].str.replace(r'[\r\n]', ' ', regex=True).apply(limparHtml)
    df['alternativa_correta'] = df['alternativa_correta'].str.replace(r'[\r\n]', ' ', regex=True)
    df['respostas_concatenada'] = df['respostas_concatenada'].str.replace(r'[\r\n]', ' ', regex=True).apply(limparHtml)

    # 🔹 Converte isCerta para booleano
    df['iscerta'] = df['iscerta'].astype(int).apply(lambda x: True if x == 1 else False)

    # 🔹 Pega os dados da disciplina (apenas uma)
    disciplina = df[['idDisciplina', 'nomeDisciplina']].drop_duplicates().iloc[0].to_dict()
    
    # 🔹 Monta a lista de questões com estrutura de resposta_aluno
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

    # 🔹 Monta o dicionário final
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
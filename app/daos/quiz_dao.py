from app.models.quiz import Quiz
from extensions import db
# Importação do banco de dados (para evitar dependências circulares)
from app import db
import sqlalchemy as sa
from sqlalchemy import text

def buscar_select_banco(id_disc, data_inicio, data_fim, username):  
    # Busca os dados do quiz no banco de dados filtrando por ID da disciplina e período especificado.

    # Parâmetros:
    # - id_disc (int): ID da disciplina.
    # - data_inicio (str): Data inicial do período de busca (YYYY-MM-DD).
    # - data_fim (str): Data final do período de busca (YYYY-MM-DD).
    # Retorno:
    # - (list[dict]) Lista de dicionários contendo os dados do quiz.

    #  Query SQL para buscar os dados do quiz
    query = text("""
        SELECT 
            ic.fullname,
            ic.id AS curso_id,
            iq.name AS quiz_nome,
            CONCAT(iu.firstname, ' ', iu.lastname) AS estudante,
            iq2.questiontext,
            iqa2.rightanswer,
            iqa2.responsesummary,
            iqa3.answer,
            FROM_UNIXTIME(iqas.timecreated) AS hora_realizada,
            iqas.fraction,
            iqas.sequencenumber,
            iqa.userid,
            iu.email,
            iqa2.questionid,
            iqa2.timemodified,
            icm.id AS id_modulo
        FROM icev_course ic
        JOIN icev_course_modules icm ON icm.course = ic.id
        JOIN icev_quiz iq ON icm.instance = iq.id
        JOIN icev_quiz_attempts iqa ON iqa.quiz = iq.id
        JOIN icev_user iu ON iu.id = iqa.userid
        JOIN icev_question_usages iqu ON iqu.id = iqa.uniqueid
        JOIN icev_question_attempts iqa2 ON iqa2.questionusageid = iqu.id
        JOIN icev_question iq2 ON iq2.id = iqa2.questionid
        JOIN icev_question_answers iqa3 ON iqa3.question = iq2.id
        JOIN icev_question_attempt_steps iqas ON iqas.questionattemptid = iqa2.id
        WHERE ic.id = :id
            AND iqas.sequencenumber in (2)
            AND iu.username = :username
            AND iqas.timecreated BETWEEN UNIX_TIMESTAMP (:data_inicio) AND UNIX_TIMESTAMP (:data_fim) + 86399
        ORDER BY estudante
    """)

    #  Executa a query no banco de dados
    result = db.session.execute(query, {
        'id': id_disc,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'username':  username
    })

    #  Obtém todos os resultados
    users = result.fetchall()

    #  Formata os dados retornados em uma lista de dicionários
    users_data = [
        {
            'nomeDisciplina': user[0],
            'idDisciplina': user[1],
            'quiz_name': user[2],
            'estudante': user[3],
            'enunciado': user[4],
            'alternativa_correta': user[5],
            'resposta_sumario': user[6],
            'respostas_concatenada': user[7],
            'hora_realizada': user[8],
            'iscerta': -1 if user[9] is None else user[9],
            'sequencenumber': user[10],
            'idUser': user[11],
            'email': user[12],
            'idQuestao': user[13],
            'timemodified': user[14],
            'idPergunta': user[15]
        }
        for user in users
    ]

    return users_data

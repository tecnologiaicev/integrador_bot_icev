from app.models.quiz import Quiz
from extensions import db
import sqlalchemy as sa
from sqlalchemy import text

def buscar_select_banco(id_disc, data_inicio, data_fim, username):
    """
    Busca os dados do quiz no banco de dados filtrando por ID da disciplina e período especificado.

    Parâmetros:
    - id_disc (int): ID da disciplina.
    - data_inicio (str): Data inicial do período de busca (YYYY-MM-DD).
    - data_fim (str): Data final do período de busca (YYYY-MM-DD).

    Retorno:
    - (list[dict]) Lista de dicionários contendo os dados do quiz.
    """

    # Importação do banco de dados (para evitar dependências circulares)
    from app import db

    #  Query SQL para buscar os dados do quiz
    query = text("""
        SELECT 
            ic.fullname,
            ic.id,
            iq.name,
            CONCAT(iu.firstname, ' ', iu.lastname) AS Estudante,
            iq2.questiontext,
            iqa2.rightanswer,
            iqa2.responsesummary,
            GROUP_CONCAT(iqa3.answer SEPARATOR '##@@##') AS RespostasConcat,
            MAX(COALESCE(FROM_UNIXTIME(iqas.timecreated), 1)) AS HoraRealizada,
            CASE 
                WHEN IFNULL(iqas.fraction, '') = '' THEN -1
                ELSE iqas.fraction 
            END AS CertoOuErrado,
            CASE
                WHEN IFNULL(iqa2.responsesummary, '') = '' AND iqas.sequencenumber = 1 THEN 'Não respondido'
                ELSE iqa2.responsesummary
            END AS RespostaAluno, 
            icm.id,
            iqa.userid,
            iu.email,
            iqas.sequencenumber,
            iqa2.questionid,
            CASE 
                WHEN iqas.sequencenumber = 2 AND iqa2.responsesummary IS NULL THEN 1
                WHEN iqas.sequencenumber = 1 AND iqa2.responsesummary IS NOT NULL THEN 1
                WHEN iqas.sequencenumber = 0 THEN 1
                ELSE 2
            END AS StatusAtivo
        FROM icev_course ic 
        JOIN icev_course_modules icm ON icm.course = ic.id 
        JOIN icev_quiz iq ON icm.instance = iq.id 
        JOIN icev_quiz_sections iqs ON iqs.quizid = iq.id 
        JOIN icev_quiz_attempts iqa ON iqa.quiz = iq.id 
        JOIN icev_user iu ON iu.id = iqa.userid
        JOIN icev_question_usages iqu ON iqu.id = iqa.uniqueid
        JOIN icev_question_attempts iqa2 ON iqa2.questionusageid = iqu.id
        JOIN icev_question iq2 ON iq2.id = iqa2.questionid 
        JOIN icev_question_answers iqa3 ON iqa3.question = iq2.id 
        JOIN icev_question_attempt_steps iqas ON iqas.questionattemptid = iqa2.id
        WHERE ic.id = :id
            AND iu.username = :username  # Busca pelo cpf do estudante. 
            AND DATE(FROM_UNIXTIME(iqas.timecreated)) BETWEEN :data_inicio AND :data_fim
        GROUP BY ic.fullname,
            ic.id,
            iq.name,
            iu.firstname,
            iu.lastname,
            iq2.questiontext,
            iqa2.rightanswer,
            iqa2.responsesummary,
            iqas.timecreated,
            iqas.sequencenumber,
            iqas.fraction, 
            iqa2.timemodified,
            icm.id,
            iqa.userid,
            iu.email,
            iqa2.questionid
        HAVING StatusAtivo = 2
        ORDER BY Estudante;
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
            'nomeDisciplina': user[0],   # Nome da disciplina
            'idDisciplina': user[1],     # ID da disciplina
            'quiz_name': user[2],        # Nome do quiz
            'estudante': user[3],        # Nome do estudante
            'enunciado': user[4],        # Pergunta do quiz
            'alternativa_correta': user[5],  # Alternativa correta
            #[6] Resposta Sumario
            'respostas_concatenada': user[7], # Respostas do estudante concatenadas
            'hora_realizada': user[8],   # Horário da resposta
            'iscerta': user[9],          # Indicador de acerto (1 = correto, 0 = errado, -1 = não respondido)
            #[10] Resposta Aluno Conversao da 6
            'idQuestao': user[11],       # ID da questão
            'idUser': user[12],          # ID do usuário (estudante)
            'email': user[13],           # E-mail do estudante
            #[14] Status ativo 
            'idPergunta': user[15]       # ID da pergunta original
        }
        for user in users
    ]

    return users_data

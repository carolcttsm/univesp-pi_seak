import logging
from datetime import date
from website import db
from website.models import Professor, Aluno, Oficina, Turma, Presenca

def popular_banco_demo():
    logging.info("[SEED] Ambiente de demonstração detectado. Populando banco com dados de exemplo...")

    Presenca.query.delete()
    Turma.query.delete()
    Oficina.query.delete()
    Aluno.query.delete()
    Professor.query.delete()
    db.session.commit()

    prof_ana = Professor(nome="Ana Lúcia")
    prof_joao = Professor(nome="João Mendes")
    prof_carla = Professor(nome="Carla Souza")
    db.session.add_all([prof_ana, prof_joao, prof_carla])
    db.session.commit()

    of_hist = Oficina(
        nome="História do Brasil",
        descricao="Oficina de introdução à história brasileira",
        vagas=30,
        ano_mes="2025-05",
        professor=prof_ana
    )
    of_mat = Oficina(
        nome="Matemática Divertida",
        descricao="Jogos e dinâmicas com matemática básica",
        vagas=25,
        ano_mes="2025-05",
        professor=prof_joao
    )
    of_teatro = Oficina(
        nome="Teatro Infantil",
        descricao="Expressão corporal e teatro para crianças",
        vagas=20,
        ano_mes="2025-05",
        professor=prof_carla
    )
    db.session.add_all([of_hist, of_mat, of_teatro])
    db.session.commit()

    turma_mat = Turma(oficina_id=of_mat.id, horario="Segundas e quartas, 15h")
    turma_tea = Turma(oficina_id=of_teatro.id, horario="Sextas, 10h")
    db.session.add_all([turma_mat, turma_tea])
    db.session.commit()

    aluno1 = Aluno(nome="Maria Silva", sexo="F")
    aluno2 = Aluno(nome="Pedro Gomes", sexo="M")
    aluno3 = Aluno(nome="Larissa Oliveira", sexo="F")
    aluno4 = Aluno(nome="Diego Ramos", sexo="M")
    db.session.add_all([aluno1, aluno2, aluno3, aluno4])
    db.session.commit()

    turma_mat.alunos.extend([aluno2, aluno3])
    turma_tea.alunos.append(aluno4)
    db.session.commit()

    pres1 = Presenca(aluno_id=aluno2.id, oficina_id=of_mat.id, data=date(2025, 5, 20))
    pres2 = Presenca(aluno_id=aluno3.id, oficina_id=of_mat.id, data=date(2025, 5, 22))
    db.session.add_all([pres1, pres2])
    db.session.commit()

    logging.info("[SEED] Dados de demonstração inseridos com sucesso.")

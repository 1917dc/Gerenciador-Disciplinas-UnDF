import streamlit as st
from login_page import URL
import requests as req
import json
import guli
import pandas as pd

turma = {
    'id' : None,
    'professor': None,
    'nome' : None
}

turma_id = guli.GuliVariable('turma_id').get()
turma = req.get(URL + '/turmas/%s' %turma_id).json()

@st.experimental_dialog("Crie o feedback")
def create_feedback():
    turma_alunos_json = (req.get(URL + "/turmas/%s/alunos" %turma_id)).json()
    CHOICES = {aluno['id']: aluno['aluno']['nome'] for aluno in turma_alunos_json}
    def format_func(option):
        return CHOICES[option]

    option = st.selectbox("Selecione o aluno", options=list(CHOICES.keys()), format_func=format_func)

    titulo_feedback = st.text_area("Título do feedback")
    corpo_feedback = st.text_area("Corpo do feedback")

    if st.button("Enviar"):
        response = req.post(URL + "/feedbacks/aluno/post/%s/%s/%s" %(turma['id'], turma['professor']['id'], option),
                            json={"titulo": titulo_feedback,
                                  "corpo": corpo_feedback},
                            headers={"Content-Type": "application/json"})
        st.rerun()

def welcome():
    st.markdown('## Notas de :blue[%s]' %turma['nome'])

def table_alunos():
    turma_alunos_json = (req.get(URL + "/turmas/%s/alunos" %turma_id)).json()

    alunos_nomes = []
    alunos_cursos = []
    alunos_notas = []
    alunos_feedbacks = []
    alunos_ids = []


    for aluno in turma_alunos_json:

        # definindo quais informações vou pegar do json
        detalhes_aluno = {'id': None, 'aluno_id' : None, 'nota' : None, 'feedback' : None, 'curso' : None}

        # pegando feedback respectivamente
        feedback = {'id' : None, 'aluno' : None,'descricao' : None, 'turma' : None}

        if req.get(URL + '/feedbacks/%s' %aluno['aluno']['id']).json() == None:
            feedback['descricao'] = 'Sem feedback'
        else:
            feedback = req.get(URL + '/feedbacks/aluno/%s' %aluno['aluno']['id']).json()

        detalhes_aluno['id'] = aluno['id']
        detalhes_aluno['aluno_nome'] = aluno['aluno']['nome']
        detalhes_aluno['curso'] = aluno['aluno']['curso']
        detalhes_aluno['nota'] = aluno['nota']
        detalhes_aluno['feedback'] = feedback['corpo']

        alunos_ids.append(detalhes_aluno['id'])
        alunos_nomes.append(detalhes_aluno['aluno_nome'])
        alunos_notas.append(detalhes_aluno['nota'])
        alunos_cursos.append(detalhes_aluno['curso'])
        alunos_feedbacks.append(detalhes_aluno['feedback'])



    df = pd.DataFrame({
        'Indice' : alunos_ids,
        'Nome' : alunos_nomes,
        'Curso' : alunos_cursos,
        'Feedback' : alunos_feedbacks,
        'Nota' : alunos_notas
    })
    original_df = df.copy()
    # Exiba o editor de dataframe
    edited_df = st.data_editor(df, disabled=["Feedback","Nome", "Curso", "Laudo"], hide_index= True, width=900, key= 'df_copy', column_config={"Indice" : None})

    col1, col2 = st.columns(2)

    with col1:
        # Crie um botão para enviar alterações
        if st.button('Enviar Alterações'):
            # Encontre as diferenças entre os dataframes original e editado
            diff = pd.concat([original_df, edited_df]).drop_duplicates(keep=False)

            # Imprima as alterações
            counter = 0
            for index, row in diff.iterrows():
                counter += 1
                if counter == 2:
                    print(f"Índice: {row['Indice']}, Nome: {row['Nome']}, Nota: {row['Nota']}")
                    url = URL + "/alunos/%s/nota" %row['Indice']
                    headers = {"Content-Type": "application/json"}
                    data_json = row['Nota']
                    response = req.put(url, headers=headers, json=float(data_json))
                    if response.status_code != 200:
                        print(f"Error: Failed to update nota for aluno_id {row['Indice']}. Status code: {response.status_code}")
    with col2:
        if st.button('Gerar feedback'):
            create_feedback()

def start():
    welcome()
    st.divider()
    table_alunos()

start()
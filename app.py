import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('feira.db')
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute('''CREATE TABLE IF NOT EXISTS itens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descricao TEXT,
                    unidade TEXT,
                    quantidade INTEGER,
                    status TEXT)''')
conn.commit()

# Função para inserir novo item
def add_item(descricao, unidade, quantidade, status):
    cursor.execute("INSERT INTO itens (descricao, unidade, quantidade, status) VALUES (?, ?, ?, ?)",
                   (descricao, unidade, quantidade, status))
    conn.commit()

# Função para editar item
def update_item(id, descricao, unidade, quantidade, status):
    cursor.execute("UPDATE itens SET descricao = ?, unidade = ?, quantidade = ?, status = ? WHERE id = ?",
                   (descricao, unidade, quantidade, status, id))
    conn.commit()

# Função para excluir item
def delete_item(id):
    cursor.execute("DELETE FROM itens WHERE id = ?", (id,))
    conn.commit()

# Função para buscar itens
def get_itens(status=None):
    if status:
        cursor.execute("SELECT * FROM itens WHERE status = ?", (status,))
    else:
        cursor.execute("SELECT * FROM itens")
    return cursor.fetchall()

# Função para pegar um item por ID
def get_item_by_id(id):
    cursor.execute("SELECT * FROM itens WHERE id = ?", (id,))
    return cursor.fetchone()

# Página de Criação
def criar_item():
    st.title("Criar Novo Item")
    descricao = st.text_input("Descrição do item")
    unidade = st.text_input("Unidade")
    quantidade = st.number_input("Quantidade", min_value=0)
    status = st.selectbox("Status", ["pendente", "concluído"])

    if st.button("Adicionar"):
        add_item(descricao, unidade, quantidade, status)
        st.success("Item adicionado com sucesso!")

# Função para exibir a tabela com os dados e botões de editar e excluir
def exibir_tabela(itens):
    # Adiciona os cabeçalhos das colunas
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 2, 1.5, 2, 2, 1, 1])
    col1.write("**ID**")
    col2.write("**Descrição**")
    col3.write("**Unidade**")
    col4.write("**Quantidade**")
    col5.write("**Status**")
    col6.write("**Editar**")
    col7.write("**Excluir**")
    
    # Exibe os dados dos itens
    for item in itens:
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 2, 1.5, 2, 2, 1, 1])
        col1.write(item[0])  # ID
        col2.write(item[1])  # Descrição
        col3.write(item[2])  # Unidade
        col4.write(item[3])  # Quantidade
        col5.write(item[4])  # Status
        
        # Botões para editar e excluir
        edit_button = col6.button("✏️", key=f"edit_{item[0]}")  # Botão Editar
        delete_button = col7.button("❌", key=f"delete_{item[0]}")  # Botão Excluir

        # Verificação de clique no botão "Editar"
        if edit_button:
            # Armazenando os dados no session_state para persistência
            st.session_state.edit_item_id = item[0]
            st.session_state.edit_item_descricao = item[1]
            st.session_state.edit_item_unidade = item[2]
            st.session_state.edit_item_quantidade = item[3]
            st.session_state.edit_item_status = item[4]
        
        # Verificação de clique no botão "Excluir"
        if delete_button:
            delete_item(item[0])  # Excluir item
            st.success(f"Item {item[0]} excluído com sucesso!")  # Mensagem de sucesso após exclusão
            st.rerun()  # Forçar recarregamento da página

# Função de Modal de Edição
def editar_item():
    if 'edit_item_id' in st.session_state:
        item_id = st.session_state.edit_item_id
        descricao = st.text_input("Descrição", st.session_state.edit_item_descricao)
        unidade = st.text_input("Unidade", st.session_state.edit_item_unidade)
        quantidade = st.number_input("Quantidade", min_value=0, value=st.session_state.edit_item_quantidade)
        status = st.selectbox("Status", ["pendente", "concluído"], index=["pendente", "concluído"].index(st.session_state.edit_item_status))

        if st.button("Atualizar"):
            update_item(item_id, descricao, unidade, quantidade, status)
            st.success("Item atualizado com sucesso!")  # Mensagem de sucesso após atualização
            del st.session_state.edit_item_id  # Remove o estado após a atualização
            del st.session_state.edit_item_descricao
            del st.session_state.edit_item_unidade
            del st.session_state.edit_item_quantidade
            del st.session_state.edit_item_status
            st.rerun()  # Forçar recarregamento da página após atualização

# Página de Lista Geral
def lista_geral():
    st.title("Lista Geral de Itens")
    itens = get_itens()
    exibir_tabela(itens)

# Página de Itens Concluídos
def lista_concluidos():
    st.title("Lista de Itens Concluídos")
    itens = get_itens(status="concluído")
    exibir_tabela(itens)

# Página de Itens Pendentes
def lista_pendentes():
    st.title("Lista de Itens Pendentes")
    itens = get_itens(status="pendente")
    exibir_tabela(itens)

# Função principal para navegação com menu horizontal
def main():
    # Exibe o menu horizontal e navega entre as páginas
    selected = option_menu("Lista de Feira - Cartaxo's Family", ["Lista Geral", "Lista de Concluídos", "Lista de Pendentes","Novo Item"],
                           icons=["list", "check-circle", "hourglass","plus-circle"], menu_icon="cast", default_index=0, orientation="horizontal")

    if selected == "Novo Item":
        criar_item()
    elif selected == "Lista Geral":
        lista_geral()
    elif selected == "Lista de Concluídos":
        lista_concluidos()
    elif selected == "Lista de Pendentes":
        lista_pendentes()

    # Verifica se é necessário exibir o modal de edição
    if 'edit_item_id' in st.session_state:
        editar_item()

if __name__ == "__main__":
    main()
import streamlit as st

#Deixar barra de opções invisível
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Inicializa a sessão (se não existir)
if "pagina" not in st.session_state:
    st.session_state.pagina = "Início"

# Sidebar com botões
st.sidebar.button("Início", on_click=lambda: st.session_state.update({"pagina": "Início"}))
st.sidebar.button("Gráfico", on_click=lambda: st.session_state.update({"pagina": "Gráfico"}))
st.sidebar.button("Código", on_click=lambda: st.session_state.update({"pagina": "Código"}))


# Mostra conteúdo com base no estado
if st.session_state.pagina == "Início":
    st.markdown("<h1 style='text-align: center;'>No-Stress Elisa</h1>", unsafe_allow_html=True)
    st.subheader('Você poderá analisar com precisão dados do leitor de placas "Elisa" automaticamente')
    st.markdown("---", unsafe_allow_html=True)

elif st.session_state.pagina == "Gráfico":
    st.markdown("<h1 style='text-align: center;'>Gráfico</h1>", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)
    radio_btn = st.radio("Qual tipo de gráfico?", options=("Barra", "Linha"))    
    file = st.file_uploader("**1)** Faça o upload de seu arquivo:", type=["xlsx"])
    if radio_btn == "Barra":
        st.markdown("Barra")
    elif radio_btn == "Linha":
        st.markdown("Linha")



elif st.session_state.pagina == "Código":
    code = """
    #Colocar o código aqui

    """
    st.code(code, language="python")
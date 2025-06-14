import streamlit as st
import pandas as pd

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
    st.header("Equipe:")
    equipe = [
        {
            "nome": "Jõao Roberto B. K. Cruz",
            "resumo": "Resumo",
            "imagem": "images/matheus_velloso.jpg",
            "link": "https://github.com/RobertJbkc"
        },
        {
            "nome": "Lucas Candinho",
            "resumo": "Resumo",
            "imagem": "images/matheus_velloso.jpg",
            "link": "https://github.com/LucasCandinho"
        },
        {
            "nome": "Matheus P. Velloso da Silveira",
            "resumo": "Cursando bacharel em ciência e tecnologia na Ilum - Escola de Ciência ",
            "imagem": "images/matheus_velloso.jpg",
            "link": "https://github.com/Velky2"
        }
    ]
    cols = st.columns(3)

    for col, pessoa in zip(cols, equipe):
        with col:
            st.image(
                pessoa["imagem"], 
                width=250, 
                caption=None, 
                use_container_width=False
            )
            st.markdown(f"### {pessoa['nome']}")
            st.markdown(f"<p style='text-align: justify;'>{pessoa['resumo']}</p>", unsafe_allow_html=True)
            st.markdown(
    f'<a href="{pessoa["link"]}" target="_blank">'
    '<img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="50">'
    '</a>',
    unsafe_allow_html=True
)
elif st.session_state.pagina == "Gráfico":
    st.markdown("<h1 style='text-align: center;'>Gráfico</h1>", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)
    radio_btn = st.radio("Qual tipo de gráfico?", options=("Barra", "Linha"))    
    file = st.file_uploader("**1)** Faça o upload de seu arquivo:", type=["xlsx"])
    st.markdown("**2)** Selecione as concentrações de cada poço")

    # Definindo as linhas e colunas da placa
    rows = list("ABCDEFGH")
    cols = list(range(1, 13))

    # Inicializar a matriz se ainda não estiver na sessão
    if "elisa_matrix" not in st.session_state:
        matriz = pd.DataFrame(None, index=rows, columns=cols)
        st.session_state.elisa_matrix = matriz

    # Mostrar a matriz editável
    edited_matrix = st.data_editor(
        st.session_state.elisa_matrix,
        use_container_width=True,
        num_rows="fixed",
        hide_index=False
    )

    # Botão de salvar alterações
    if st.button("💾 Salvar alterações"):
        st.session_state.elisa_matrix = edited_matrix
        st.success("Concentrações atualizadas!")

    # Mostrar matriz salva
    with st.expander("📊 Ver matriz final"):
        st.dataframe(st.session_state.elisa_matrix, use_container_width=True)

    # Exportar como CSV
    st.download_button(
        label="📥 Baixar como CSV",
        data=st.session_state.elisa_matrix.to_csv().encode("utf-8"),
        file_name="matriz_elisa.csv",
        mime="text/csv"
    )
    
    if radio_btn == "Barra":
       #Colocar gráfico de barra
       # Exportar como CSV
        st.markdown("**3)** Veja o gráfico de barra do seu Elisa:")
    elif radio_btn == "Linha":
        #Colocar gráfico de linha
        st.markdown("**3)** Veja o seu gráfico de linha do seu Elisa:")
        



elif st.session_state.pagina == "Código":
    code = """
    #Colocar o código aqui

    """
    st.code(code, language="python")
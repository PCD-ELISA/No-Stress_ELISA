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
st.sidebar.button("Como usar", on_click=lambda: st.session_state.update({"pagina": "Como usar"}))
st.sidebar.button("Gráfico", on_click=lambda: st.session_state.update({"pagina": "Gráfico"}))
st.sidebar.button("Código", on_click=lambda: st.session_state.update({"pagina": "Código"}))


# Mostra conteúdo com base no estado
if st.session_state.pagina == "Início":
    #Cabeçalho
    st.markdown("<h1 style='text-align: center;'>No-Stress Elisa</h1>", unsafe_allow_html=True)
    st.subheader('Você poderá analisar com precisão dados do leitor de placas "Elisa" automaticamente')
    st.markdown("---", unsafe_allow_html=True)
    #Explicar sobre Elisa
    st.header(" 🡆 O que é um Leitor de placas Elisa?")
    elisa_info = ["images/elisa.png",
                """
                O leitor de Elisa (Enzyme-Linked Immunosorbent Assay) é um instrumento laboratorial
                que usa uma placa de 96 poços de microtitulação. Luz de um comprimento de onda específico
                incide em cada poço e através da diferença entre a luz emitida e detectada, é medida
                a absorbância individualmente.
                """]

    cols1 = st.columns(2)
    for col, info, indi in zip(cols1, elisa_info, [0,1]):
            with col:
                if indi == 0:
                    st.image(
                        info, 
                        width=250, 
                        caption=None, 
                        use_container_width=False
                    )
                else:
                    st.markdown(f"{info}")

    st.markdown("---", unsafe_allow_html=True)
    #Falar sobre a equipe
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
            "resumo": "Cursando bacharelado em ciência e tecnologia na Ilum - Escola de Ciência ",
            "imagem": "images/matheus_velloso.jpg",
            "link": "https://github.com/Velky2"
        }
    ]
    cols2 = st.columns(3)

    for col, pessoa in zip(cols2, equipe):
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
            
elif st.session_state.pagina == "Como usar":
    st.markdown("<h1 style='text-align: center;'>Como usar</h1>", unsafe_allow_html=True)
    st.subheader("Aprenda a utilizar nossa ferramenta de forma simples")
    st.markdown("---", unsafe_allow_html=True)
    


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
    concentracao = st.file_uploader("Ou faça upload das concentrações:", type=["xlsx"])

    
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
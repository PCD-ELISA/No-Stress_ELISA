import streamlit as st
import pandas as pd
from processa_dados import layout_para_dataframe
from processa_dados import remove_celulas_vazias
from processa_dados import recebe_arquivo
from processa_dados import separa_namostra
from gera_graficos import plot_absorbancia
import traceback
import io
from PIL import Image

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
    col1, col2 = st.columns([1, 2])
    with col1:
            st.image(
            "images/elisa.png",
            caption="Leitor de placas ELISA moderno",
            width=200
            )
    with col2:
            st.markdown("")
            st.markdown("")
            st.markdown(
                """
                O leitor de Elisa (Enzyme-Linked Immunosorbent Assay) é um instrumento laboratorial
                que usa uma placa de 96 poços de microtitulação. Luz de um comprimento de onda específico
                incide em cada poço e, através da diferença entre a luz emitida e detectada, é medida
                a absorbância ou fluorescência com alta precisão.
                """)
    st.markdown("<h3 style='text-align: center;'>Aplicações</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.28, 1, 1])
    with col1:
            st.markdown("""
                🔬 **Diagnóstico médico**  
                - Detecção de anticorpos e antígenos
                - Testes para HIV, hepatite, COVID-19
                - Diagnóstico de doenças autoimunes
                        """)
    with col2:
            st.markdown("""
                🧪 **Pesquisa científica**  
                - Quantificação de proteínas
                - Estudos imunológicos
                - Análise de sinalização celular
                        """)
    with col3:
            st.markdown("""
                🏭 **Controle de qualidade**  
                - Indústria farmacêutica
                - Segurança alimentar
                - Monitoramento ambiental                  
                """)
    
    st.markdown("---", unsafe_allow_html=True)
    #Falar sobre a equipe
    st.header("Equipe:")
    equipe = [
        {
            "nome": "Jõao Roberto B. K. Cruz",
            "resumo": "Cursando bacharelado em ciência e tecnologia na Ilum - Escola de Ciência ",
            "imagem": "images/joao_roberto.jpeg",
            "link": "https://github.com/RobertJbkc"
        },
        {
            "nome": "Lucas Candinho",
            "resumo": "Cursando bacharelado em ciência e tecnologia na Ilum - Escola de Ciência ",
            "imagem": "images/lucas_candinho.jpg",
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
    st.video("images/nostressexplanation.mp4")

elif st.session_state.pagina == "Gráfico":
    st.markdown("<h1 style='text-align: center;'>Gráfico</h1>", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)
    radio_btn = st.radio("Qual tipo de gráfico?", options=("Barra", "Linha"))    
    file = st.file_uploader("**1)** Faça o upload de seu arquivo:", type=["xlsx"])
    st.markdown("**2)** Selecione o contido em cada poço")
    st.markdown("(Poços com água devem ser escritos como Água)")

    # Definindo as linhas e colunas da placa
    rows = list("ABCDEFGH")
    cols = [str(i) for i in range(1, 13)]

    # Inicializar a matriz se ainda não estiver na sessão
    if "elisa_matrix" not in st.session_state:
        st.session_state.elisa_matrix = pd.DataFrame("", index=rows, columns=cols)

    # Mostrar a matriz editável
    edited_matrix = st.data_editor(
        st.session_state.elisa_matrix,
        use_container_width=True,
        num_rows="fixed",
        hide_index=False
    )

    # Botão de salvar alterações
    if st.button("💾 Salvar alterações"):
        st.session_state.elisa_matrix = edited_matrix.fillna("")
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
    st.markdown("Ou faça upload das informações:")
    dados = st.file_uploader("""Obs.: O Excel deverá ter informações de A a H representando as linhas da placa 
                             e de 1 a 12 representando as colunas""", type=["xlsx"])
    st.markdown("**3)** Veja o gráfico de barra do seu Elisa:")
    
    if st.button("📶 Plotar gráfico"):
        try:
            if file is None:
                st.error("⚠️ Por favor, envie o arquivo principal (leitor de placas)")
                raise ValueError("Arquivo principal não enviado")
            
            elif dados is not None:
                #Matriz do Excel
                try:
                    data = pd.read_excel(dados, header=None)
                    data.columns = list("ABCDEFGH")[:data.shape[1]]
                    data.index = range(1, data.shape[0] + 1)
                    layout = {}
                    for coluna in data.columns:
                        for linha in data.index:
                            valor = str(data.loc[linha, coluna]).strip()
                            if valor not in ["", "nan", "0", "None"]:
                                posicao = f"{coluna}{linha}"
                                if valor not in layout:
                                    layout[valor] = [posicao]
                                else:
                                    layout[valor].append(posicao)
                    
                    data_info = [[k] + v for k, v in layout.items()]
                    st.success("Dados processados com sucesso!")
        
                except Exception as e:
                    st.error(f"Erro ao processar arquivo: {str(e)}")
                
            else:
                # Matriz Analógica
                if st.session_state.elisa_matrix.empty:
                    st.error("⚠️ A matriz está vazia. Preencha ou envie um arquivo.")
                    raise ValueError("Matriz vazia")
                
                layout = {}
                for i in rows:
                    for j in cols:
                        tmp = st.session_state.elisa_matrix.loc[i, j]
                        if pd.isna(tmp) or str(tmp).strip() in ["", "0", "None", "-"]:
                            continue
                        if tmp not in layout:
                            layout[tmp] = [f"{i}{j}"]
                        else:
                            layout[tmp].append(f"{i}{j}")
                data_info = [[k] + v for k, v in layout.items()]
                st.success("Dados da Matriz carregados com sucesso!")
                
            #Processar dados

            layout = layout_para_dataframe(data_info)
            dados_amostrais = remove_celulas_vazias(recebe_arquivo(file))[1]
            dados_df = separa_namostra(layout, dados_amostrais)

            #Plotar gráficos
            if radio_btn == "Barra":
                imagem_grafico = plot_absorbancia(dados_df, "barra")
                st.image(
                        imagem_grafico,
                        width=800
                        )
                buf = io.BytesIO()
                imagem_grafico.save(buf, format="PNG")
                buf.seek(0)
    
                st.download_button(
                    label="📥 Baixar gráfico como PNG",
                    data=buf,
                    file_name="grafico_absorbancia_barra.png",
                    mime="image/png"
                )

            elif radio_btn == "Linha":
                imagem_grafico = plot_absorbancia(dados_df, "linha")
                st.image(
                        imagem_grafico,
                        width=800
                        )
                buf = io.BytesIO()
                imagem_grafico.save(buf, format="PNG")
                buf.seek(0)
    
                st.download_button(
                    label="📥 Baixar gráfico como PNG",
                    data=buf,
                    file_name="grafico_absorbancia_linha.png",
                    mime="image/png"
                )

        except Exception:
             st.markdown("Não foi possível plotar seu gráfico. Verifique se os arquivos correspondem ao solicitado")
             print(traceback.format_exc())
             

elif st.session_state.pagina == "Código":
    st.markdown("<h1 style='text-align: center;'>Código</h1>", unsafe_allow_html=True)
    st.subheader("Veja o código em python usado para tratamento de dados e plotagem do gráfico")
    st.markdown("---", unsafe_allow_html=True)
    code_gera_graficos = """
def plot_absorbancia(dados_df, tipo_grafico="barra"):
    dados = []
    for absorbancia in dados_df.index:
        for amostra in dados_df.columns:
            media, incerteza = dados_df.loc[absorbancia, amostra]
            dados.append({
                "Amostra": amostra,
                "Absorbância": absorbancia,
                "Média": media,
                "Incerteza": incerteza
            })

    print(dados)
    df_plot = pd.DataFrame(dados)
    print(df_plot)

    p = so.Plot(df_plot, x="Amostra", y="Média", color="Absorbância")

    if tipo_grafico == "barra":
        p = p.add(so.Bar(), so.Dodge())
    elif tipo_grafico == "linha":
        p = p.add(so.Line(marker="o"))
    else:
        raise ValueError("tipo_grafico deve ser 'barra' ou 'linha'.")

    p = p.label(x="Amostras", y="Absorbância (u.a.)")

    buf = io.BytesIO()
    p.save(buf, format="png")
    buf.seek(0)
    return Image.open(buf)

df_exemplo = pd.DataFrame({
    "Amostra1": [(0.52, 0.03), (0.68, 0.05), (0.75, 0.04)],
    "Amostra2": [(0.49, 0.02), (0.65, 0.06), (0.78, 0.05)],
    "Amostra3": [(0.55, 0.04), (0.63, 0.05), (0.80, 0.03)],
}, index=["Abs1", "Abs2", "Abs3"])

print(df_exemplo)

plot_absorbancia(df_exemplo)

"""
    code_processa_dados = """
def retira_branco(df, incerteza_equipamento=0):
    '''Retira o branco das medidas e propaga o erro por essa operação. O erro é a raiz quadrada
    da soma dos quadrados das incertezas.
    As incertezas concideradas sõa o erro do equipamento e a incerteza padrão
    
    Retorna o dataframe sem o branco e retorna a incerteza associada a cada medida
    '''

    # Define uma incerteza de equipamento
    branco = df['Água'].mean()
    incerteza_branco = df['Água'].sem()
    df_sem_branco = df.drop('Água', axis=1)
    for i in df_sem_branco:
        for j in df_sem_branco[i]:
            if j == 'nan':
                continue
            df_sem_branco[i] = df_sem_branco[i].replace(j, j-branco)
    # df_sem_branco -= branco 
    # Propagar o erro
    incerteza_saida = sqrt(pow(incerteza_equipamento, 2) + pow(incerteza_branco, 2))

    return df_sem_branco, incerteza_saida

def recebe_arquivo(nome_do_arquivo):
    # TODO:
    # Receber o arquivo da interface
    # Botar nomes mais significativos nas variáveis

    ''' 
    Essa função recebe um arquivo xlsx e transforma ele em um dataframe do Pandas.
    Por simplicidade, nesse protótipo inicial receberemos ele diretamente, sem intermédio
    da interface
    '''

    planilha = pd.read_excel(nome_do_arquivo, sheet_name=None, header=1)
    sheet_names = list(planilha.keys())
    metadados = planilha[sheet_names[0]]
    dados_amostrais = planilha[sheet_names[1]]

    return metadados, dados_amostrais
    
def remove_celulas_vazias(dataframes):
    ''' 
    Essa função recebe uma tupla de dataframes e remove celulas vazias

    Retorna uma tupla de dataframes com metadados e dados amostrais
    '''
    dataframes_processados = []
    for data in dataframes:
        data = data.drop('Unnamed: 0', axis=1)
        data = data.dropna()
        dataframes_processados.append(data)
    return dataframes_processados


def separa_layout(lista_amostras):
    colunas = []
    pocos = []
    for dado in lista_amostras:
        colunas.append(dado[0])
        dado.pop(0)
        pocos.append(dado)
    return colunas, pocos

def normaliza_lista(lista_amostras):
    # Gerado pelo ChatGPT
    maior_num_de_amostras = max(len(amostras) for amostras in lista_amostras) 
    normalizado = [amostras + [np.nan] * (maior_num_de_amostras - len(amostras)) for amostras in lista_amostras]
    return normalizado

def layout_para_dataframe(layout_provisorio):
    colunas, pocos = separa_layout(layout_provisorio)
    pocos = normaliza_lista(pocos)
    pocos_transposto = np.transpose(pocos)
    layout_organizado = pd.DataFrame(pocos_transposto, columns=colunas)
    return layout_organizado


def substitui(layout, dados_amostrais={}, abs=2):
    '''Separa em um dataframe (layout) apenas as absorbâncias de poços que contém uma determinada amostra
    
    Faz isso substituindo os poços (A1, A2, ...,) pelas absorbâncias medidas nesses poços.
    O parâmetro "abs" indica em qual comprimento de onda a medida de absorbancia foi realizada.
    "abs" >= 2

    Essa função lê apenas um comprimento de onda por vez
    '''

    abs = str(dados_amostrais.columns.tolist()[abs])
    #layout é uma tabela com colunas de composto químico e poços em que o composto está
    layout_copy = layout.copy()
    for i in layout_copy:
        for j in layout_copy[i]:
            if j == 'nan':
                continue
            # Encontra o índice na tabela de dados amostrais correspondente ao poço em que há uma amostra
            indice = dados_amostrais.index[dados_amostrais['Well'] == j].tolist()[0]
            # Substitui na cópia do layout o valor das absorbâncias associadas aos poços
            layout_copy[i] = layout_copy[i].replace(j, (dados_amostrais[abs][indice]))

    return layout_copy

def separa_namostra(layout, dados_amostrais={}):
    # Pega as colunas e os índices para formar uma tabela com os comprimentos de onda
    colunas = layout.columns.tolist()
    # Retira a coluna de Água pois essa sumirá na função retira branco
    colunas.pop(0)
    indice = [i for i in dados_amostrais if i.startswith('A')]
    
    # Anexar o valor de absorbância à coordenada Amostra; Comprimento (média, incerteza)
    lista_dados = []
    dados = []
    for i in range(len(indice)):

        dataframe_interno, incerteza = retira_branco(substitui(layout, dados_amostrais, abs=i+2))
        print(i)
        print('\n dataframe', dataframe_interno, '\n')    
        
        # Faz o dataframe ficar "numérico"
        for coluna in dataframe_interno:
            dataframe_interno[coluna] = pd.to_numeric(dataframe_interno[coluna], errors='coerce')

        

        for coluna in dataframe_interno:
            media = dataframe_interno[coluna].mean()
            sigma = dataframe_interno[coluna].sem()
            incerteza_saida = sqrt(pow(sigma, 2) + pow(incerteza, 2))
            dados.append((media, incerteza_saida))

        lista_dados.append(dados)
        dados = []


    df = pd.DataFrame(lista_dados, index=indice, columns=colunas)
    print(df)
    
    return df


    #     for coluna in dataframe_interno:

    #         # Calcula a média; Pandas não queria fazer o serviço
    #         soma = 0
    #         contador = 0
    #         for valor in dataframe_interno[coluna]:
    #             if valor == 'nan':
    #                 continue
    #             soma += valor
    #             contador += 1
    #         media = soma / contador

    #         dados.append((media, incerteza))
    #     lista_dados.append(dados)
    #     dados = []

    # df = pd.DataFrame(lista_dados, index=indice, columns=colunas)
    # print(df)
    
    # return df

layout_caso_teste = [["Água", "A10", "A11", "A12", "B10", "B11", "B12", "C10", "C11", "C12"],
                    ["Controle_1_ph2", "A1", "B1", "C1"],
                    ["Controle_1_ph8", "A5", "B5", "C5"],
                    ["Controle_2_ph2", "F1", "G1", "H1"],
                    ["Controle_2_ph8", "F5", "G5", "H5"],
                    ["CaCl2_1_ph2", "A2", "B2", "C2"],
                    ["CaCl2_1_ph8", "A6", "B6", "C6"],
                    ["CaCl2_2_ph2", "F2", "G2", "H2"],
                    ["CaCl2_2_ph8", "F6", "G6", "H6"],
                    ["FeSO4_1_ph2", "A3", "B3", "C3"],
                    ["FeSO4_1_ph8", "A7", "B7", "C7"],
                    ["FeSO4_2_ph2", "F3", "G3", "H3"],
                    ["FeSO4_2_ph8", "F7", "G7", "H7"]]


layout = layout_para_dataframe(layout_caso_teste)
dados_amostrais = remove_celulas_vazias(recebe_arquivo('Teste.xlsx'))[1]
print('Layout\n', layout)
print('Dados amostrais\n', dados_amostrais)
print('----------##########----------##########----------##########')

separa_namostra(layout, dados_amostrais)

"""
    st.header("Código para tratamento de dados:")
    st.code(code_processa_dados, language="python")
    st.markdown("---", unsafe_allow_html=True)
    st.header("Código para gerar gráfico:")
    st.code(code_gera_graficos, language="python")
    

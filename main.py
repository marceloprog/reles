#Universidade Federal de Uberlândia
#Faculdade de Engenharia Elétrica (FEELT)
#Projeto apresentado para a disciplina de Experimental de Circuitos Elétricos II
#Tema: Filtros Passivos
#Alunos: Isabela de Carvalho Favareto - 11711EBI025, Maria Luiza de Oliveira R. Pereira - 11811EBI023 e Mariana Rigo Estevão - 11711EBI008
#Professor: Wellington Maycon Santos Bernardes

import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import funcao_sistema as sistema

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

app.title = "Filtros Passivos"
app.config['suppress_callback_exceptions']=True
server = app.server

atual_clique = 0

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[

	html.Link(href="https://fonts.googleapis.com/css2?family=Indie+Flower&family=Open+Sans+Condensed:ital,wght@0,300;1,300&display=swap", style={"font-family": 'Roboto','textAlign': 'justify', 'color':'#20B2AA'}),
	dcc.Tabs(id="abas", value="aba-sobre", style={"font-family": 'Roboto','textAlign': 'center', 'backgroudColor':'#092269ff'}, children=[

		dcc.Tab(label="Sobre", value="aba-sobre",style={'borderColor':'#092269ff','backgroundColor':'#092269ff','color':'#FFFFFF'}),

		dcc.Tab(label="Instruções", value="aba-instrucoes",style={'borderColor':'#092269ff','backgroundColor':'#092269ff','color':'#FFFFFF'}),

		dcc.Tab(label="Interface", value="aba-interface",style={'borderColor':'#092269ff','backgroundColor':'#092269ff','color':'#FFFFFF'}),

		dcc.Tab(label="Agradecimentos", value="aba-agradecimentos",style={'borderColor':'#092269ff','backgroundColor':'#092269ff','color':'#FFFFFF'}),

		#dcc.Tab(label="Informações", value="aba-informacoes",style={'borderColor':'#092269ff','backgroundColor':'#092269ff','color':'#FFFFFF'}),
	]),

	html.H1("Coordenação de Relés de Sobrecarga", style={"font-family": 'Roboto','textAlign': 'center', 'backgroundColor':'#092269ff','color':'#FFFFFF','padding-y':'10px'}),

	html.Div(id="conteudo", style={'textAlign':'justify !important'} ),

	html.P("Nomes de quem fez", style={'margin-top':'10%',"font-family": 'Roboto','textAlign': 'center', 'backgroundColor':'#092269ff', 'color':'#FFFFFF'}),
])



@app.callback(Output('conteudo', 'children'),
			[Input('abas', 'value')])
def renderizar_aba(aba):
	if aba == "aba-sobre":
	
		return html.Div(style={'textAlign': 'justify', 'margin-right':'10%', 'margin-left':'10%', 'color': colors['text']}, children=[
                        html.Link(href="https://fonts.googleapis.com/css2?family=Indie+Flower&family=Open+Sans+Condensed:ital,wght@0,300;1,300&display=swap", rel="stylesheet"),
                        html.H4("Introdução Teórica", style={"font-family": 'Roboto','textAlign': 'center', 'color':'#008B88'}),
                        html.Br(),
			html.P("Os filtros eletrônicos analógicos estão presentes em quase todos os equipamentos, como por exemplo geradores de sinais, computadores, televisores, sistemas de som, entre outros."),
			html.P("Filtros passivos podem ser definidos como a combinação em série e em paralelo de dispositivos passivos, tais como resistores, indutores e capacitores, que atuam em função de selecionar ou rejeitar uma faixa de frequência. Esse tipo de filtro pode ser utilizado para eliminar ruídos ou frequências indesejáveis de componentes eletrônicos, bem como para potencializar ou atenuar faixas desejadas de frequência em sistemas de rádio, comunicação e som estéreo. Os filtros passivos podem ser divididos em quatro tipos: passa-baixa, passa-alta, passa-faixa e rejeita-faixa."),
                        html.P("Nestes filtros, os polos se encontram no semiplano esquerdo, enquanto os zeros se encontram sobre o eixo jw, entre −∞ e +∞. Apesar de majoritariamente ser levada em conta apenas a magnitude da resposta em frequência, a fase também pode ser considerada, se necessário. A faixa de frequência cujo filtro permite a passagem dos sinais é denominada banda de passagem, enquanto a faixa na qual não há interesse do sinal é chamada de banda de atenuação. Ainda, a faixa de frequências entre essas duas bandas é denominada região de transição, uma vez que os comportamentos dos filtros não são ideais, havendo uma faixa de transição de frequências entre as bandas de passagem e de atenuação."),
						html.P("A frequência de corte de um filtro pode ser definida como a potência média de saída do circuito, sendo assim a sua relação de ganho de G  =  0,5. Assim, substituindo essa relação nas fórmulas matemáticas das potências, encontra-se que a tensão de saída do circuito na frequência de corte é de 70,7% da tensão de entrada, como demonstrado pela equação a seguir:"),
                        html.Br(),
			html.P("Assim, dado que o ganho real do filtro se dá para R = XL:"),
                        html.Br(),
			html.Img(src="https://uploaddeimagens.com.br/images/002/992/844/full/form-ganho2.png?1607317486", style={'margin-left':'40%', 'margin-bottom':'30px'}),
                        html.Br(),
			html.P("Ou seja, para a frequência estabelecida como fc, o ganho real não é de 100%, mas sim de aproximadamente 70,7%, em outras palavras, há atenuação do sinal dentro desse espectro de frequência. Esse valor em dB é dado por:"),
                        html.Br(),
			html.Img(src="https://uploaddeimagens.com.br/images/002/992/845/original/form-ganho3.png?1607317505", style={'margin-left':'40%', 'margin-bottom':'30px'}),
                        html.Br(),
                        html.P("Então, pode-se dizer que a frequência provoca um ganho de -3 dB na tensão de saída em relação à entrada do circuito."),
		])

	if aba == "aba-instrucoes":
    		return html.Div(style={'textAlign': 'justify', 'margin-right':'10%', 'margin-left':'10%', 'color': colors['text']}, children=[
                 
                 html.P("Planilha para montagem do Sistema Elétrico:"),
                        
                 html.Button(html.A('Baixar',download='sistema_eletrico.xlsx',href='/sistema_eletrico.xlsx')   , id='submit-val', n_clicks=0),
                    html.Br(),
                 html.P("Planilha para disposição dos relés:"),
                        
                 html.Button(html.A('Baixar',download='teste.txt',href='teste.txt')   , id='submit-val', n_clicks=0),
                 #DOWNLOAD ESTÁ CORROMPENDO ARQUIVOS 

                    html.Br(),

                 


            ])

	if aba == "aba-interface":
    		return html.Div(style={'textAlign': 'justify', 'margin-right':'10%', 'margin-left':'10%', 'color': colors['text']}, children=[
                 
                 html.P("Inserir Planilha do Sistema Elétrico:"),
                        
                 html.Button(html.A('Baixar',download='sistema_eletrico.xlsx',href='/sistema_eletrico.xlsx')   , id='submit-val', n_clicks=0),
                    html.Br(),
                 html.P("Inserir planilha disposição dos relés:"),
                        
                 html.Button(html.A('Baixar',download='teste.txt',href='teste.txt')   , id='submit-val', n_clicks=0),
                 #DOWNLOAD ESTÁ CORROMPENDO ARQUIVOS 

                    html.Br(),
                
                

                 


            ])
	if aba == "aba-agradecimentos":
    		return html.Div(style={'textAlign': 'justify', 'margin-right':'10%', 'margin-left':'10%', 'color': colors['text']}, children=[
                        html.Link(href="https://fonts.googleapis.com/css2?family=Indie+Flower&family=Open+Sans+Condensed:ital,wght@0,300;1,300&display=swap", rel="stylesheet",style={"font-family": 'Roboto','textAlign': 'center', 'color':'#8a3399'}),
			html.P("Os filtros passivos possuem diversas aplicações, podendo ser elas nas áreas de meteorologia, aeronáutica, radiolocalização, radionavegação marítima, dentre várias outras. Para os filtros passa-baixa e passa-alta, as principais aplicações são nas áreas de processamento de sons, dados e imagens, podendo ser para circuitos de áudio, (sensores de circuitos com baixas frequências para o passa-baixa, e um protetor para um alto falante para o passa-alta, por exemplo), sensores industriais, ou área de telecomunicações."),
			html.P("Para o filtro passa-faixa, a aplicação mais comum é a de estações de rádio, nas quais as estações operam em faixas determinadas de frequência. Já para o filtro rejeita-faixa, algumas de suas aplicações são nas áreas de processamento de som, através de consoles de mixagem e diversos outros dispositivos de áudio."),
			html.P("Para visualizar as diversas faixas de frequências atribuídas no Brasil, clique no link referente ao site da Anatel:"),
                        html.Br(),
			html.A('ATRIBUIÇÃO DE FAIXAS DE FREQUÊNCIAS NO BRASIL', href='https://www.anatel.gov.br/Portal/verificaDocumentos/documento.asp?numeroPublicacao=314474&pub=original&filtro=1&documentoPath=314474.pdf', style={'textAlign': 'center', 'color':'#008B88' }),
                        
		])

		
	

	""" if aba == "aba-interface":
    	
		return html.Div(style={'textAlign': 'justify', 'margin-right':'10%', 'margin-left':'10%', 'color': colors['text']}, children=[
			html.Br(),
                        html.H6("MODO DE USO:", style={"font-family": 'Open Sans Condensed', 'colors':'#008B88'}),
                        
			dcc.Markdown('''
			> Utilize de ponto (".") para separar as casas decimais.
			> Coloque o número utilizando de casas decimais e não de múltiplos como k (quilo), u(micro), dentre outros.
			> 
			> As unidades do resistor, indutor e capacitor são dadas em ohm, henry e faraday, respectivamente.
			>
			> Não está previsto na calculadora:
			> - O uso de vírgula;
			> - O uso de notação científica;
			> - O uso de prefixos do Sistema Internacional de Unidades.
			'''),
                        html.Br(),
			dcc.Dropdown(id="seletor-filtro", value="FPB", clearable=False, style={'textAlign':'center', 'margin-left':'20%', 'backgroudColor':'#FFFFFF', 'color': '#20B2AA', 'max-width': '360px'}, options=[
                {"label": "Filtro Passa Baixa", "value": "FPB"},
                {"label": "Filtro Passa Alta", "value": "FPA"},
                {"label": "Filtro Passa Faixa", "value": "FPF"},
                {"label": "Filtro Rejeita Faixa", "value": "FRF"}
            ]),
            html.Div(style={"display": "flex-direction: column"}, children=[
                dcc.Input(id="campo-resistor", type="number", placeholder="Valor do resistor", style={'margin-top':'15px', 'margin-left':'15%', 'backgroudColor':'#FFFFFF', 'max-width': '200px', 'textAlign':'center','color': '#20B2AA', 'margin-right':'20px', "flex-grow":'1'}),
                dcc.Input(id="campo-indutor", type="number", placeholder="Valor do indutor", style={'max-width': '200px', 'textAlign':'center','backgroudColor':'#FFFFFF', 'color': '#20B2AA', 'margin-right':'20px',"flex-grow":'1'}),
                dcc.Input(id="campo-capacitor", type="number", placeholder="Valor do capacitor", style={'max-width': '200px', 'textAlign':'center','backgroudColor':'#FFFFFF', 'color': '#20B2AA', "flex-grow":'1'}),

            ]),
            html.Div(style={"display": "flex-direction: column", 'max-width': '200px', 'textAlign':'center', 'margin-left':'35%', 'margin-top':'15px'}, children=[
                html.Button("Calcular", id="submit-val", n_clicks = 0),
            ]),
            html.Div(id="resultado")
		]) """

	return ""

@app.callback(Output('resultado', 'children'),
			[Input('seletor-filtro', 'value'),
			Input('campo-resistor', 'value'),
			Input('campo-indutor','value'),
			Input('campo-capacitor', 'value'),
			Input('submit-val', 'n_clicks')])
def calcular(filtro, resistor, indutor, capacitor, cliques):
	global atual_clique
	if cliques is not None:
		if cliques > atual_clique:
			atual_clique = cliques
			if filtro == "FPB":
				denominador = (2.0 *3.1415* resistor * capacitor)
				fc = 1/denominador
				
				if resistor is None:
					return "Insira o valor de resistência"

				if capacitor is None:
					return "Insira valor do capacitor"
				
				return html.Div(children=[
					html.Br(),
                                        html.P("O valor da frequência de corte do Filtro Passa Baixa é:"),
					html.P("Frequência de corte =" ),
					html.P(fc),
					html.P("Hz"),
					html.Br(),
					html.Br(),
					html.P("Seu filtro apresenta o seguinte comportamento:", style ={'textAlign': 'center'}),
					html.Img(src="https://uploaddeimagens.com.br/images/002/992/847/full/gr-baixa.png?1607317622", style={'margin-left':'30%', 'margin-bottom':'30px'}),
					html.P("Fonte: Boylestad, 2012.",style ={'textAlign': 'center'}),
				])
			
			if filtro == "FPA":
				denominador = (2*3.1415*resistor*capacitor)
				fc = (1/denominador)
				
				if resistor is None:
					return "Insira o valor de resistência"

				if capacitor is None:
					return "Insira valor do capacitor"
				
				return html.Div(children=[
					html.Br(),
                    				html.P("O valor da frequência de corte do Filtro Passa Alta é:"),
					html.P("Frequência de corte =" ),
					html.P(fc),
					html.P("Hz"),
					html.Br(),
					html.Br(),
					html.P("Seu filtro apresenta o seguinte comportamento:", style ={'textAlign': 'center'}),
					html.Img(src="https://uploaddeimagens.com.br/images/002/992/850/original/gr-alta.png?1607317677", style={'margin-left':'30%', 'margin-bottom':'30px'}),
					html.P("Fonte: Boylestad, 2012.",style ={'textAlign': 'center'}),
				])

			if filtro == "FPF":
				denominador = (2*3.1415*((indutor*capacitor)**(1/2)))
				fc = (1/denominador)
				x = (resistor/(2 * indutor))**2
				x = (x + (1/(indutor*capacitor)))
				x =((x)**(1/2))
				y = (resistor/(2*indutor))
				fcmin = x - y
				fcmax = x + y
				banda = fcmax - fcmin

				if resistor is None:
					return "Insira o valor de resistência"

				if capacitor is None:
					return "Insira valor do capacitor"

				if resistor is None:
					return "Insira o valor do indutor"
				
				return html.Div(children=[
					html.Br(),
                    				html.P("Para o Filtro Passa Faixa, tem-se:"),
					html.P("Frequência de corte mínima =" ),
					html.P(fcmin),
					html.P("Hz"),
					html.P("Frequência de corte máxima =" ),
					html.P(fcmax),
					html.P("Hz"),
					html.P("Frequência de corte média =" ),
					html.P(fc),
					html.P("Hz"),
					html.P("Banda de passagem =" ),
					html.P(banda),
					html.P("Hz"),
					html.Br(),
					html.Br(),
					html.P("Seu filtro apresenta o seguinte comportamento:", style ={'textAlign': 'center'}),
					html.Img(src="https://uploaddeimagens.com.br/images/002/992/854/full/gr-passafaixa.png?1607317751", style={'margin-left':'30%', 'margin-bottom':'30px'}),
					html.P("Fonte: Boylestad, 2012.",style ={"textAlign": "center"}),
					html.Br(),
				])

			if filtro == "FRF":
				denominador = (2*3.1415*((indutor*capacitor)**(1/2)))
				fc = (1/denominador)
				x = (resistor/(2 * indutor))**2
				x = (x + (1/(indutor*capacitor)))
				x =((x)**(1/2))
				y = (resistor/(2*indutor))
				fcmin = x - y
				fcmax = x + y
				banda = fcmax - fcmin

				if resistor is None:
					return "Insira o valor de resistência"

				if capacitor is None:
					return "Insira valor do capacitor"

				if resistor is None:
					return "Insira o valor do indutor"
				
				return html.Div(children=[
					html.Br(),
                    				html.P("Para o Filtro Rejeita Faixa, tem-se:"),
					html.P("Frequência de corte mínima =" ),
					html.P(fcmin),
					html.P("Hz"),
					html.P("Frequência de corte máxima =" ),
					html.P(fcmax),
					html.P("Hz"),
					html.P("Frequência de central =" ),
					html.P(fc),
					html.P("Hz"),
					html.P("Banda de rejeição =" ),
					html.P(banda),
					html.P("Hz"),
					html.Br(),
					html.Br(),
							html.P("Seu filtro apresenta o seguinte comportamento:", style ={'textAlign': 'center'}),
					html.Img(src="https://uploaddeimagens.com.br/images/002/992/857/original/gr-rejeita.png?1607317807", style={'margin-left':'30%', 'margin-bottom':'30px'}),
					html.P("Fonte: Boylestad, 2012.",style ={"textAlign": "center"}),
					html.Br(),
				])

				

	raise PreventUpdate
	return ""

if __name__ == '__main__':
	app.run_server(debug=True)
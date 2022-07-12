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
	dcc.Tabs(id="abas", value="aba-filtros", style={"font-family": 'Roboto','textAlign': 'center', 'backgroudColor':'#20B2AA'}, children=[
		dcc.Tab(label="Filtros", value="aba-filtros",style={'borderColor':'#20B2AA','backgroundColor':'#20B2AA','color':'#FFFFFF'}),
		dcc.Tab(label="Tipos de Filtros", value="aba-tiposdefiltros",style={'borderColor':'#20B2AA','backgroundColor':'#20B2AA','color':'#FFFFFF'}),
		dcc.Tab(label="Calculadora", value="aba-calculadora",style={'borderColor':'#20B2AA','backgroundColor':'#20B2AA','color':'#FFFFFF'}),
		dcc.Tab(label="Aplicações", value="aba-aplicacoes",style={'borderColor':'#20B2AA','backgroundColor':'#20B2AA','color':'#FFFFFF'}),
		dcc.Tab(label="Informações", value="aba-informacoes",style={'borderColor':'#20B2AA','backgroundColor':'#20B2AA','color':'#FFFFFF'}),
	
	]),
	html.H1("Filtros Passivos", style={"font-family": 'Roboto','textAlign': 'center', 'backgroundColor':'#20B2AA','color':'#FFFFFF'}),
	html.Div(id="conteudo", style={'textAlign':'justify !important'} ),
	html.P("Desenvolvido por Isabela, Maria Luiza e Mariana", style={'margin-top':'10%',"font-family": 'Roboto','textAlign': 'center', 'backgroundColor':'#20B2AA', 'color':'#FFFFFF'}),
])



@app.callback(Output('conteudo', 'children'),
			[Input('abas', 'value')])
def renderizar_aba(aba):
	if aba == "aba-filtros":
	
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

	if aba == "aba-tiposdefiltros":
    		return html.Div(style={'textAlign': 'justify', 'margin-right':'10%', 'margin-left':'10%', 'color': colors['text']}, children=[
                        html.Link(href="https://fonts.googleapis.com/css2?family=Indie+Flower&family=Open+Sans+Condensed:ital,wght@0,300;1,300&display=swap", rel="stylesheet"),
                        html.H4("Filtro Passa-Baixa", style={"font-family": 'Roboto','textAlign': 'center', 'color':'#008B88'}),
                        html.Br(),
			html.P("O filtro passa-baixa tem como característica permitir a passagem de sinais de baixa frequência, rejeitando sinais acima da frequência de corte do filtro projetado. Seu comportamento é ilustrado através da Figura 1, enquanto sua configuração para um circuito RC é apresentada na Figura 2."),
                        html.Br(),
			html.P("Figura 1 - Comportamento do filtro passa-baixa", style ={'textAlign': 'center'}),
			html.Img(src="https://uploaddeimagens.com.br/images/002/992/847/full/gr-baixa.png?1607317622", style={'margin-left':'30%', 'margin-bottom':'30px'}),
			html.P("Fonte: Boylestad, 2012.",style ={'textAlign': 'center'}),
                        html.Br(),
			html.P("Figura 2 - Configuração do circuito do filtro passa-baixa",  style ={'textAlign': 'center'}),
			html.Img(src="https://uploaddeimagens.com.br/images/002/992/848/full/FPB.png?1607317640", style={'margin-left':'40%', 'margin-bottom':'30px'}),
			html.P("Fonte: Boylestad, 2012.",  style ={'textAlign': 'center'}),
                        html.Br(),
			html.P("A frequência de corte para esse tipo de filtro é demonstrada pela equação a seguir:"),
			html.Img(src="https://uploaddeimagens.com.br/images/002/992/849/full/fc-pb.png?1607317655", style={'margin-left':'40%', 'margin-bottom':'30px'}),
                        html.Br(),
			html.Br(),

			html.H4("Filtro Passa-Alta", style={"font-family": 'Roboto','textAlign': 'center', 'color':'#008B88'}),
                        html.Br(),
			html.P("O filtro passa-alta pode ser obtido invertendo as posições do resistor e do capacitor no filtro passa-baixa. De maneira semelhante, esse filtro tem como característica o comportamento inverso do passa-baixa, ou seja, permite a passagem de sinais de alta frequência, rejeitando sinais abaixo da frequência de corte do filtro projetado. Seu comportamento é ilustrado através da Figura 3, enquanto sua configuração para um circuito RC é apresentada na Figura 4."),
                        html.Br(),
			html.P("Figura 3 - Comportamento do filtro passa-alta",style ={"textAlign": "center"}),

			html.Img(src="https://uploaddeimagens.com.br/images/002/992/850/original/gr-alta.png?1607317677", style={'margin-left':'30%', 'margin-bottom':'30px'}),
			html.P("Fonte: Boylestad, 2012.", style ={"textAlign": "center"}),
                        html.Br(),
			html.P("Figura 4 - Configuração do circuito do filtro passa-alta",style ={"textAlign": "center"}),
			html.Img(src="https://uploaddeimagens.com.br/images/002/992/851/original/FPA.png?1607317691", style={'margin-left':'40%', 'margin-bottom':'30px'}),
			html.P("Fonte: Boylestad, 2012.",style ={'textAlign': 'center'}),
                        html.Br(),
			html.P("A frequência de corte para esse tipo de filtro é coincidente a do filtro passa-baixa, demonstrada pela equação a seguir:"),
			html.Img(src="https://uploaddeimagens.com.br/images/002/992/852/original/fc-pa.png?1607317709", style={'margin-left':'40%', 'margin-bottom':'30px'}),
			html.Br(),
			html.P("Sabendo que as fórmulas de frequência de corte são iguais para os filtros passa-baixa e passa-alta, é possível estabelecer uma relação em comum para os dois tipos de filtro, sendo exposta através da equação a seguir:"),
                        html.Br(),
			html.Img(src="https://uploaddeimagens.com.br/images/002/992/853/original/fc.png?1607317731", style={'margin-left':'30%', 'margin-bottom':'30px'}),
			html.Br(),
			html.Br(),

			html.H4("Filtro Passa-Faixa", style={"font-family": 'Roboto','textAlign': 'center', 'color':'#008B88'}),
                        html.Br(),
			html.P("Esse tipo de filtro possui a característica de permitir a passagem de uma faixa de frequências de uma banda determinada através das frequências de corte inferior e superior, rejeitando as frequências fora dessa faixa."),
			html.P("Seu comportamento é ilustrado através da Figura 5, enquanto sua configuração é apresentada na Figura 6."),
                        html.Br(),
			html.P("Figura 5 - Comportamento do filtro passa-faixa",style ={"textAlign": "center"}),
			html.Img(src="https://uploaddeimagens.com.br/images/002/992/854/full/gr-passafaixa.png?1607317751", style={'margin-left':'30%', 'margin-bottom':'30px'}),
			html.P("Fonte: Boylestad, 2012.",style ={"textAlign": "center"}),
                        html.Br(),
			html.P("Figura 6 - Configuração do circuito do filtro passa-faixa em série e em paralelo",style ={'textAlign': 'center'}),
			html.Img(src="https://uploaddeimagens.com.br/images/002/992/855/original/FPF.png?1607317767", style={'margin-left':'30%', 'margin-bottom':'30px'}),
			html.P("Fonte: Boylestad, 2012.",style ={'textAlign': 'center'}),
                        html.Br(),
			html.P("A frequência de corte para esse tipo de filtro é demonstrada pela equação a seguir:"),
			html.Img(src="https://uploaddeimagens.com.br/images/002/992/856/original/fc-pf.png?1607317786", style={'margin-left':'40%', 'margin-bottom':'30px'}),
			html.Br(),
			html.P("Os filtros eletrônicos analógicos estão presentes em quase todos os equipamentos, como por exemplo geradores de sinais, computadores, televisores, sistemas de som, entre outros."),
			html.P("Para altas frequências, o indutor do circuito tende a se comportar como circuito aberto, enquanto o capacitor opera como um curto circuito. No entanto, para a situação contrária, sob baixas frequências, o indutor opera como um curto circuito, enquanto o capacitor se comporta como circuito aberto."),
                        html.P("Então, pode-se dizer que, para a primeira situação, a maior parte da tensão de entrada está sobre o indutor, o que impede a passagem de sinais. Já para baixas frequências, a maior parte da tensão de entrada está sobre o capacitor, impedindo a passagem de sinais da mesma maneira."),
			html.P("Dessa forma, para frequências médias, o os componentes se comportam como curto circuito, permitindo, a passagem de frequências dentro dessa faixa determinada. Esse fator ocorre na chamada frequência de ressonância, sendo quando o módulo das reatâncias indutiva e capacitiva se igualarem e, consequentemente, se anularem."),
			html.Br(),
			html.Br(),
			
			html.H4("Filtro Rejeita-Faixa", style={"font-family": 'Roboto','textAlign': 'center', 'color':'#008B88'}),
                        html.Br(),
			html.P("O filtro rejeita-faixa possui um comportamento inverso ao demonstrado para o filtro passa-faixa, uma vez que ele rejeita as frequências de uma determinada banda, permitindo a passagem dessas frequências fora dela."),
			html.P("Seu comportamento é ilustrado através da Figura 7, enquanto sua configuração é apresentada na Figura 8."),
                        html.Br(),
			html.P("Figura 7 - Comportamento do filtro rejeita-faixa",style ={'textAlign': 'center'}),
			html.Img(src="https://uploaddeimagens.com.br/images/002/992/857/original/gr-rejeita.png?1607317807", style={'margin-left':'30%', 'margin-bottom':'30px'}),
			html.P("Fonte: Boylestad, 2012.",style ={'textAlign': 'center'}),
                        html.Br(),
			html.P("Figura 8 - Configuração do circuito do filtro rejeita-faixa em série e em paralelo",style ={'textAlign': 'center'}),
			html.Img(src="https://uploaddeimagens.com.br/images/002/992/859/original/FRF.png?1607317821", style={'margin-left':'30%', 'margin-bottom':'30px'}),
			html.P("Fonte: Boylestad, 2012.",style ={'textAlign': 'center'}),
                        html.Br(),
			html.P("A frequência de corte para esse tipo de filtro é demonstrada pela equação a seguir:"),
			html.Img(src="https://uploaddeimagens.com.br/images/002/992/860/original/fc-rf.png?1607317840", style={'margin-left':'40%', 'margin-bottom':'30px'}),
			html.Br(),
			html.P("Os filtros rejeita-faixa podem ser construídos a partir de uma combinação de um filtro passa-baixa e um passa-alta, de acordo com a Figura 9."),
                        html.Br(),
			html.P("Figura 9 - Filtro rejeita-faixa construído a partir de filtros passa-baixa e passa-alta.",style ={'textAlign': 'center'}),
			html.Img(src="https://uploaddeimagens.com.br/images/002/992/862/original/rf.png?1607317857", style={'margin-left':'30%', 'margin-bottom':'30px'}),
			html.P("Fonte: Boylestad, 2012.",style ={'textAlign': 'center'}),
		])

	if aba == "aba-informacoes":
    		return html.Div(style={'textAlign': 'justify', 'margin-right':'10%', 'margin-left':'10%', 'color': colors['text']}, children=[
                        html.Link(href="https://fonts.googleapis.com/css2?family=Indie+Flower&family=Open+Sans+Condensed:ital,wght@0,300;1,300&display=swap", rel="stylesheet",style={"font-family": 'Roboto','textAlign': 'center', 'color':'#8a3399'}),
                        dcc.Markdown('''
							> Universidade Federal de Uberlândia
							>
							> Faculdade de Engenharia Elétrica 
							> 
							> Graduação em Engenharia Biomédica
							>
							> Experimental de Circuitos Elétricos II
							>
							>
							>
							>Alunas: 
							>
							>Isabela de Carvalho Favareto - 11711EBI025
							>
							>Maria Luiza de Oliveira Rodrigues Pereira - 11811EBI023
							>
							>Mariana Rigo Estevão - 11711EBI008
							>
							>
							>Professor:
							>
							> Wellington Maycon Santos Bernardes
							
					'''),
						
                        			html.Br(),
		])				

	if aba == "aba-aplicacoes":
    		return html.Div(style={'textAlign': 'justify', 'margin-right':'10%', 'margin-left':'10%', 'color': colors['text']}, children=[
                        html.Link(href="https://fonts.googleapis.com/css2?family=Indie+Flower&family=Open+Sans+Condensed:ital,wght@0,300;1,300&display=swap", rel="stylesheet",style={"font-family": 'Roboto','textAlign': 'center', 'color':'#8a3399'}),
			html.P("Os filtros passivos possuem diversas aplicações, podendo ser elas nas áreas de meteorologia, aeronáutica, radiolocalização, radionavegação marítima, dentre várias outras. Para os filtros passa-baixa e passa-alta, as principais aplicações são nas áreas de processamento de sons, dados e imagens, podendo ser para circuitos de áudio, (sensores de circuitos com baixas frequências para o passa-baixa, e um protetor para um alto falante para o passa-alta, por exemplo), sensores industriais, ou área de telecomunicações."),
			html.P("Para o filtro passa-faixa, a aplicação mais comum é a de estações de rádio, nas quais as estações operam em faixas determinadas de frequência. Já para o filtro rejeita-faixa, algumas de suas aplicações são nas áreas de processamento de som, através de consoles de mixagem e diversos outros dispositivos de áudio."),
			html.P("Para visualizar as diversas faixas de frequências atribuídas no Brasil, clique no link referente ao site da Anatel:"),
                        html.Br(),
			html.A('ATRIBUIÇÃO DE FAIXAS DE FREQUÊNCIAS NO BRASIL', href='https://www.anatel.gov.br/Portal/verificaDocumentos/documento.asp?numeroPublicacao=314474&pub=original&filtro=1&documentoPath=314474.pdf', style={'textAlign': 'center', 'color':'#008B88' }),
                        
		])

		
	

	if aba == "aba-calculadora":
    	
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
		])
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
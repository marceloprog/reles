import pandas as pd
import pandapower as pp
import pandapower.shortcircuit as sc
import numpy as np
import reles as rs
from copy import deepcopy

from dash import html,dcc

import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

import time


#Local do arquivo
filename = r"sistema_eletrico.xlsx"


def rede(filename):
    "Construindo um rede no PandaPower"
    

    #Criando a rede
    net = pp.create_empty_network(f_hz=60, sn_mva=100) 
    
    #Criando as barras
    df = pd.read_excel(filename,
                  sheet_name= "Barras", index_col= 0)

    for idx in df.index:
        pp.create_bus(net, name=df.at[idx,"name"], vn_kv=df.at[idx,"vn_kv"],
                  zone=df.at[idx,"zone"], in_service=df.at[idx,"in_service"])
    
    
    #Criando um gerador externo - slack
    df = pd.read_excel(filename,
                  sheet_name= "Gerador - Slack")
    for idx in df.index:
        pp.create_ext_grid(net,bus=df.at[idx,"bus"],vm_pu=df.at[idx,"vm_pu"], 
                      va_degree=df.at[idx,"va_degree"],  
                      s_sc_max_mva=df.at[idx,"s_sc_max_mva"],
                      s_sc_min_mva=df.at[idx,"s_sc_min_mva"],
                      rx_max=df.at[idx,"rx_max"],
                      rx_min=df.at[idx,"rx_min"],
                      r0x0_max=df.at[idx,'r0x0_max'],
                      x0x_max=df.at[idx,'x0x_max'])

    
    
    #Criando as linhas
    df = pd.read_excel(filename,
                  sheet_name= "Linhas")
    for idx in df.index:
        pp.create_line_from_parameters(net, from_bus=df.at[idx,"from_bus"], 
                                   to_bus=df.at[idx,"to_bus"],
                                   length_km=df.at[idx,"length_km"],
                                   r_ohm_per_km=df.at[idx,"r_ohm_per_km"],
                                   x_ohm_per_km=df.at[idx,"x_ohm_per_km"],
                                   c_nf_per_km=df.at[idx,"c_nf_per_km"],
                                   g_us_per_km=df.at[idx,"g_us_per_km"],
                                   max_i_ka=df.at[idx,"max_i_ka"],
                                   r0_ohm_per_km=df.at[idx,"r0_ohm_per_km"],
                                   x0_ohm_per_km=df.at[idx,"x0_ohm_per_km"],
                                   c0_nf_per_km=df.at[idx,"c0_nf_per_km"])

    #Criando as cargas
    df = pd.read_excel(filename,
                  sheet_name= "Carga", index_col= 0)

    for idx in df.index:
        pp.create_load(net, bus=df.at[idx,"bus"], p_mw=df.at[idx,"p_mw"],
                   q_mvar=df.at[idx,"q_mvar"])
    
    

    
    #Criando o transformador
    df = pd.read_excel(filename,
                  sheet_name= "Trafo")
    for idx in df.index:
        pp.create_transformer_from_parameters(net, name=df.at[idx,"name"],
                                          hv_bus=df.at[idx,"hv_bus"],
                                          lv_bus=df.at[idx,"lv_bus"],
                                          sn_mva=df.at[idx,"sn_mva"],
                                          vn_hv_kv=df.at[idx,"vn_hv_kv"],
                                          vn_lv_kv=df.at[idx,"vn_lv_kv"],
                                          vk_percent=df.at[idx,"vk_percent"],
                                          vkr_percent=df.at[idx,"vkr_percent"],
                                          i0_percent=df.at[idx,"i0_percent"],
                                          pfe_kw=df.at[idx,"pfe_kw"],
                                          in_service=df.at[idx,"in_service"],
                                          vk0_percent=df.at[idx,"vk0_percent"],
                                          vkr0_percent=df.at[idx,"vkr0_percent"],
                                          mag0_percent=df.at[idx,"mag0_percent"],
                                          mag0_rx=df.at[idx,"mag0_rx"],
                                          si0_hv_partial=df.at[idx,"si0_hv_partial"])


   
    
    # Criando shunts
    df = pd.read_excel(filename,
                  sheet_name= "Shunt")
    for idx in df.index:
        pp.create_shunt(net, bus=df.at[idx,"bus"],
                    name=df.at[idx,"name"],
                    q_mvar=df.at[idx,"q_mvar"], p_mw=df.at[idx,"p_mw"],
                    vn_kv=df.at[idx,"vn_kv"], step=df.at[idx,"step"],
                    max_step=df.at[idx,"max_step"],
                    in_service=df.at[idx,"in_service"])
    
    
    return net


def conversao(net):
    "Convertendo de Dataframe no Pandas para dicionário em Python"
    
    #Dicionário de Barras
    bus = net.bus.to_dict('list')
   
    #Dicionário de Cargas
    load = net.load.to_dict('list')

    #Dicionário de Geradores
    gen = net.gen.to_dict('list')

    #Dicionário de Shunt
    shunt = net.shunt.to_dict('list')

    #Dicionário de ext_grid
    ext_grid = net.ext_grid.to_dict('list')

    #Dicionário de linhas
    line = net.line.to_dict('list')

    #Dicionário de trafo
    trafo = net.trafo.to_dict('list')
    
    return bus, load, gen, shunt, ext_grid, line, trafo  


def barras_fic(net,line, bus, m, len1):
    
    #"Insere as barras ficticias no sistema"
    
    porcentagem = 1 - len1/100
    
    #Definindo a tensão nas barras fictícias

    v_DE = [ ]
    v_PARA = [ ] 

    for l in line['from_bus']:
        k = bus['vn_kv'][l]
        v_DE.append(k)
        
    for ll in line['to_bus']:
        t = bus['vn_kv'][ll]
        v_PARA.append(t)
        

    #Calculando a tensão em cada barra ficticia
    V_BF = ((np.array(v_PARA) - np.array(v_DE))* porcentagem)  + np.array(v_DE)
    
    pp.create_bus(net, name='b1000', vn_kv=V_BF[m], type='b')    
    
    
 
def line_fic(net,DEprim, PARAprim, i, m, len1 ):
    "Inserindo linhas fictícias no sistema baseado na porcentagem fornecida"
    
    #A porcentagem que o usuário deseja do curto-circuito
    comprimento = len1/100
    
    pp.create_line_from_parameters(net, from_bus= DEprim[i], 
                                   to_bus= len(net.bus) - 1 ,
                                   length_km= comprimento,
                                   r_ohm_per_km= line['r_ohm_per_km'][m],
                                   x_ohm_per_km= line['x_ohm_per_km'][m],
                                   c_nf_per_km= line['c_nf_per_km'][m],
                                   g_us_per_km= line['g_us_per_km'][m],
                                   max_i_ka= line['max_i_ka'][m], 
                                   in_service = True)
    
    pp.create_line_from_parameters(net, from_bus= len(net.bus) - 1, 
                                   to_bus= PARAprim[i] ,
                                   length_km= 1-comprimento,
                                   r_ohm_per_km= line['r_ohm_per_km'][m],
                                   x_ohm_per_km= line['x_ohm_per_km'][m],
                                   c_nf_per_km= line['c_nf_per_km'][m],
                                   g_us_per_km= line['g_us_per_km'][m],
                                   max_i_ka= line['max_i_ka'][m], 
                                   in_service = True)


   
def limpa_memoria(net):
    "Eliminando as linhas inseridas e limpando a memória"

    net = rede(filename)
    
    return net
    
def ID_barras():
    "Realiza as configuracoes das barras DE e PARA"
    
    RELE_PRIMARIO, RELE_SECUNDARIO, DEprim, PARAprim, DEsec, PARAsec = rs.pares_rele() 
    
    DEprim = np.array(DEprim) - 1
    
    PARAprim = np.array(PARAprim) - 1
    
    DEsec = np.array(DEsec) - 1
    
    PARAsec = np.array(PARAsec) - 1
    
    return RELE_PRIMARIO, RELE_SECUNDARIO, DEprim, PARAprim, DEsec, PARAsec


def short_circuit_inter(net, line, tipo_cc,len1):
    "Aplica o curto-circuito close-in"
    
    #tipo_cc = "1ph" ou "2ph" ou "3ph"
    
    #Váriaveis para armazenar o curto
    rp = []   #corrente cc rele primario

    rs =[]    #corrente cc rele secundario
    
    r1 = []   #curto aplicado no primeiro rele do sistema
    
    #Inserindo o ID de cada barra 
    RELE_PRIMARIO, RELE_SECUNDARIO, DEprim, PARAprim, DEsec, PARAsec = ID_barras()
    
    #Curto-circuito para os outros reles    
    for i in range(len(DEprim)):
        ####Condicao para protecao principal     
        if DEprim[i] in net.line.from_bus.tolist():
                                       
            m = 0
            for m in range(len(net.line)):
                if DEprim[i] == net.line.from_bus[m] and \
                    PARAprim[i] == net.line.to_bus[m]: 
                    break
                     
            #Insere a barra ficticia no sistema
            barras_fic(net,line, bus, m, len1)
            
            #Insere a linha ficticia no sistema
            line_fic(net,DEprim, PARAprim, i, m, len1)      
            
            #Exclui a linha original - temporariamente  
            net.line.drop(index=m, inplace=True)
            
            #Calcula o curto-circuito
            sc.calc_sc(net,bus=(len(net.line)+2), ip=True, fault= tipo_cc, \
                       ith=True, branch_results=True)
            
            #Armazena o resultado da corrente de curto-circuito
            a = net.line[(net.line['from_bus'] == DEprim[i]) & \
                         (net.line['to_bus'] == (len(net.line)+2))].index.tolist()
            rp.append(net.res_line_sc.ikss_ka.iloc[a[0]-1].tolist())
               
            #Condicao 1 - rele primario (insere-se barras e linhas ficticias)          
            
        if DEprim[i] not in net.line.from_bus.tolist():
            #Calcula o curto-circuito
            sc.calc_sc(net,bus= DEprim[i], ip=True, fault= tipo_cc, ith=True,\
                       branch_results=True)
            
            #Armazena o resultado da corrente de curto-circuito
            a = net.res_bus_sc.ikss_ka.tolist()
            rp.append(a[0])
            
            #Condicao 2 - rele primario (o curto ocorre na barra onde 
            #rele esta localizado)
        

        ###FIM condicao protecao principal

        ###Condicao para protecao retaguarda
             
        if DEsec[i] in net.line.from_bus.tolist():
            #Armazena a corrente vista pelo rele secundario se ele estiver 
            #localizado em uma linha
            
            b = net.line[(net.line['from_bus'] == DEsec[i]) & \
                         (net.line['to_bus'] == PARAsec[i])].index.tolist()
            rs.append(net.res_line_sc.ikss_ka.iloc[b[0]].tolist())
            
            #Condicao 1 - rele retaguarda
            
        if DEsec[i] in net.trafo.hv_bus.tolist():
            #Armazena a corrente vista pelo secundario se ele estiver 
            #localizado em um trafo
            
            b = net.trafo[(net.trafo['hv_bus'] == DEsec[i]) & \
                          (net.trafo['lv_bus'] == PARAsec[i])].index.tolist()
            rs.append(net.res_trafo_sc.ikss_hv_ka.iloc[b[0]].tolist())
            
            #Condicao 2 - rele retaguarda
        
        ###FIM condicao protecao retaguarda
        
        #Chama-se funcao rede() com intuito de limpar os dataframes do 
        #sistema para novos curtos    
        net = rede(filename)
    
    #Condicao rele 1
    #ID do rele 1
    
    Dpri = DEsec[0]
    
    Ppri = PARAsec[0]
    
    comprimento = len1/100
    
    if Dpri in net.line.from_bus.tolist():
        f = 0
        for f in range(len(net.line)):
            if Dpri == net.line.from_bus[f] and \
                Ppri == net.line.to_bus[f]: 
                break
    
        #Local onde será aplicado o curto
        porcentagem = 1 - len1/100
        
        #Calculando a tensão em cada barra ficticia
        V_BF = ((np.array(bus['vn_kv'][Ppri]) - np.array(bus['vn_kv'][Dpri]))* porcentagem)  + np.array(bus['vn_kv'][Dpri])
        
        #Insere a linha ficticia
        pp.create_bus(net, name='b1000', vn_kv=V_BF, type='b') 
        pp.create_line_from_parameters(net, from_bus= Dpri, 
                                       to_bus= len(net.bus) - 1 ,
                                       length_km= comprimento,
                                       r_ohm_per_km= line['r_ohm_per_km'][f],
                                       x_ohm_per_km= line['x_ohm_per_km'][f],
                                       c_nf_per_km= line['c_nf_per_km'][f],
                                       g_us_per_km= line['g_us_per_km'][f],
                                       max_i_ka= line['max_i_ka'][f], 
                                       in_service = True)
        
        pp.create_line_from_parameters(net, from_bus= len(net.bus) - 1, 
                                       to_bus= Ppri ,
                                       length_km= 1-comprimento,
                                       r_ohm_per_km= line['r_ohm_per_km'][f],
                                       x_ohm_per_km= line['x_ohm_per_km'][f],
                                       c_nf_per_km= line['c_nf_per_km'][f],
                                       g_us_per_km= line['g_us_per_km'][f],
                                       max_i_ka= line['max_i_ka'][f], 
                                       in_service = True)
        
        
        
        #Exclui a linha original - temporariamente  
        net.line.drop(index=f, inplace=True)
        
        #Calcula o curto-circuito
        sc.calc_sc(net,bus=(len(net.line)+2), ip=True, fault= tipo_cc, \
                   ith=True, branch_results=True)
        
        #Armazena o resultado da corrente de curto-circuito
        a = net.line[(net.line['from_bus'] == Dpri) & \
                     (net.line['to_bus'] == (len(net.line)+2))].index.tolist()
        r1.append(net.res_line_sc.ikss_ka.iloc[a[0]-1].tolist())
        
    else:
        
        #FIM condicao rele 1
        #Calcula o curto-circuito
        sc.calc_sc(net,bus= Dpri, ip=True, fault= tipo_cc, ith=True,\
                   branch_results=True)
        
        #Armazena o resultado da corrente de curto-circuito
        a = net.res_bus_sc.ikss_ka.tolist()
        r1.append(a[0])
    
    #FIM condicao rele 1
    
    #Retornando ao sistema original
    limpa_memoria(net)
    
    #Organizar as correntes
    rp.insert(0,r1[0])
    
    #Fim de curto para outros reles
    return rp, rs


def power_flow(net):
    "Calcular o fluxo de potência do sistema"
    pp.runpp(net, calculate_voltage_angles=True, init="dc")
    
    return net.res_bus, net.res_load, net.res_shunt, net.res_ext_grid, \
        net.res_trafo, net.res_line 


def valor_k(net,rp, rs,DEprim, PARAprim, DEsec, PARAsec, RELE_SECUNDARIO, tipoCurva):
    "Determinar o coeficiente k"
    
    ip = []  #Armazena a corrente de pickup 
    
    #Converter para lista e adicionar R1
    deprim = DEprim.tolist()
    paraprim = PARAprim.tolist()
    desec = DEsec.tolist()
    parasec = PARAsec.tolist()
    
    #Adicionando no vetor que será trabalhado
    deprim.insert(0,desec[0])
    paraprim.insert(0,parasec[0])
    
    #Lógica para obter a corrente de pickup
    for i in range(len(deprim)):
        
                   
        if deprim[i] in net.line.from_bus.tolist():
                                       
            n = 0
            for n in range(len(net.line)):
                if deprim[i] == net.line.from_bus[n] and \
                    paraprim[i] == net.line.to_bus[n]: 
                    break
            
            p = net.line[(net.line['from_bus'] == deprim[i]) & \
                        (net.line['to_bus'] == paraprim[i])].index.tolist()
                          
            ip.append(net.res_line.i_from_ka.iloc[p[0]].tolist()) 
            
            print("linha")
            
        if deprim[i] not in net.line.from_bus.tolist():
            
            if paraprim[i] == 9997:
                
                if deprim[i] in net.shunt.bus.tolist():
                    
                    v_bus = net.res_bus.vm_pu[deprim[i]]
                    va_bus = net.res_bus.va_degree[deprim[i]]
                    
                    #Converter da forma polar para retangular
                    va =  x = v_bus*np.exp(1j*np.deg2rad(va_bus))
                                          
                    #Determina o index das que estao conectadas nas barras
                    h = net.shunt[net.shunt['bus'] == deprim[i]].index
                                
                    #Armazena as potencias
                    Pmw = net.res_shunt.p_mw[h[0]]
                    
                    Qmvar = net.res_shunt.q_mvar[h[0]]
                    
                    #Converte para array    
                    pmw = np.array(Pmw)
                     
                    qmvar = np.array(Qmvar)
                    
                    #Calcula a potencia aparente             
                    S = np.sqrt(pmw**2 + qmvar**2)
                                    
                    #Deleta as cargas temporariamente
                    net.shunt.drop(index=h[0], inplace=True)
                    net.res_shunt.drop(index=h[0], inplace=True)
                    
                    #Calcula a corrente 
                    I = abs(np.conj(S/va))
                    
                    #Armazena a corrente 
                    ip.append(I)
                    
                    print("shunt")
                    
                if deprim[i] in net.load.bus.tolist():
                    v_bus = net.res_bus.vm_pu[deprim[i]]
                    va_bus = net.res_bus.va_degree[deprim[i]]
                    
                    #Converter da forma polar para retangular
                    va =  x = v_bus*np.exp(1j*np.deg2rad(va_bus))
                                          
                    #Determina o index das que estao conectadas nas barras
                    h = net.load[net.load['bus'] == deprim[i]].index
                                
                    #Armazena as potencias
                    Pmw = net.res_load.p_mw[h[0]]
                    
                    Qmvar = net.res_load.q_mvar[h[0]]
                    
                    #Converte para array    
                    pmw = np.array(Pmw)
                     
                    qmvar = np.array(Qmvar)
                    
                    #Calcula a potencia aparente             
                    S = np.sqrt(pmw**2 + qmvar**2)
                                    
                    #Deleta as cargas temporariamente
                    net.load.drop(index=h[0], inplace=True)
                    net.res_load.drop(index=h[0], inplace=True)
                    
                    #Calcula a corrente 
                    I = abs(np.conj(S/va))
                    
                    #Armazena a corrente 
                    ip.append(I)
                    
                    print("load")
                      
            else:
                
                if deprim[i] in net.trafo.hv_bus.tolist():
                                
                    p = net.trafo[(net.trafo['hv_bus'] == deprim[i]) & \
                                  (net.trafo['lv_bus'] == paraprim[i])].index.tolist()
                        
                    ip.append(net.res_trafo.i_hv_ka.iloc[p[0]].tolist())
                    
                    print("trafo")
    
    Ipickup = 1.2 * np.array(ip)
    #Fim da logica
    
    
    #Rele secundario
    releSec = np.array(RELE_SECUNDARIO) - 1
    
    Ipickup1 = []
    for c in releSec:
        r = Ipickup[c]
        Ipickup1.append(r)
    
    
    
    #Armazenando os resultados
    RP = np.array(rp)
    RS = np.array(rs)
    
    beta = 0.14
    alpha = 0.02
    
    #Determinando o Kp e Ks --> beta/((RP ou RS/Ipickup) ** alpha) - 1
  
    if tipoCurva == "Curva: Inversa Padrão":
        
        #"Curva: Inversa Padrão"
        beta = 0.14
        alpha = 0.02
        
        #Constante kp --> rele primario
        kp= beta / (((rp/Ipickup) **(alpha)) -1 )
        
        #Constante ks --> rele retaguarda
        ks= beta / (((rs/np.array(Ipickup1)) **(alpha)) -1 )
        
    if tipoCurva == "Curva: Inversa de Tempo Curto":
        #"Curva: Inversa de Tempo Curto "
        beta = 0.05
        alpha = 0.04
         
        #Constante kp --> rele primario
        kp= beta / (((rp/Ipickup) **(alpha)) -1 )
         
        #Constante ks --> rele retaguarda
                  
        ks= beta / (((rs/np.array(Ipickup1)) **(alpha)) -1 )
         
    if tipoCurva == "Curva: Muito Inversa":
        #"Curva: Muito inversa"
        beta = 13.5
        alpha = 1
            
        #Constante kp --> rele primario
        kp= beta / (((rp/Ipickup) **(alpha)) -1 )
            
        #Constante ks --> rele retaguarda
         
        ks= beta / (((rs/np.array(Ipickup1)) **(alpha)) -1 )
        
    if tipoCurva == "Curva: Extremamente Inversa":
        #"Curva: Extremamente Inversa"
        beta = 80
        alpha = 2
        
        #Constante kp --> rele primario
        kp= beta / (((rp/Ipickup) **(alpha)) -1 )
        
        #Constante ks --> rele retaguarda
        
        ks= beta / (((rs/np.array(Ipickup1)) **(alpha)) -1 )
        
    if tipoCurva == "Curva: Inversa de Tempo Longo":
        #"Curva: Inversa de Tempo Longo"
        beta = 120
        alpha = 1
        
        #Constante kp --> rele primario
        kp= beta / (((rp/Ipickup) **(alpha)) -1 )
        
        #Constante ks --> rele retaguarda
        
        ks= beta / (((rs/np.array(Ipickup1)) **(alpha)) -1 )
        
    
    return kp,ks
    
def funcao_otimizacao(net, kp, ks, RELE_PRIMARIO, RELE_SECUNDARIO):
    "Otimizar a funcao objetiva"
    
    #Salvando os elementos
    Kp = kp.tolist()
    Ks = ks.tolist()
    RP = np.array(RELE_PRIMARIO) - 1
    RS = np.array(RELE_SECUNDARIO) - 1
    
    #Definindo a funcao objetiva
    f = deepcopy(kp)
    del Kp[0]
    
    #Definindo a dimensao da matriz
    N = range(len(f))
    M = range(len(f)-1)
    
    model = ConcreteModel()

    model.x = pyo.Var(N, within=Reals, bounds=(0.05,np.inf))

    def obj_rule(model):
        return sum(f[i]*model.x[i] for i in N)

    model.obj = pyo.Objective(rule=obj_rule)


    def con_rule(model,m):
            
        const = Ks[m] * model.x[RS[m]] - Kp[m] * model.x[RP[m]] >=0.2
           
        return const

    model.con = pyo.Constraint(M, rule = con_rule)



    tempo_inicial = time.time()
    opt = SolverFactory('glpk')
    opt.solve(model).write()
    tempo = time.time() - tempo_inicial
    
    TMS = []
    for i in N:
        s= (pyo.value(model.x[i]))
        TMS.append(s)

    

    #Exibe os resultados detalhados
    model.pprint()
    
    
   
  
    
    
    
    return TMS

    
        
    

#Chamando as funções

net = rede(filename)


bus, load, gen, shunt, ext_grid, line, trafo = conversao(net)




RELE_PRIMARIO, RELE_SECUNDARIO, DEprim, PARAprim, DEsec, PARAsec = ID_barras()

rp, rs = short_circuit_inter(net,line, "3ph",1)

net = limpa_memoria(net)

power_flow(net)

kp, ks = valor_k(net, rp, rs,DEprim, PARAprim, DEsec, PARAsec, RELE_SECUNDARIO, "Curva: Inversa Padrão")

TMS = funcao_otimizacao(net, kp, ks, RELE_PRIMARIO,RELE_SECUNDARIO)


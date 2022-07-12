"""
@Autor: Prof. Wellington Maycon S. Bernardes (UFU / FEELT)

Essa função determina os pares de relés primário e secundário conforme a topologia
do sistema elétrico.

Criado em: 03 Jun. 2021
Última atualização: 28 Jan. 2022
"""
import numpy as np
import pandas as pd

def pares_rele():
    file = 'Excel' #OU: file = 'txt'
    ERRO = 0
    
    arquivo_sistema_eletr = ""  
    
    
    if file == "txt":
        # Carregando BASE_RELES.txt
        # https://www.w3schools.com/python/python_file_open.asp
        nome_arquivo = 'breles.txt'
        nreles = 0 # Numero de reles
        dreles = 0 # Flag que sinaliza que DRELES foi encontrado
        inicio_dreles = 0 # Linha onde inicia os dados dos reles no txt
        i_linha_txt = 0 # Posicao da linha lida
        rele_txt = [] # Armazena cada linha lida (relés) na integra
        f = open(nome_arquivo, 'r')
        for line in f:
            print(line)
            i_linha_txt += 1
            if line[0:6]=="DRELES":
                while(1):
                    dreles = 1
                    line = f.readline(); i_linha_txt+=1;
                    print(line)
                    if line[0:5]=="99999":
                        dreles = 0
                        break
                    else:
                        if line[0:1]=="(":
                            continue
                        else:
                            if inicio_dreles==0:
                                inicio_dreles=i_linha_txt;
                            # FIM IF
                            # Empilha linha de DRELES em rele_txt
                            rele_txt.append(line)
                            nreles+=1
                        # FIM IF
                    # FM IF
                # FIM WHILE
            # FIM IF
            if line[0:1]=="(":
                continue
            # FIM IF
        # FIM FOR
    
        # Fechando arquivo - economia de buffer / memória
        f.close()
          
        # Inicializando estrutura de reles
        IDReles = np.full(nreles,0)
        DEReles = np.full(nreles,0)
        PARAReles = np.full(nreles,0)
        NCReles = np.full(nreles,1)
        # Deve reservar espaço, senão não armazena todos os valores
        NOMEReles = np.full(nreles,"               ")
        RTC1Reles = np.full(nreles,100)
        RTC2Reles = np.full(nreles,5)
    
        print("Separando dados de reles...")
        
        for i in range(nreles):  # De 0 até nreles-1
            # IDReles
            if len(rele_txt[i]) > 4 and rele_txt[i][0:5] != "     ": #5
                IDReles[i] = int(rele_txt[i][0:5])
            # DEReles
            if len(rele_txt[i]) > 10 and rele_txt[i][6:11] != "     ": #5
                DEReles[i] = int(rele_txt[i][6:11])
            # PARAReles
            if len(rele_txt[i]) > 16 and rele_txt[i][12:17] != "     ": #5
                PARAReles[i] = int(rele_txt[i][12:17])
            # NCReles
            if len(rele_txt[i]) > 19 and rele_txt[i][18:20] != "  ": #2
                NCReles[i] = int(rele_txt[i][18:20])
            # NOMEReles
            if len(rele_txt[i]) > 35 and rele_txt[i][21:36] != "               ": #15
                NOMEReles[i] = rele_txt[i][21:36]
            #RTC1Reles
            if len(rele_txt[i]) > 41 and rele_txt[i][37:42] != "     ": #5
                RTC1Reles[i] = int(rele_txt[i][37:42])
            #RTC2Reles
            if len(rele_txt[i]) > 43 and rele_txt[i][43:44] != " ": #1
                RTC2Reles[i] = int(rele_txt[i][43:44])
        # FIM FOR
    # FIM IF (Arquivo .txt)
    
    if file == 'Excel':
        # Carregando BASE_RELES.xlsx
        nome_arquivo = 'breles.xlsx'
        df = pd.read_excel(nome_arquivo,sheet_name= "Pares")
        IDReles = df["N"].to_numpy()
        DEReles = df["DE"].to_numpy()
        PARAReles = df["PARA"].to_numpy()
        NCReles = df["NC"].to_numpy()
        NOMEReles = df["NOME"].to_numpy()
        RTC1Reles = df["RTC1"].to_numpy()
        RTC2Reles = df["RTC2"].to_numpy()
        arquivo_sistema_eletr = df["FILE"][0]
        nreles = len(IDReles)
        
        IDReles[np.isnan(IDReles)] = 0
        DEReles[np.isnan(DEReles)] = 0
        PARAReles[np.isnan(PARAReles)] = 0
        NCReles[np.isnan(NCReles)] = 1
        RTC1Reles[np.isnan(RTC1Reles)] = 100
        RTC2Reles[np.isnan(RTC1Reles)] = 5
    
    print("")
    
    print("Encontrando todas as barras do sistema no arquivo Anafas...")
    
    if file == "txt":
        f = open(nome_arquivo, 'r')
        for line in f:
            print(line)
            if line[0:4] == "FILE":
                arquivo_sistema_eletr = f.readline().splitlines()[0];
                break
            # FIM IF
        # FIM FOR
        f.close()
    
    dbar = 0 #Flag para dados de barra
    nb = 0 # Número de barras
    inicio_dbar = 0
    
    barra_txt = [] # Armazena cada barra lida na íntegra
    i_linha_txt = 0
    
    
    print("Encontrando estrutura de barras...")
    df = pd.read_excel(arquivo_sistema_eletr,sheet_name= "Barras")
    B_NumFic = df["Unnamed: 0"].to_numpy()
    nb = len(B_NumFic)
    B_Nome = df["name"].to_numpy()
    B_NumReal = B_NumFic + 1
    
    # Adicionado potencial terra
    B_NumReal = np.insert(B_NumReal, nb, 9998)
    B_NumFic = np.insert(B_NumFic, nb, nb)
    nb = nb+1
    
    if len(B_NumReal) == 0:
        print("Inexistência de barras na rede. Corrija o problema e execute\
              novamente...")
        
    

    
    

    
    print("Determinação dos pares de relés primários e secundários")
    # Matriz NB x NRELES para armazenar +1, -1 e 0.
    matriz_barras_reles = np.zeros((nb,nreles))
    # Variáveis para armazenar valores de barras de relés primários e secundários
    # encontrados
    RELE_PRIMARIO = []
    RELE_SECUNDARIO = []
    PRP = []
    PRS = []
    
    for j in range(nreles):  
        pos_1 = np.where(B_NumReal == DEReles[j])[0][0]    
        matriz_barras_reles[pos_1][j] = 1
        pos_2 = np.where(B_NumReal == PARAReles[j])[0][0]
        matriz_barras_reles[pos_2][j] = -1
    # FIM FOR
    
    for j in range(nreles):
        for i in range(nb):
            if matriz_barras_reles[i][j] == 1:
                for k in range(nreles):
                    if (DEReles[j] == DEReles[k] and PARAReles[j] == PARAReles[k]\
                        and NCReles[j]==NCReles[k]):
                        # Pares de relés primários e secundários não podem pertencer
                        # a mesma linha.
                        continue
                    # FIM IF
                    if (PARAReles[j] == DEReles[k] and DEReles[j] == PARAReles[k]\
                        and NCReles[j] == NCReles[k]):
                        # Pares de relés primários e secundários não podem pertencer
                        # a mesma linha.
                        continue
                    # FIM IF
                    if (matriz_barras_reles[i][k] == -1):
                        # Armazenando pares de relés
                        RELE_PRIMARIO.append(IDReles[j]); # RELE_PRIMARIO.append(B_NumReal[j]);
                        RELE_SECUNDARIO.append(IDReles[k]); # RELE_SECUNDARIO.append(B_NumReal[k]);
                        PRP.append(j);
                        PRS.append(k);
                    # FIM IF
                # FIM FOR
            # FIM IF
        # FIM FOR
    # FIM FOR
    
    #Armazenando os valores da barra DE e PARA rele principal
    DEprim = []
    
    for k in range(len(RELE_PRIMARIO)):
        pos = DEReles[PRP[k]]
        DEprim.append(pos)
        
    PARAprim = []
    
    for h in range(len(RELE_PRIMARIO)):
        pos1 = PARAReles[PRP[h]]
        PARAprim.append(pos1)
    # FIM armazenamento
    
    #Armazenando os valores da barra DE e PARA rele retaguarda
    DEsec = []
    
    for o in range(len(RELE_PRIMARIO)):
        pos2 = DEReles[PRS[o]]
        DEsec.append(pos2)
        
    PARAsec = []
    
    for y in range(len(RELE_PRIMARIO)):
        pos3 = PARAReles[PRS[y]]
        PARAsec.append(pos3)
    # FIM armazenamento
        
    
    """# Relatorio de reles primarios e secundarios - terminal
    print("\n")
    print("Relatório de relés primários e secundários")
    print("ARQUIVO: ", arquivo_sistema_eletr)
    print("\n")
    print("Atenção: A coordenação proposta é uma sugestão calculada pelo programa")
    print("         que pode ser alterada ou acrescentada conforme a necessidade ")
    print("         do usuário. Nesta etapa, o programa entende que cada relé ")
    print("         protege primariamente SOMENTE a linha onde está alocado")
    print("         (barra DE, barra PARA)")
    print(" ")
    print("         Ainda, as barras de derivação ou fictícias nos circuitos podem")
    print("         prejudicar o cálculo dos relés secundários. Assim, evite o")
    print("         emprego dessas barras")
    print(" ")
    print("********************************************************************")
    print("                 Universidade Federal de Uberlândia                 ")
    print("                  Faculdade de Engenharia Elétrica                  ")
    print("                                                                    ")
    print("********************************************************************")
    print("  R E S U M O   D O S   R E L É S   P R I M Á R I O S   E   S E C.  ")
    print("        RELE PRIMARIO          --XX--        RELE SECUNDARIO        ")
    print("N.    DE      PARA  NC    DE   --XX-- N.    DE      PARA  NC     DE ")
    print("********************************************************************"
    for i in range(len(RELE_PRIMARIO)):
        print(str(RELE_PRIMARIO[i]).rjust(2), " ", str(DEReles[PRP[i]]).rjust(3), " ",\
              str(PARAReles[PRP[i]]).rjust(7), " ", str(NCReles[PRP[i]]).rjust(1), " ", str(DEReles[PRP[i]]).rjust(3),\
              "  --XX--",\
              str(RELE_SECUNDARIO[i]).rjust(2), " ", str(DEReles[PRS[i]]).rjust(3), " ",\
              str(PARAReles[PRS[i]]).rjust(7), " ", str(NCReles[PRS[i]]).rjust(1), " ", str(DEReles[PRS[i]]).rjust(4))
    print("********************************************************************")
    
    # Relatorio de reles primarios e secundarios - arquivo de texto
    f = open("RELE_PRIMARIO_SECUNDARIO.txt","w") # Cria um novo arquivo
    f.write("\n")
    f.write("Relatório de relés primários e secundários\n")
    f.write("ARQUIVO: " + arquivo_sistema_eletr + "\n")
    f.write("\n")
    f.write("Atenção: A coordenação proposta é uma sugestão calculada pelo programa\n")
    f.write("         que pode ser alterada ou acrescentada conforme a necessidade \n")
    f.write("         do usuário. Nesta etapa, o programa entende que cada relé \n")
    f.write("         protege primariamente SOMENTE a linha onde está alocado\n")
    f.write("         (barra DE, barra PARA)\n")
    f.write(" ")
    f.write("         Ainda, as barras de derivação ou fictícias nos circuitos podem\n")
    f.write("         prejudicar o cálculo dos relés secundários. Assim, evite o\n")
    f.write("         emprego dessas barras\n")
    f.write(" ")
    f.write("********************************************************************\n")
    f.write("                 Universidade Federal de Uberlândia                 \n")
    f.write("                  Faculdade de Engenharia Elétrica                  \n")
    f.write("                                                                    \n")
    f.write("********************************************************************\n")
    f.write("  R E S U M O   D O S   R E L É S   P R I M Á R I O S   E   S E C.  \n")
    f.write("        RELE PRIMARIO          --XX--        RELE SECUNDARIO        \n")
    f.write("N.    DE      PARA  NC    DE   --XX-- N.    DE      PARA  NC     DE \n")
    f.write("********************************************************************\n")
    for i in range(len(RELE_PRIMARIO)):
        f.write(str(RELE_PRIMARIO[i]).rjust(2) + " " + str(DEReles[PRP[i]]).rjust(5) + "   " +\
              str(PARAReles[PRP[i]]).rjust(7) + "  " + str(NCReles[PRP[i]]).rjust(2) + " " + str(DEReles[PRP[i]]).rjust(5) +\
              "   --XX-- "+\
              str(RELE_SECUNDARIO[i]).rjust(2)+ "   " + str(DEReles[PRS[i]]).rjust(3) + "    "+\
              str(PARAReles[PRS[i]]).rjust(6) + "  "+ str(NCReles[PRS[i]]).rjust(2) + "  "+ str(DEReles[PRS[i]]).rjust(5) + "\n")
    f.write("********************************************************************\n")
    f.close()"""
    
    return RELE_PRIMARIO, RELE_SECUNDARIO, DEprim, PARAprim, DEsec, PARAsec 

if __name__ == "__main__":
    pares_rele()
    print("Código executado com sucesso...")
# FIM IF
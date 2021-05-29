import tkinter as tk
import fitz
from tkinter.filedialog import askopenfile,askdirectory

#Criação da janela
janela= tk.Tk()
janela.title('Extrator de imagens PDF - Edson Freitas - "Freijoto" ')
tela = tk.Canvas(janela,width=600, height=300)
tela.grid(columnspan=3,rowspan=3)
#Label de instrução
lbExplicacao = tk.Label(janela,text='Escolha um pdf')
lbExplicacao.grid(columnspan=3, column=0,row=0)

#Rotina de busca do Arquivo PDF na maquina
def EscolherArquivo():
    lbEscolher.set('Carregando')
    arquivo= askopenfile(parent=janela,mode='rb',title='Selecione o arquivo',filetypes=[('Pdf file','*.pdf')])
    
    if arquivo:
        lbEscolher.set('Extraindo Imagens')
        Extrair_Imagens(arquivo)
        lbEscolher.set('Concluído')
#Rotina Que varre o PDF em busca das imagens para salvar
def Extrair_Imagens(arquivo):
    #arquivo= Variável que recebe o Caminho do PDF a ter suas imagens extraídas)
    if arquivo:
        doc = fitz.open(arquivo)
        for i in range(len(doc)):
            for img in doc.getPageImageList(i):
                try:
                    xref = img[0]   #Arquivo de imagem
                    smask = img[1]  #Camada de transparencia
                    pix1 = fitz.Pixmap(doc, xref)    #Definindo o mapeamento da imagem
                    pix2 = fitz.Pixmap(doc, smask)   #Definindo o mapeamento da transparencia
                    pix = fitz.Pixmap(pix1)          #Carregando a Imagem em um objeto que ira consolidar Imagem e transparencia 
                    pix.set_alpha(pix2.samples)      #Aplicando camada de transparencia
                    if pix.n < 5:       #Verificando o tipo, caso seja maior que 5 é nessário converter para RGB
                        pix.writePNG('p%s-%s.png' % (i, xref)) #Salvando o Arquivo
                    else:               
                        pix1 = fitz.Pixmap(fitz.csRGB, pix)     #Convertendo em RGB
                        pix1.writePNG('p%s-%s.png'% (i, xref))  #Salvando o Arquivo
                        pix1 = None
                        pix = None
                except Exception: #Ignorando possíveis erros caso a pagina em analise não possua imagens para serem extraídas
                    pass

#Definições de tela
lbEscolher = tk.StringVar()
btnEscolher = tk.Button(janela,textvariable=lbEscolher,command=lambda:EscolherArquivo())
lbEscolher.set('Selecione')
btnEscolher.grid(column=1, row=1)


def start():
    janela.mainloop()

if __name__ =='__main__':
    start()
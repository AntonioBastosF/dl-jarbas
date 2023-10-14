import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import os
import webbrowser
import requests

# Substitua 'sua_chave_de_api' pela chave que você obteve
api_key = 'def427c541b44440a154246b063f3527'

# URL da API de previsão do tempo em português
url = "http://wttr.in/SaoPaulo?format=%C+%t&lang=pt"

# Inicializa o reconhecedor de voz e o mecanismo de síntese de voz
reconhecedor = sr.Recognizer()
robo = pyttsx3.init()

# Configuração da voz do robô
robo.setProperty('rate', 155)
robo.setProperty('volume', 0.8)

# Variável para controlar o estado do programa
esperando_comando = False


# Função com lista de comandos
def menu():
    print("Aguardando comando de voz...",
          "\n1- Criar evento na agenda ", " 2- Ler agenda",
          "\n3- Diga uma verdade",
          "\n4- Texto para áudio", "\  5- Pesquisa no Google",
          "\n6- Pesquisa de imagem no Google",
          "\n7- Ver Notícias",
          "\n8- Qual é o meu signo",
          "\n9- Previsão do tempo"
          "\n10- Encerrar")


# Função para determinar o signo com base na data de nascimento
def determinar_signo(data_nascimento):
    # Lógica para determinar o signo com base na data de nascimento
    dia, mes = data_nascimento.split('/')
    dia, mes = int(dia), int(mes)

    if (mes == 3 and 21 <= dia <= 31) or (mes == 4 and 1 <= dia <= 19):
        return "Áries"
    elif (mes == 4 and 20 <= dia <= 30) or (mes == 5 and 1 <= dia <= 20):
        return "Touro"
    elif (mes == 5 and 21 <= dia <= 31) or (mes == 6 and 1 <= dia <= 20):
        return "Gêmeos"
    elif (mes == 6 and 21 <= dia <= 30) or (mes == 7 and 1 <= dia <= 22):
        return "Câncer"
    elif (mes == 7 and 23 <= dia <= 31) or (mes == 8 and 1 <= dia <= 22):
        return "Leão"
    elif (mes == 8 and 23 <= dia <= 31) or (mes == 9 and 1 <= dia <= 22):
        return "Virgem"
    elif (mes == 9 and 23 <= dia <= 30) or (mes == 10 and 1 <= dia <= 22):
        return "Libra"
    elif (mes == 10 and 23 <= dia <= 31) or (mes == 11 and 1 <= dia <= 21):
        return "Escorpião"
    elif (mes == 11 and 22 <= dia <= 30) or (mes == 12 and 1 <= dia <= 21):
        return "Sagitário"
    elif (mes == 12 and 22 <= dia <= 31) or (mes == 1 and 1 <= dia <= 19):
        return "Capricórnio"
    elif (mes == 1 and 20 <= dia <= 31) or (mes == 2 and 1 <= dia <= 18):
        return "Aquário"
    elif (mes == 2 and 19 <= dia <= 29) or (mes == 3 and 1 <= dia <= 20):
        return "Peixes"
    else:
        return "Signo não identificado"


# Função para exibir a previsão do tempo em São Paulo
def exibir_previsao_do_tempo():
    response = requests.get(url)
    previsao_tempo = response.text
    print("Previsão do tempo para São Paulo:")
    print(previsao_tempo)


# Função para ler a agenda em voz
def ler_agenda_em_voz():
    if os.path.isfile("agenda.txt"):
        with open("agenda.txt", "r") as agenda:
            eventos = agenda.readlines()
            if eventos:
                texto_agenda = '\n'.join([evento.strip() for evento in eventos])
                tts = gTTS(text=texto_agenda, lang='pt-br')
                tts.save("agenda.mp3")
                os.system("start agenda.mp3")
                robo.say("Aqui está a sua agenda.")
                robo.runAndWait()
            else:
                robo.say("A agenda está vazia.")
                robo.runAndWait()
    else:
        robo.say("A agenda não foi encontrada.")
        robo.runAndWait()


# Função para fazer uma pesquisa no Google
def pesquisa_no_google():
    robo.say("Digite o que deseja procurar no Google.")
    robo.runAndWait()
    pesquisa = input()
    pesquisa = pesquisa.replace(" ", "+")
    url = f"https://www.google.com/search?q={pesquisa}"
    webbrowser.open(url)
    robo.say("Aqui estão os resultados da pesquisa no Google.")
    robo.runAndWait()


# Função para pesquisar imagens no Google
def pesquisa_imagem_no_google():
    robo.say("Digite o que deseja pesquisar no Google Images.")
    robo.runAndWait()
    pesquisa = input()
    pesquisa = pesquisa.replace(" ", "+")
    url = f"https://www.google.com/search?q={pesquisa}&tbm=isch"
    webbrowser.open(url)
    robo.say("Aqui estão os resultados da pesquisa de imagens no Google.")
    robo.runAndWait()


# Função para obter as principais manchetes
def obter_principais_manchetes():
    url = f'https://newsapi.org/v2/top-headlines?apiKey={api_key}&country=br'
    response = requests.get(url)
    data = response.json()
    manchetes = data.get('articles', [])

    if manchetes:
        print("Principais manchetes:")
        for i, noticia in enumerate(manchetes, 1):
            print(f"{i}. {noticia['title']}")

        # Pedir ao usuário para escolher um número
        escolha = int(input("Escolha um número para ver mais detalhes ou 0 para sair: "))
        if escolha == 0:
            return
        elif 1 <= escolha <= len(manchetes):
            noticia_selecionada = manchetes[escolha - 1]
            print("\nTítulo:", noticia_selecionada['title'])
            print("Fonte:", noticia_selecionada['source']['name'])
            print("Descrição:", noticia_selecionada['description'])
            print("URL:", noticia_selecionada['url'])

            # Abra a URL da notícia no navegador
            webbrowser.open(noticia_selecionada['url'])
        else:
            print("Escolha inválida.")


# Função para aguardar comandos de voz
def aguardar_comandos():
    global esperando_comando
    while True:
        with sr.Microphone() as source:
            if not esperando_comando:
                print("Diga olá Jarbas")
            try:
                audio = reconhecedor.listen(source, timeout=7)
            except sr.WaitTimeoutError:
                if esperando_comando:
                    print("Tempo limite de 5 segundos atingido. Sem resposta.")
                continue

        try:
            texto = reconhecedor.recognize_google(audio, language='pt-BR')
            print(f"Você disse: {texto}")

            if "olá jarbas" in texto.lower():
                resposta = "Jarbas na escuta, como posso ajudar?"
                robo.say(resposta)
                robo.runAndWait()
                menu()
                esperando_comando = True  # Aguardar novo comando
            elif esperando_comando:
                if "criar evento na agenda" in texto.lower():
                    robo.say("Ok, qual evento devo cadastrar?")
                    robo.runAndWait()
                    with sr.Microphone() as source:
                        try:
                            audio = reconhecedor.listen(source, timeout=5)
                            evento = reconhecedor.recognize_google(audio, language='pt-BR')
                            with open("agenda.txt", "a") as agenda:
                                agenda.write(evento + "\n")
                            robo.say(f"Evento '{evento}' cadastrado na agenda.")
                            robo.runAndWait()
                        except sr.WaitTimeoutError:
                            if esperando_comando:
                                print("Tempo limite de 5 segundos atingido. Sem resposta.")
                            continue
                    menu()
                elif "ler agenda" in texto.lower():
                    ler_agenda_em_voz()
                    menu()
                elif "diga uma verdade" in texto.lower():
                    verdade = "Palmeiras não tem mundial"
                    robo.say(verdade)
                    robo.runAndWait()
                elif "texto para áudio" in texto.lower():
                    robo.say("Digite o texto que deseja transformar em áudio e pressione Enter.")
                    robo.runAndWait()
                    texto_para_audio = input()
                    tts = gTTS(text=texto_para_audio, lang='pt-br')
                    tts.save("texto_para_audio.mp3")
                    os.system("start texto_para_audio.mp3")
                    menu()
                elif "pesquisa no google" in texto.lower():
                    pesquisa_no_google()
                    menu()
                elif "pesquisa de imagem no google" in texto.lower():
                    pesquisa_imagem_no_google()
                    menu()
                elif "ver notícias" in texto.lower():
                    obter_principais_manchetes()
                    menu()
                elif "signo" in texto.lower():
                    robo.say(
                        "Claro, eu posso ajudar com isso. Por favor, insira a data de nascimento no formato dd/mm.")
                    robo.runAndWait()
                    data_nascimento = input("Digite a data de nascimento (dd/mm): ")
                    signo = determinar_signo(data_nascimento)
                    if signo:
                        robo.say(f"Seu signo com base na data de nascimento {data_nascimento} é {signo}.")
                        robo.runAndWait()
                    else:
                        robo.say("Data de nascimento inválida.")
                        robo.runAndWait()
                elif "previsão do tempo" in texto.lower():
                    exibir_previsao_do_tempo()
                    menu()
                elif "encerrar" in texto.lower():
                    robo.say("Encerrando o programa. Até logo!")
                    robo.runAndWait()
                    exit()
        except sr.UnknownValueError:
            print("Não foi possível entender a fala.")
        except sr.RequestError as e:
            print(f"Erro na requisição ao serviço de reconhecimento de fala: {e}")


# Iniciar a escuta de comandos
aguardar_comandos()

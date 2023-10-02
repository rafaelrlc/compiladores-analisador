import re
import webbrowser
import time


# Definindo caminho do chrome
chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

# dicionário para mapear os nomes dos tokens com as expressões regulares
regex_tokens = {
    'LOOP': r'loop',
    'BROWSER': r'chrome|firefox|edge|safari',
    'LINK': r'https?://[^\s]+',
    # 'TEMPO': r'\d+',
    'TEMPO': r'15_min|20_min|1_hora|1_dia|2_dias|sem_limite',
    'ESPACO': r'\s+',
    'VEZES': r'1|2|3|4|5',
    'PV': r';'
}

temporizador = {
    '15_min': 15,  # *60,
    '20_min': 20 * 60,
    '1_hora': 60 * 60,
    '1_dia': 24 * 60 * 60,
    '2_dias': 2 * 24 * 60 * 60,
    'sem_limite': 999999
}


def lexer(codigo):
    tokens = []

    while codigo:
        match = False
        # print(codigo)
        for nome, regex in regex_tokens.items():
            resultado = re.match(regex, codigo)  # tenta encontrar um padrão no início da string
            # se encontrou
            if resultado:
                lexema = resultado.group()  # extrai o texto que corresponde ao token
                tokens.append((nome, lexema))
                codigo = codigo[len(lexema):]  # remove o lexema do código
                match = True  # marca que houve um reconhecimento
                break
        if not match:
            print('Lexema não reconhecido')
            lexemaErrado = codigo.split()
            raise Exception(
                f'Lexema não reconhecido: {lexemaErrado[0]}')  # lança uma exceção com a parte inválida do código
    return tokens


class NoComando:

    def __init__(self, browser, link, tempo):
        self.browser = browser
        self.link = link
        self.tempo = tempo

    def __str__(self) -> str:
        return self.browser + "," + str(self.link) + "," + self.tempo


def reconhece(tokens, lookahead, tipo):
    if lookahead >= len(tokens):
        return False

    return True if tokens[lookahead][0] == tipo and lookahead < len(tokens) else False


def tempo(tokens, lookahead, no):
    if reconhece(tokens, lookahead, 'TEMPO') and reconhece(tokens, lookahead + 1, 'PV'):
        return no

    return None


def link(tokens, lookahead, no):
    if reconhece(tokens, lookahead, 'LINK') and reconhece(tokens, lookahead + 1, 'ESPACO'):
        if tempo(tokens, lookahead + 2, no) is not None:
            no.tempo = tokens[lookahead + 2][1]
            return no
        else:
            raise Exception(f'Erro de sintaxe: {tokens[lookahead + 2]}')
    else:
        raise Exception(f'Erro de sintaxe: {tokens[lookahead]}')


def navegar(tokens, lookahead, no):
    if reconhece(tokens, lookahead, 'BROWSER') and reconhece(tokens, lookahead + 1, 'ESPACO'):
        if tempo(tokens, lookahead + 2, no):
            no.tempo = tokens[lookahead + 2][1]
            return no

        elif link(tokens, lookahead + 2, no):
            no.link = tokens[lookahead + 2][1]
            return no

        else:
            raise Exception(f'Erro de sintaxe: {tokens[lookahead]}')
    else:
        raise Exception(f'Erro de sintaxe: {tokens[lookahead]}')


def explore(tokens, lookahead, no):
    if navegar(tokens, lookahead, no):
        no.browser = tokens[lookahead][1]
        return no
    else:
        raise Exception(f'Erro de sintaxe: {tokens[lookahead]}')


def vezes(tokens, lookahead, no):
    if reconhece(tokens, lookahead, 'VEZES') and reconhece(tokens, lookahead + 1, 'ESPACO'):
        if explore(tokens, lookahead + 2, no):
            return no
    else:
        raise Exception(f'Erro de sintaxe: {tokens[lookahead]}')


def programa_sol(tokens, lookahead, no):
    if reconhece(tokens, lookahead, 'LOOP') and reconhece(tokens, lookahead + 1, 'ESPACO'):
        if vezes(tokens, lookahead + 2, no):
            return no
    else:
        raise Exception(f'Erro de sintaxe: {tokens[lookahead]}')


def parser(tokens):
    lookahead = 0
    no = NoComando(-1, -1, -1)

    # browser = -1      # Não sei se vai precisar ser usado
    # link = -1
    # tempo = -1

    if reconhece(tokens, lookahead, 'LOOP') and reconhece(tokens, lookahead + 1, 'ESPACO'):
        arvore = programa_sol(tokens, lookahead, no)
        return arvore

    print('\nSintaxe inválida\n')
    return None


def executar(arvore):
    # extrai os atributos do nó da árvore
    browser = arvore["browser"]
    #print(f'Browser: {browser}')

    link = "about:blank"
    if arvore["link"] != -1:
        link = arvore["link"]
    #print(f'Link: {link}')

    tempo = temporizador[arvore["tempo"]]
    #print(f'Tempo: {tempo}')

    # abre o navegador com o link especificado
    webbrowser.get(browser).open(link)

    # espera o tempo especificado em segundos
    time.sleep(tempo)

    # fecha o navegador
    #webbrowser.get(browser).close()

    return 'Programa executado com sucesso'

def main2(codigo):
    tokens = lexer(codigo)
    arvore = parser(tokens)
    browser  = arvore.browser
    link = arvore.link
    tempo = arvore.tempo
    return [tokens,browser,link,tempo]

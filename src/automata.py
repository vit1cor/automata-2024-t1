"""Implementação de autômatos finitos."""


def load_automata(filename):
    """
    Lê os dados de um autômato finito a partir de um arquivo.

    A estsrutura do arquivo deve ser:

    <lista de símbolos do alfabeto, separados por espaço (' ')>
    <lista de nomes de estados>
    <lista de nomes de estados finais>
    <nome do estado inicial>
    <lista de regras de transição, com "origem símbolo destino">

    Um exemplo de arquivo válido é:

    ```
    a b
    q0 q1 q2 q3
    q0 q3
    q0
    q0 a q1
    q0 b q2
    q1 a q0
    q1 b q3
    q2 a q3
    q2 b q0
    q3 a q1
    q3 b q2
    ```

    Caso o arquivo seja inválido uma exceção Exception é gerada.
    """
    if isinstance(filename, str):
        if not filename.endswith('.txt'):
            filename += '.txt'
        resposta = {}
    else:
        raise Exception('O tipo esperado para o nome do arquivo é string')

    try:
        with open(filename, "rt") as arquivo:
            linhas, regras = arquivo.readlines(), []
            resposta['simbolos'] = linhas[0].strip().split(' ')
            resposta['estados'] = linhas[1].strip().split(' ')
            possiveis_estados_finais, estados_finais = linhas[2].strip().split(' '), []
            for estado in possiveis_estados_finais:
                if estado in resposta['estados']:
                    estados_finais.append(estado)
                else:
                    raise Exception('Os estados finais devem estar presentes na descrição do autômato')
            resposta['estados_finais'] = estados_finais
            if linhas[3].strip() in resposta['estados']:
                resposta['estado_inicial'] = linhas[3].strip()
            else:
                raise Exception('O estado inicial não está presente na descrição do autômato')
            for linha in linhas[4:]:
                linha = linha.strip().split(' ')
                if len(linha) >= 3:
                    if linha[0] in resposta['estados'] and linha[2] in resposta['estados'] and linha[1] in resposta['simbolos']:
                        try:
                            regras.append(tuple(linha))
                        except ValueError:
                            raise Exception('O valor não pôde ser convertido para tupla e inserido nas regras do autômato')
                    else:
                        raise Exception('Os estados e símbolos devem estar presentes na descrição do autômato')
                else:
                    raise Exception('As regras de transição precisam de no mínimo 3 parâmetros')
            resposta['regras'] = regras
        return resposta
    except FileNotFoundError:
        raise Exception('O arquivo não foi encontrado no sistema')


def process(automata, words):
    """
    Processa a lista de palavras e retora o resultado.

    Os resultados válidos são ACEITA, REJEITA, INVALIDA.
    """
    if isinstance(automata, dict) and isinstance(words, list):
        for w in words:
            if not isinstance(w, str):
                raise Exception('As palavras devem ser do tipo string')
    else:
        raise Exception('O tipo esperado para o autômato é dict e para a palavra é list')
    try:
        simbolos = automata['simbolos']
        estados_finais = automata['estados_finais']
        estado_inicial = automata['estado_inicial']
        regras = automata['regras']
    except KeyError:
        raise Exception('O autômato não possui todos os campos esperados')

    resposta = []

    for word in words:
        container = None
        estado_atual = estado_inicial
        for char in word:
            if container:
                break
            if char not in simbolos:
                container = resposta.append((word, 'INVALIDA'))
                break
            for regra in regras:
                if regra[0] == estado_atual and regra[1] == char:
                    estado_atual = regra[2]
                    break
            else:
                container = resposta.append((word, 'REJEITA'))
                break
        else:
            if estado_atual in estados_finais:
                container = resposta.append((word, 'ACEITA'))
            else:
                container = resposta.append((word, 'REJEITA'))
    return dict(resposta)

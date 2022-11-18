import re


def parse_code(code, excs):
    result = re.search(r'^[A-Za-z]{2}[0-9]{4}$', code)
    if result:
        return result.group(0)
    excs.append(Exception(f'Código {code} no formato incorreto, use 2 letras e 4 números (ex: XX9999).'))

def check_chegada_partida(chegada_prevista, partida_prevista, excs):
    if chegada_prevista > partida_prevista:
        return chegada_prevista, partida_prevista
    excs.append(Exception('Partida prevista tem que ser antes da chegada prevista.'))
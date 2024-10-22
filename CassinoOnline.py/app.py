import itertools
import random
from time import sleep

#Criando a classe Player

class Player:
    def __init__(self, balance=0):
        self.balance = balance

#Criando a classe cassaniquel, na onde esta uma lista com os emojis
#As variavis levels que decide o level da rodada, balance é o saldo,
#Permutations serve para gerar os emojis aleatorios

class CassaNiquel:
    def __init__(self):
        self.SIMBOLOS = {
            'smirking face': '1F60F',
            'collision': '1F4A5',
            'smiling face with sunglasses': '1F60E',
            'smiling face with horns': '1F608',
            'alien': '1F47D'
        }
        self.levels = ['1', '2', '3', '4']
        self.balance = 0
        self.permutations = self._gen_permutations()

    #Gerando uma matriz de 3 por 3 com os simbulos

    def _gen_permutations(self):
        permutations = list(itertools.product(self.SIMBOLOS.keys(), repeat=3))

        # Aumentando a chance do usuário ganhar

        for i in self.SIMBOLOS.keys():
            permutations.append((i, i, i))
        return permutations
    
    #Escolhendo figuras aleatorias para a matriz

    def _get_final_result(self, level):
        result = list(random.choice(self.permutations))

        # Aumenta a chance de ganhar com base no nível
        if level in ['3', '4'] and len(set(result)) == 3 and random.randint(0, 10) >= 2:
            result[1] = result[0]
        
        return result
    
    #Criando um display com tempo tanto de rolagem das imagens como o tempo que elas vão acontecer

    def _display(self, amout_bet, result, time=0.5):
        seconds = 3
        for _ in range(int(seconds / time)):
            print(self._emojize(random.choice(self.permutations)))
            sleep(time)
        print(self._emojize(result))

        #Exibindo a mensagem para o usuario

        if self._check_result_user(result):
            print(f'Você venceu e recebeu: {amout_bet * 1.5}')
        else:
            print('Essa foi por pouco! Na próxima você ganha, tente novamente.')

    #Trasnformando os emojis de hexadecimal para emojis

    def _emojize(self, emojis):
        return ''.join(chr(int(self.SIMBOLOS[code], 16)) for code in emojis)
    
    #Analisando os resultados dos usuarios, se a tupla for igual o usuario ganhou
    
    def _check_result_user(self, result):
        return result[0] == result[1] == result[2]
    
    #Atualizando o balance com os ganhos e as perdas

    def _update_balance(self, amout_bet, result, player: Player):
        if self._check_result_user(result):
            player.balance += (amout_bet * 2)
            self.balance -= (amout_bet * 1.5)
        else: 
            player.balance -= amout_bet
            self.balance += amout_bet

    #Criando a função play

    def play(self, amout_bet, player: Player):
        level = random.choice(self.levels)  # Seleciona um nível aleatório para cada jogada
        print(f"Nível da jogada: {level}")
        result = self._get_final_result(level)
        self._display(amout_bet, result)
        self._update_balance(amout_bet, result, player)

# Execução do jogo
maquina1 = CassaNiquel()
player1 = Player(balance=100)  # Exemplo de saldo inicial para o jogador

for _ in range(5):
    bet = random.randint(1, min(10, player1.balance))  # Aposta aleatória entre 1 e o saldo do jogador
    if player1.balance >= bet:
        maquina1.play(bet, player1)
    else:
        print("Saldo insuficiente para a aposta.")

print(f'Saldo do jogador: {player1.balance}')
print(f'Saldo da máquina: {maquina1.balance}')


try:
    import numpy as np
except ImportError:
    print("Lo sentimos... Necesita Instalar numpy para que funcione el juego.")
    print("MANCALA - jugado desde tiempos remotos")
    raise

from easyAI import TwoPlayersGame


class Awele(TwoPlayersGame):
 
    print()
    print("MANCALA - jugado desde tiempos remotos")
    print()
    print("Comienzas eres el jugador player 1")
    print("Tus casillas son a, b, c, d, e, f")
    print()
    def __init__(self, players):
        for i, player in enumerate(players):
            player.score = 0
            player.isstarved = False
            player.camp = i
        self.players = players
        
        # Initial configuration of the board.
        # holes are indexed by a,b,c,d...
        self.board = [4, 4, 4, 4, 4, 4,  
                      4, 4, 4, 4, 4, 4]  
                      
        self.nplayer = 1  # player 1 starts.

    def make_move(self, move):
        if move == "None":
            self.player.isstarved = True
            s = 6 * self.opponent.camp
            self.player.score += sum(self.board[s:s + 6])
            return

        move = 'abcdefghijkl'.index(move)

        pos = move
        for i in range(self.board[move]):  #DEAL
            pos = (pos + 1) % 12
            if pos == move:
                pos = (pos + 1) % 12
            self.board[pos] += 1
        self.board[move] = 0

        while ((pos / 12) == self.opponent.camp
               and (self.board[pos] in [2, 3])):  # TAKE
            self.player.score += self.board[pos]
            self.board[pos] = 0
            pos = (pos - 1) % 12
    def possible_moves(self):


        if self.nplayer == 1:
            if max(self.board[:6]) == 0: return ['None']
            moves = [i for i in range(6) if (self.board[i] >= 6 - i)]
            if moves == []:
                moves = [i for i in range(6) if self.board[i] != 0]
        else:
            if max(self.board[6:]) == 0: return ['None']
            moves = [i for i in range(6,12) if (self.board[i] >= 12-i)]
            if moves == []:
                moves = [i for i in range(6, 12) if self.board[i] != 0]

        return ['abcdefghijkl'[u] for u in moves]

    def show(self):
        print("Puntuje: Player1 %d /  Maquina %d" % tuple(p.score for p in self.players))
        print('  '.join('lkjihg'))
        print(' '.join(["%02d" % i for i in self.board[-1:-7:-1]]))
        print(' '.join(["%02d" % i for i in self.board[:6]]))
        print('  '.join('abcdef'))

    def lose(self):
        return self.opponent.score > 24

    def is_over(self):
        return ( self.lose() or
                  sum(self.board) < 7 or
                  self.opponent.isstarved )


if __name__ == "__main__":
    
    from easyAI import Human_Player, AI_Player, Negamax

    scoring = lambda game: game.player.score - game.opponent.score
    ai = Negamax(6, scoring)
    game = Awele([Human_Player(), AI_Player(ai)])

    game.play()

    if game.player.score > game.opponent.score:
        print("GANASTE .")
    elif game.player.score < game.opponent.score:
        print("PERDISTE .")
    else:
        print("Looks like we have a draw.")

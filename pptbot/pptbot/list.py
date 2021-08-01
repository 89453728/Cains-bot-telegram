class Player:
    def __init__(self,points: int,position: int,attemps: int, username: str):
        self.attemps = attemps
        self.position = position
        self.points = points
        self.username = username
    def addPoints(self,points:int):
        self.points = self.points + points
    def ChangePosition(self,pos: int):
        self.position = pos 
    def getPosition(self):
        return self.position
    def getPoints(self):
        return self.points
    def getUsername(self):
        return self.username

class Top:
    def __init__(self):
        self.topList = []
        self.nPlayers = 0
        self.bestScore = 0
        self.worstScore = 0
    def addPlayer (self,player: Player):
        aux = []
        if(self.nPlayers > 0):
            for iter in range(0,self.nPlayers):
                print ("attemp " + str(iter))
                if (self.topList[iter].getPoints() < player.getPoints()):
                    # agrego el jugador nuevo delante del que tiene menor puntuacion que el
                    player.ChangePosition(self.topList[iter].getPosition())

                    for iter2 in range(iter,self.nPlayers):
                        self.topList[iter2].ChangePosition(self.topList[iter2].getPosition + 1)

                    if (iter != 0):
                        aux = self.topList[0:iter-1]
                        aux.append(player)
                        aux.append(self.topList[iter:(self.nPlayers-1)])
                    else:
                        aux.append(player)
                        aux.append(self.topList[1:self.nPlayers-1])
                    self.topList = aux
                    self.nPlayers = self.nPlayers + 1

                elif (self.topList[iter].getPoints() == player.getPoints()):
                    # agrego el jugador justo despues del que tiene menor puntuacion que el
                    player.ChangePosition(self.topList[iter].getPosition())
                    aux = self.topList[0:iter]
                    aux.append(player)
                    aux.append(self.topList[iter+1:(self.nPlayers-1)])
                    self.topList = aux
                    self.nPlayers = self.nPlayers + 1
                else:
                    continue
        else :
            self.topList.append(player)
            self.nPlayers = 1
        self.bestScore = self.topList[0].getPoints()

    def removePlayer (self, username:str):
        aux = []
        if (self.nPlayers > 0):
            for iter in range(0,self.nPlayers):
                if (self.topList[iter].username == username):
                    if(iter != 0):
                        aux = self.topList[0:iter-1]
                        aux.append(self.topList[iter+1:self.nPLayers -1])
                    else:
                        aux = self.topList[1:self.nPlayers - 1]

                    self.topList = aux
                    self.nPlayers = self.nPlayers - 1
            if (self.nPlayers > 0):
                self.bestScore = self.topList[0].getPoints()
            else:
                self.bestScore = 0

    
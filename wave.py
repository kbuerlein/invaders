"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

Kayton Buerlein keb324
11 December 2023
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    #Attribute _direction: direction aliens should head in
    #Invariant: _direction is a string and either 'right' or 'left'

    #Attribute _steps: amount of steps that should pass before alien fires
    #Invariant: _steps is an int between 1 and BOLT_RATE

    #Attribute _tracker: tracks the amount of steps an alien takes
    #Invariant: _tracker is an int

    #Attribute _change: tracks when need to change state to paused
    #Invariant: _change is a boolean expression, either True or False

    #Attribute _aliendefeat: True when all aliens are defeated, False if not
    #Invariant: _aliendefeat is a boolean expression, either True or False

    #Attribute _playerlose: True when an alien breaches the defense line, False
    #if not.
    #Invariant: _playerlose is a boolean expression, either True or False

    #Attribute _speeder: keeps track of how much aliens should speed up by.
    #Invariant: _speeder is a float


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getchange(self):
        """
        Returns value of self._change.
        """
        return self._change

    def getlives(self):
        """
        Returns value of self._lives.
        """
        return self._lives

    def getaliendefeat(self):
        """
        Returns value of self._aliendefeat.
        """
        return self._aliendefeat

    def getplayerlose(self):
        """
        Returns value of self._playerlose.
        """
        return self._playerlose

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes the App with attributes.
        """
        self.alienmaker()
        self.shipmaker()
        self.dlinemaker()
        self._time = 0
        self._direction = 'right'
        self._bolts = []
        self._steps = random.randrange(1, BOLT_RATE)
        self._tracker = 0
        self._lives = SHIP_LIVES
        self._change = False
        self._aliendefeat = False
        self._playerlose = False
        self._speeder = 1.0

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,dt,input):
        """
        Updates the ship, aliens, and bolts.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: detected input to determine whether to fire a playerbolt
        Precondition: input is an instance of GInput
        """
        self._change = False
        if self._ship is not None:
            self._ship.moveship(input)
        self.movealiens(dt)
        self.detectbolt(input)
        self.alienbolt()
        for x in self._bolts:
            x.y = x.y + x._velocity
            if x.y > GAME_HEIGHT or x.y < 0:
                index = self._bolts.index(x)
                del self._bolts[index]
        self.shipcollision()
        self.aliencollision()
        if self.alienchecker():
            self._aliendefeat = True
        self.checkplayerlose()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws the Ship, Aliens, Defensive line, and Bolts

        Parameter view: view is the view in which to draw the attributes
        Precondition: view is an instance of GView.
        """
        for row in self._aliens:
            for a in row:
                if a is not None:
                    a.draw(view)
        if self._ship is not None:
            self._ship.draw(view)
        self._dline.draw(view)
        for b in self._bolts:
            b.draw(view)


    # HELPER METHODS FOR COLLISION DETECTION
    def alienmaker(self):
        """
        Creates a 2d list of aliens of ALIEN_WIDTH width and ALIEN_HEIGHT height.

        Horizontal distance between aliens is ALIEN_H_SEP and vertical distance
        between aliens is ALIEN_V_SEP.
        This method also accounts for the game ceiling, ALIEN_CEILING.

        The aliens are created from the bottom, changing alien images between
        every 2 rows.
        """
        alienlist = ['alien1.png','alien1.png','alien2.png','alien2.png',\
        'alien3.png','alien3.png']
        o = 0
        p = []
        for i in range(ALIEN_ROWS):
            l = []
            for w in range(ALIENS_IN_ROW):
                source=alienlist[o]
                px=(ALIEN_H_SEP+ALIEN_WIDTH//2)+w*(ALIEN_WIDTH + ALIEN_H_SEP)
                py=(i*(ALIEN_HEIGHT + ALIEN_V_SEP)+GAME_HEIGHT-\
                ALIEN_CEILING-ALIEN_HEIGHT//2-(ALIEN_HEIGHT*(ALIEN_ROWS-1))\
                -(ALIEN_V_SEP*(ALIEN_ROWS-1)))
                l.append(Alien(x = px, y = py, source=source))
            o = o+1
            if o == 6:
                o = 0
            p.append(l)
        self._aliens = p
        self.megaalienmaker()

    def shipmaker(self):
        """
        Creates the ship and stores it in self._ship.
        """
        self._ship=Ship(y = SHIP_BOTTOM+SHIP_HEIGHT//2,\
        x = GAME_WIDTH/2, source = SHIP_IMAGE)

    def dlinemaker(self):
        """
        Creates the defense line and stores it in self._dline.
        """
        p = [0, DEFENSE_LINE,GAME_WIDTH, DEFENSE_LINE]
        self._dline=GPath(points=p, linecolor='pink',linewidth=2)

    def movealiens(self, dt):
        """
        Moves the aliens at speed ALIEN_SPEED*self._speeder.

        self._tracker tracks when the Aliens should move.
        """
        #Accounts for new speed of aliens after defeat
        if self._time > ALIEN_SPEED*self._speeder:
            self.rmove()
            self.lmove()
            self._time = 0
            self._tracker = self._tracker + 1
        self._time = self._time + dt

    def rmove(self):
        """
        Moves list of aliens right (or vertically if they reach the right edge)

        Accounts for aliens that are not None.
        """
        if self._direction == 'right' and self.checkright() is not False:
            a = self.checkright()
            b = a[0]
            c = a[1]
            if self._aliens[b][c].x > GAME_WIDTH-(ALIEN_H_SEP+ALIEN_WIDTH//2):
                for row in self._aliens:
                    for alien in row:
                        if alien is not None:
                            alien.y = alien.y - ALIEN_V_WALK
                self._direction = 'leftone'
            else:
                for row in self._aliens:
                    for alien in row:
                        if alien is not None:
                            alien.x = alien.x + ALIEN_H_WALK


    def lmove(self):
        """
        Moves list of aliens left (or vertically if they reach the left edge)

        Accounts for aliens that are not None.
        """
        if self._direction == 'left' and self.checkleft() is not False:
            a = self.checkleft()
            b = a[0]
            c = a[1]
            if self._aliens[b][c].x < (ALIEN_H_SEP+ALIEN_WIDTH//2):
                for row in self._aliens:
                    for alien in row:
                        if alien is not None:
                            alien.y = alien.y - ALIEN_V_WALK
                self._direction = 'right'
            else:
                for row in self._aliens:
                    for alien in row:
                        if alien is not None:
                            alien.x = alien.x - ALIEN_H_WALK
        if self._direction == 'leftone':
            self._direction = 'left'

    def detectbolt(self,input):
        """
        Detects input to fire a bolt from ship.

        Parameter input: input from user to determine whether to fire
        Precondition: input is an instance of GInput
        """
        if self.checkbolts() == False and self._ship is not None:
            if input.is_key_pressed('up') or input.is_key_pressed('spacebar'):
                yy = SHIP_BOTTOM+SHIP_HEIGHT+(0.5*BOLT_WIDTH)
                d = Bolt(x=(self._ship.x),y=yy,firer='player')
                self._bolts.append(d)

    def checkbolts(self):
        """
        Returns True if there is a player bolt in self._bolts, otherwise False
        """
        if self._bolts == []:
            return False
        for bolt in self._bolts:
            if bolt.isPlayerBolt() == True:
                return True
        return False

    def alienbolt(self):
        """
        Creates an alien bolt from a random column at the lowest row.
        """
        if self._tracker == self._steps:
            self._tracker = 0
            self._steps = random.randrange(1, BOLT_RATE)
            b = random.randrange(0, ALIENS_IN_ROW)
            r = self.checkcolumn(b)
            if r is not False:
                d = Bolt(x=(self._aliens[r][b].x),y=self._aliens[r][b].y,\
                firer='alien')
                self._bolts.append(d)

    def checkcolumn(self,b):
        """
        Returns lowest row in column b that is not None. If None, return False.

        Parameter b: b is a column in self._aliens
        Precondition: b is an int, and is a column in self._aliens
        """
        for g in range(len(self._aliens)):
            if self._aliens[g][b] != None:
                return g
        return False

    def shipcollision(self):
        """
        Deletes the ship (makes it None) when it collides with an alienbolt

        Also deletes the bolt that the ship collides with from self._bolts.
        """
        index = False
        self._change = False
        for bolt in range(len(self._bolts)):
            if self._ship is not None:
                if self._ship.shipcollides(self._bolts[bolt]):
                    self._ship = None
                    index = bolt
                    self._change = True
                    self._lives = self._lives-1
        if index != False:
            del self._bolts[index]

    def aliencollision(self):
        """
        Deletes an alien if it collides with a playerbolt.

        Accounts for MegaAlien lives, and depletes or deletes them (depending on
        how many lives they have left) if hit by a playerbolt.

        If an alien is defeated, self._speeder is multiplied by 0.97.

        Removes the playerbolt that collided with the alien from self._bolts.
        """
        for row in range(len(self._aliens)):
            for col in range(len(self._aliens[row])):
                for bolt in self._bolts[:]:
                    if self._aliens[row][col] is not None:
                        c = self._aliens[row][col]
                        if c.aliencollides(bolt):
                            if isinstance(c, MegaAlien):
                                new = bolt
                                self._bolts.remove(new)
                                if c.getmalienlives() <= 1:
                                    #have to delete megaalien if no lives left
                                    self._aliens[row][col] = None
                                    self._speeder = (self._speeder)*0.97
                                    if self.alienchecker():
                                        self._aliendefeat = True
                                else:
                                #have to deplete a life and not delete megaalien
                                    c.changemalienlives()
                            else:
                                self._aliens[row][col] = None
                                new = bolt
                                self._bolts.remove(new)
                                self._speeder = (self._speeder)*0.97
                                if self.alienchecker():
                                    self._aliendefeat = True

    def alienchecker(self):
        """
        If all aliens are defeated, returns True. Else, False.
        """
        for row in self._aliens:
            for col in row:
                if col is not None:
                    return False
        return True

    def checkleft(self):
        """
        Returns lowest row and lowest column in self._aliens that is not None.

        Returns a list of [row, column], or False if all aliens are None.
        """
        for x in range(ALIENS_IN_ROW):
            for g in range(len(self._aliens)):
                if self._aliens[g][x] is not None:
                    return [g,x]
        return False

    def checkright(self):
        """
        Returns lowest row and highest column in self._aliens that is not None.

        Returns a list of [row, column], or False if all aliens are None.
        """
        for x in range(ALIENS_IN_ROW-1, -1, -1):
            for g in range(len(self._aliens)):
                if self._aliens[g][x] is not None:
                    return [g,x]
        return False

    def checkplayerlose(self):
        """
        Checks to see if a player has lost by aliens breaching the defense line.
        """
        for row in self._aliens:
            for col in row:
                if col is not None:
                    if (col.y - ALIEN_HEIGHT) < DEFENSE_LINE:
                        self._playerlose = True

    def megaalienmaker(self):
        """
        Creates one 'mega alien' per row in self._alien rows.

        Chooses a random column in each row of self._aliens and changes that
        specific alien at self._aliens[row][column] to become a MegaAlien.
        """
        #Changes one alien in a row to be a megaalien
        for row in range(len(self._aliens)):
            r = random.randint(0, ALIENS_IN_ROW-1)
            c = self._aliens[row][r]
            self._aliens[row][r] = MegaAlien(x = c.x, y = c.y, lives = 3)

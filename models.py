"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

Kayton Buerlein keb324
11 December 2023
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, x, y, source):
        """
        Initializes the ship with all attributes.

        Parameter x: x position of the center of the ship.
        Precondition: x must be an int or a float

        Parameter y: y position of the center of the ship.
        Precondition: y must be an int or a float

        Parameter source: image file for the ship.
        Precondition: source must be a valid image file
        """
        super().__init__(width = SHIP_WIDTH,height = SHIP_HEIGHT,\
        x=x, y=y, source=source)

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def moveship(self, input):
        """
        Moves the ship when correct input is received.
        """
        da = 0
        if input.is_key_down('left'):
            da = da - SHIP_MOVEMENT
        if input.is_key_down('right'):
            da = da + SHIP_MOVEMENT
        if 0 < self.x + da < GAME_WIDTH:
            self.x = self.x+da

    def shipcollides(self,bolt):
        """
        Returns True if the alien bolt collides with player

        This method returns False if bolt was not fired by an alien.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt, Bolt)

        if bolt._velocity == BOLT_SPEED:
            return False
        if self.contains((bolt.x+BOLT_WIDTH//2, bolt.y+BOLT_HEIGHT//2)):
            return True
        if self.contains((bolt.x-BOLT_WIDTH//2, bolt.y+BOLT_HEIGHT//2)):
            return True
        if self.contains((bolt.x+BOLT_WIDTH//2, bolt.y-BOLT_HEIGHT//2)):
            return True
        if self.contains((bolt.x-BOLT_WIDTH//2, bolt.y-BOLT_HEIGHT//2)):
            return True
        return False
    # COROUTINE METHOD TO ANIMATE THE SHIP

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    #

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y, source):
        """
        Initializes an alien with all of its attributes.

        Parameter x: x position of the center of the alien.
        Precondition: x must be an int or a float

        Parameter y: y position of the center of the alien.
        Precondition: y must be an int or a float

        Parameter source: image file for the alien.
        Precondition: source must be a valid image file
        """
        super().__init__(width = ALIEN_WIDTH,height = ALIEN_HEIGHT,\
        x=x, y=y, source=source)

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)

    def aliencollides(self,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt, Bolt)

        if bolt._velocity == -BOLT_SPEED:
            return False
        elif self.contains((bolt.x+BOLT_WIDTH//2, bolt.y+BOLT_HEIGHT//2)):
            return True
        elif self.contains((bolt.x-BOLT_WIDTH//2, bolt.y+BOLT_HEIGHT//2)):
            return True
        elif self.contains((bolt.x+BOLT_WIDTH//2, bolt.y-BOLT_HEIGHT//2)):
            return True
        elif self.contains((bolt.x-BOLT_WIDTH//2, bolt.y-BOLT_HEIGHT//2)):
            return True
        else:
            return False

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, x, y, firer):
        """
        Initializes the bolt with all of its attributes.

        Parameter x: x position of the center of the bolt.
        Precondition: x is an int or a float.

        Parameter y: y position of the center of the bolt.
        Precondition: y is an int or a float.

        Parameter firer: firer determines where the bolt is coming from (alien
        or player)
        Precondition: firer is a string and either 'alien' or 'player'
        """
        assert isinstance(firer, str)
        assert firer == 'alien' or firer == 'player'

        super().__init__(x=x,y=y,width = BOLT_WIDTH,\
        height = BOLT_HEIGHT,fillcolor = '#cc0066', firer=firer)
        if firer == 'player':
            self._velocity = BOLT_SPEED
        if firer == 'alien':
            self._velocity = -BOLT_SPEED

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """
        Returns True if the bolt is fired from the player.
        """
        if self._velocity == BOLT_SPEED:
            return True
        if self._velocity == -BOLT_SPEED:
            return False


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE

class MegaAlien(Alien):
    """
    A class to represent a single mega alien.

    A mega alien is an alien that has its own _lives attribute, and it has the
    same attributes as Alien. Unlike normal aliens, mega aliens have 3 lives.
    They also have a special image.
    Inherits all attributes from Alien.
    """
    # ATTRIBUTES
    #Attribute _lives: Keeps track of how many lives a mega alien has left.
    #Invariant: _lives is an int

    #Getters and setters
    def getmalienlives(self):
        """
        Returns the value of _lives attribute.
        """
        return self._lives

    #Initializer
    def __init__(self, x, y, lives):
        """
        Initializes a mega alien with all of its attributes.

        Parameter x: x position of the center of the bolt.
        Precondition: x is an int or a float.

        Parameter y: y position of the center of the bolt.
        Precondition: y is an int or a float.

        Parameter lives: lives is the amount of lives the MegaAlien still has.
        Precondition: lives is an int.
        """
        assert isinstance(lives, int)
        super().__init__(x=x, y=y, source='alien5.png')
        self._lives = lives

    #Methods
    def changemalienlives(self):
        """
        Depletes a life from the MegaAlien by subtracting 1 from _lives.
        """
        self._lives = self._lives - 1

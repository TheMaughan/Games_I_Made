"""
File: skeet.py
Original Author: Br. Burton
Co-Author: Bryce Maughan
This program implements an awesome version of skeet.
McBeth teaching 212-python data structs intro & 310
CS- 246  Do -> CSE-310
"""
import arcade
import math
import random
from abc import abstractmethod
from abc import ABC

# These are Global constants to use throughout the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

RIFLE_WIDTH = 100
RIFLE_HEIGHT = 20
RIFLE_COLOR = arcade.color.DARK_RED

BULLET_RADIUS = 3
BULLET_SPEED = 10

TARGET_RADIUS = 30
#TARGET_SAFE_RADIUS = 15

"""
#- I'm going to put this code into comments to come back to on a later date...
class Animate_Object:
    def __init__(self):
        self.red = arcade.color.RASPBERRY
        self.purple = arcade.color.PURPLE_MOUNTAIN_MAJESTY
        self.orange = arcade.color.ORANGE_PEEL
        self.black = arcade.color.BLACK_OLIVE

    def animate_object(self):
        color_list = [self.red, self.purple, self.orange, self.black]
        self.script.append(color_list)
        return self.script
"""

class Point: #- Object Location
    def __init__(self):
        self.x = 0
        self.y = 0

class Velocity: #- Object progression
    def __init__(self):
        self.dx = 0
        self.dy = 0

class Place_Obj(ABC): #- All travling objects share these same atrabutes:
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True
        self.radius = 0.0
        self.create()

    @abstractmethod
    def draw(self): #- Draw the physical properties:
        pass

    def advance(self): #- Progress/move in a straight line:
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    
    def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT): #- If event where object leaves the window, kill the object:
        if (self.center.x < 0.0 or self.center.x > SCREEN_WIDTH):
            return True
        if (self.center.y < 0.0 or self.center.y > SCREEN_HEIGHT):
            return True
        return False

    @abstractmethod
    def create(self): #- Set dementions for the target to draw at a location:
        pass

class Target(Place_Obj, ABC): #- Sets the design for the Target template
    def __init__(self): #- Set perameters
        super().__init__()
        self.radius = TARGET_RADIUS
    @abstractmethod
    def draw(self): #- Draw
        pass
    @abstractmethod
    def hit(self): #- Kill on event
        pass
    @abstractmethod
    def create(self): #- Create at location based on random generator perameters:
        pass
    
class Target_Safe(Target):
    def __init__(self):
        super().__init__()

    #- Set dementions for the target to draw:
    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius / 2, arcade.color.GREEN)

    #- Kills target on collision event:
    def hit(self):
        self.alive = False
        return -10
    
    #- Set dementions for the target to draw at a location.
    def create(self):
        self.center.x = self.radius
        self.center.y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT)
        self.velocity.dx = random.uniform(1, 5) #- Manipulate speed of ball here (min speed, max speed)
        self.velocity.dy = random.uniform(-2, 5)

class Target_Strong(Target):
    def __init__(self):
        super().__init__()
        self.red = arcade.color.RASPBERRY
        self.purple = arcade.color.PURPLE_MOUNTAIN_MAJESTY
        self.orange = arcade.color.ORANGE_PEEL
        self.black = arcade.color.BLACK_OLIVE
        self.color_list = [self.red, self.purple, self.orange, self.black]

    #- Set dementions for the target to draw:
    def draw(self):
        
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, self.color_list[self.animate()])
        #self.script.append(color_list)
        #return self.script
        

    #- Kill target on collision event:
    def hit(self):
        score = 0

        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, arcade.color.RED)

        self.radius -= 10

        if self.radius == 20:
            score += 1
        elif self.radius == 10:
            score += 1
        elif self.radius <= 0:
            score += 5
            self.alive = False

        return score
        
    #- Set dementions for the target to draw at a location:
    def create(self):
        self.alive = True
        self.center.x = SCREEN_WIDTH - self.radius
        self.center.y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT)
        self.velocity.dx = random.uniform(-1, -3) #- Manipulate speed of ball here (min speed, max speed)
        self.velocity.dy = random.uniform(-2, 3)

    def animate(self):
        pointer = 0
        for color in self.color_list:
            if pointer >= 4:
                pointer -= 1
            elif pointer <=  0:
                pointer += 1
        return pointer

class Target_Standard(Target):
    def __init__(self):
        super().__init__()
        
    #- Set dementions for the Safe_Target to draw:
    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, arcade.color.BLUE)

    #- Kill the target on collision event.
    def hit(self):
        self.alive = False
        return 1
    
    #- Set dementions for the target to draw at a location.
    def create(self):
        self.center.x = SCREEN_WIDTH - self.radius
        self.center.y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT)
        self.velocity.dx = random.uniform(-1, -5) #- Manipulate speed of ball here (min speed, max speed)
        self.velocity.dy = random.uniform(-2, 5)


class Bullet(Place_Obj):
    def __init__(self):
        super().__init__()
        #- Call the ceation of the bullet:
        self.create()

    def draw(self): #- Draw Ball with radius of 10 px:
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, self.color)

    #- Sets the angle of the bullet tragectory and initiates the creation of the bullet.
    def fire(self, angle: float):
        self.alive = True
        self.velocity.dx = math.cos(math.radians(angle)) * self.speed
        self.velocity.dy = math.sin(math.radians(angle)) * self.speed
    
    #- Create the Bullet in the Rifle
    def create(self): #- Set the perameters for the bullet
        self.center.x = 0
        self.center.y = 0
        self.speed = BULLET_SPEED
        self.radius = BULLET_RADIUS
        self.color = arcade.color.BLACK
        self.alive = True


class Rifle:
    """
    The rifle is a rectangle that tracks the mouse.
    """
    def __init__(self):
        self.center = Point()
        self.center.x = 0
        self.center.y = 0

        self.angle = 45

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, RIFLE_WIDTH, RIFLE_HEIGHT, RIFLE_COLOR, 360 - self.angle)


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Rifle
        Target (and it's sub-classes)
        Point
        Velocity
        Bullet
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class, but mostly
    you shouldn't have to. There are a few sections that you
    must add code to.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.rifle = Rifle()
        self.bullet = Bullet()
        #self.animate = Target()
        self.score = 0

        self.bullets = []

        self.targets = []

        self.pointer = Target_Strong()

        self.script = []

        # TODO: Create a list for your targets (similar to the above bullets)


        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.rifle.draw()

        for bullet in self.bullets:
            bullet.draw()

        for target in self.targets:
            target.draw()

        # TODO: iterate through your targets and draw them...


        self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()

        # decide if we should start a target
        if random.randint(1, 50) == 1:
            self.create_target()

        for bullet in self.bullets:
            bullet.advance()

        for target in self.targets:
            target.advance()

        for a in self.script:
            pointer.animate()
            

        """
        for script in self.script:
            pass
        """

        # TODO: Iterate through your targets and tell them to advance

    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        :return:
        """
        #- Initiate the different target objects:
        safe = Target_Safe()
        strong = Target_Strong()
        standard = Target_Standard()
        
        #- Create the different targets based on the data from the "create()" method:
        safe.create()
        strong.create()
        standard.create()

        #- Append the different target objects to a list:
        #- "self.targets" now represents all the targets appended while in this class.
        self.targets.append(safe)
        self.targets.append(strong)
        self.targets.append(standard)

        # TODO: Decide what type of target to create and append it to the list

    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                                abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        self.score += target.hit()

                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for target in self.targets:
            if not target.alive:
                self.targets.remove(target)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        :return:
        """
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for target in self.targets:
            if target.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.targets.remove(target)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # set the rifle angle in degrees
        self.rifle.angle = self._get_angle_degrees(x, y)
        #self.bullet.angle = self._get_angle_degrees(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire!
        angle = self._get_angle_degrees(x, y)

        bullet = Bullet()
        bullet.fire(angle)

        self.bullets.append(bullet)

    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.
        Note: This could be a static method, but we haven't
        discussed them yet...
        """
        # get the angle in radians
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees



# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()
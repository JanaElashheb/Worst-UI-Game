"""
Worst UI Possible - Classes
ICS4U-01
Madeeha Syed, Jana Elashheb, Efua Amuah
Contains classes for Worst UI possible.

History:
May 27, 2025: Date created
June 4, 2025: Added the button class
June 5, 2025: Removed unnecessary functions in Text class
June 9, 2025: Date completed
"""
#===IMPORTS===
import pygame
import random

#initalizes pygame
pygame.init()

#===CONSTANTS===
WIDTH = 400
HEIGHT = 400
FALLING_SPEED = 1
MAX_NUMS = 10

#===GAME VARIABLES===
screen = pygame.display.set_mode((WIDTH,HEIGHT))

class Number(pygame.sprite.Sprite):
    """
    Contains a number class.
    
    Attributes:
        num (str) : number
    """
    
    def __init__(self, num):
        """
        Initalize a number.
        
        Args:
            num (str)
        """
        pygame.sprite.Sprite.__init__(self)
        
        #sets actual number
        self.num = num
        
        #select a random spot on the width to spawn on
        random_width = random.randint(0, WIDTH)
        #create text of number
        self.text = Text(num, "Arial", 20, (0,0,0), (random_width, 0)) #HAVE IMAGES OF NUMBERS INSTEAD??
        
    def check_clicks(self, mouse_position, phone_number):
        """
        Checks if the user has clicked on the number.
        
        Args:
            mouse_position ((int, int)) : (x, y) position of mouse
            phone_number (str) : phone number text
            
        Returns:
            phone_number (str)
        """
        #checks if the number has been clicked
        if self.text.text_rect.collidepoint(mouse_position):
            #checks if the number being clicked doesn't exceed the maximum numbers allowed
            if len(phone_number) + 1 <= MAX_NUMS:
                #updates the phone number and kill the text
                phone_number = self.num+phone_number
                self.kill()
                
        return phone_number
    
    def fall(self):
        """Has the number constantly falling."""
        #checks if the number has completely left the screen
        if self.text.text_rect.y > HEIGHT:
            #kills the number
            self.kill()
        else:
            #updates the number's position on the screen
            self.text.text_rect.y+=FALLING_SPEED

class Text():
    """
    Contains a text class.
    
    Attributes:
        text (str) : content of text
        font (str) : text font (system fonts)
        f_colour ((int, int, int)) : RGB colour of font
        x (int) : x position of text
        y (int) : y position of text
        display_text (Surface) : rendered text
        text_rect (Rect) : text rect
    """
    
    def __init__(self, text, font, size, f_colour, position):
        """
        Initalizes text.
        
        Args:
            text (str) : content of text
            font (str) : text font (system fonts)
            size (int) : size of text
            f_colour ((int, int, int)) : RGB colour of font
            pos ((int, int)) : (x, y) position of button (centered)
        """
        self.font = pygame.font.SysFont(font, size)
        self.text = text
        self.f_colour = f_colour
        
        #gets position of text
        self.x = position[0]
        self.y = position[1]

        #renders the text on the button
        self.display_text = self.font.render(self.text, True, self.f_colour)
        
        #gets the rect of the button
        self.text_rect = self.display_text.get_rect()
        #positions the rectangle using the center point
        self.text_rect.center = self.x, self.y
        
    def display(self):
        """Displays text."""
        screen.blit(self.display_text, self.text_rect)

class Button():
    """
    Creates a button.

    Attributes:
        text (str) : content of button
        font (str) : text font (system fonts)
        size (int) : size of text
        f_colour ((int, int, int)) : RGB colour of font
        display_text (Surface) : rendering of text
        text_rect (Rect) : text rect
        b_colour ((int, int, int)) : RGB colour of background rect
        padding ((int, int)) : inflate button rect
        rounding (int) : default 0; rounds corners
        border (int) : default 0; if > 0 then outlines button, rather than filled
        current_col ((int, int, int)) : RGB value of current background colour
        back (Rect) : background rect for display
    """
    
    def __init__(self, text, font, size, f_colour, position, b_colour, padding, rounding, border=0):
        """
        Initalizes a button.
        
        Args:
            text (str) : content of button
            font (str) : text font (system fonts)
            size (int) : size of text
            f_colour ((int, int, int)) : RGB colour of font
            pos ((int, int)) : (x, y) position of button (centered)
            b_colour ((int, int, int)) : RGB colour of background rect
            padding ((int, int)) : inflate button rect
            rounding (int) : default 0; rounds corners
            border (int) : default 0; if > 0 then outlines button, rather than filled
        """
        self.font = pygame.font.SysFont(font, size)
        self.text = text
        self.f_colour = f_colour
        
        #renders the text on the button
        self.display_text = self.font.render(self.text, True, self.f_colour)
        
        #gets the rect of the button
        self.text_rect = self.display_text.get_rect()
        #positions the rectangle using the center point
        self.text_rect.center = position[0], position[1]
        
        self.b_colour = b_colour
        self.padding = padding
        self.border = border
        self.rounding = rounding
        self.current_col = self.b_colour
        #draws the back rectangle for background colour and hovering
        self.back = pygame.draw.rect(screen, self.b_colour, self.text_rect.inflate(self.padding), self.border, self.rounding)
        
    def display(self):
        """Displays button."""
        self.back = pygame.draw.rect(screen, self.current_col, self.text_rect.inflate(self.padding), self.border, self.rounding)
        screen.blit(self.display_text, self.text_rect)
        
    def hover(self, hover_col, mouse_pos):
        """
        When user hovers over button, changes colour.
        
        Args:
            hover_col ((int, int, int)) : hover colour of button
            mouse_pos ((int, int)) : current (x, y) position of cursor 
        """
        #if mouse is hovering on button
        if self.back.collidepoint(mouse_pos):
            #changes current colour to indicate button
            self.current_col = hover_col
        else:
            #otherwise changes back to normal colour
            self.current_col = self.b_colour    
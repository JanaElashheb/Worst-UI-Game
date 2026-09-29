"""
Worst UI Possible
ICS4U-01
Madeeha Syed, Jana Elashheb, Efua Amuah
This program makes the user input their phone number from a cascade of numbers and against a darkening screen.

History:
May 23: Date created 
May 27: Added text to the screen
June 2: Added the falling numbers
June 4: Edited the falling numbers, and added the enter and delete buttons. Updated program to be handled in functions
June 5: Added fading screen via fade_screen() and associated variables
June 9: Date completed
"""

#IDEAS
#Write number in the opposite order
#screen gets darker as you go
#catch the numbers

#===IMPORTS===
import pygame
import random
from classes import Text, Number, Button

#initalize pygame
pygame.init()

#===CONSTANTS===
WIDTH = 400
HEIGHT = 400
CENTERED = (WIDTH//2, HEIGHT//2)
#font for phone number
PHONE_FONT = "Arial"
#initalize number list
NUMS = ["0","1","2","3","4","5","6","7","8","9"]
#initialize maximum number limit for the phone number
MAX_NUMS = 10
#initalize initial screen colour
INITIAL_COLOUR = 211
#initalize speed of fading screen
FADE_SPEED = 0.1

#===GAME VARIABLES===
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

#sets caption of the window
pygame.display.set_caption("PLEASE LOCATE YOUR PHONE'S NUMBERS")

#===SCREEN FUNCTIONS===
def fade_screen(fade_screen, alpha_colour):
    """
    Fades the screen.
    Used the following for inspiration on how to approach fading screen: https://www.youtube.com/watch?v=H2r2N7D56Uw. Accessed 2025/06/05. 

    Args:
        fade_screen (Rect) : rectangle to fade screen
        alpha_colour (int) : colour of screen fade

    Returns:
        alpha_colour (int)
    """
    #checks to make sure colour is greater than or 0
    if alpha_colour >=0:
        #draws the updated colour rectangle onto the screen
        pygame.draw.rect(screen, (alpha_colour,alpha_colour,alpha_colour), fade_screen)
        #update the colour
        alpha_colour-=FADE_SPEED

    return alpha_colour

#===PROGRAM FUNCTIONS===
def enter_number(state):
    """
    Allows the user to enter their phone number.

    Args:
        state (str) : state of program

    Returns:
        state (str)
        phone_str (str) : phone number
    """
    #create instructions for inputting number
    input_instructions = Text("Please catch your phone number before the reset:", "Arial", 20, (0,0,0), (WIDTH//2, 40))
    #initalize enter and delete buttons
    enter = Button("ENTER", "Arial", 10, (255,255,255), (WIDTH-40,HEIGHT-20), (0,255,0), (5,5), 5)
    delete = Button("DELETE", "Arial", 10, (255,255,255), (40,HEIGHT-20), (255,0,0), (5,5), 5)
    
    #initalize phone number
    phone_str = ""
    #initalize text to display phone number
    phone_num = Text(phone_str, PHONE_FONT, 36, (0,0,0), (CENTERED))
    
    #initalize number group
    number_grp = pygame.sprite.Group()
    
    #initial screen colour
    colour = INITIAL_COLOUR
    #initalizes rectangle for fading
    fade = pygame.Rect(0,0,WIDTH,HEIGHT)

    while state == "MAIN": 
        #event handler
        for events in pygame.event.get():
            #checks if the user has clicked the X button
            if events.type == pygame.QUIT:
                #exits game loop
                state="QUIT"
            #checks if the user has clicked the mouse
            elif events.type == pygame.MOUSEBUTTONDOWN:
                #gets mouse position
                pos = pygame.mouse.get_pos()
                #if the user has clicked the enter button
                if enter.back.collidepoint(pos):
                    if len(phone_str)==MAX_NUMS:
                        state = "PASS"
                    else:
                        print("YOU SHALL NOT PASS")
                elif delete.back.collidepoint(pos):
                    #deletes last number in phone number
                    phone_str = phone_str[1:]
                else:
                    for sprite in number_grp:
                        #checks if the number has been clicked and updates the phone number
                        phone_str = sprite.check_clicks(pos, phone_str)
        else:
            #gets mouse position
            pos = pygame.mouse.get_pos()
            #updates screen
            colour = fade_screen(fade, colour)
            #checks if the screen has completely darkened
            if colour < 0:
                #empties number input to force user to restart
                phone_str = ""
                #reset colour to initial colour
                colour = INITIAL_COLOUR
            
            #loads the numbers randomly
            for i in range(0,1,8):
                #gets a random number
                rand_num = random.randint(0, len(NUMS)-1)
                number = Number(NUMS[rand_num])
                #adds it to the number group
                number_grp.add(number)
            
            #displays the numbers
            for values in number_grp:
                values.text.display()
                #has the numbers constantly falling towards the bottom of the screen
                values.fall()

            #display enter button
            enter.hover((0,0,0), pos)
            enter.display()
            #display delete (backspace) button
            delete.hover((0,0,0), pos)
            delete.display()
            
            #displays the phone number on the screen
            pygame.draw.rect(screen, (255,255,255), phone_num.text_rect)
            phone_num = Text(phone_str, PHONE_FONT, 36, (0,0,0), (CENTERED))
            phone_num.display()
            #displays the instructions
            pygame.draw.rect(screen, (255,255,255), input_instructions.text_rect)
            input_instructions.display()
            
            #updates the screen
            pygame.display.flip()
            #refreshes the frame rate
            clock.tick(60)
            
    return state, phone_str

def final_screen(state, phone_str):
    """
    Display if the user successfully inputs their number.

    Args:
        state (str) : state of program
        phone_str (str) : phone number

    Returns:
        state (str)
    """
    msg1 = Text("You have entered your number!", "Arial", 20, (0,0,0), (CENTERED))
    msg2 = Text("Yay.", "Arial", 20, (0,0,0), (WIDTH//2, msg1.text_rect.height+msg1.text_rect.bottom))
    num = Text(f"Your number: {phone_str}", "Arial", 20, (0,0,0), (WIDTH//2, msg2.text_rect.height+msg2.text_rect.bottom))

    while state == "PASS":
        #event handler
        for events in pygame.event.get():
            #checks if the user has clicked the X button
            if events.type == pygame.QUIT:
                #exits game loop
                state="QUIT"
        else:
            #fills screen with a gray background
            screen.fill((211, 211, 211))

            #displays messages
            msg1.display()
            msg2.display()
            num.display()
            
            #updates the screen
            pygame.display.flip()
            #refreshes the frame rate
            clock.tick(60)

    return state

def navigate():
    """Program handler."""
    status = "MAIN"
    #checks if the user doesn't want to quit
    while status != "QUIT":
        #if the user is in the main game function
        if status == "MAIN":
            status, phone_number = enter_number(status)
        #if the user has successfully input their number
        elif status == "PASS":
            status = final_screen(status, phone_number)

#====MAIN====        
navigate()
#exits pygame once user has exited
pygame.quit() 
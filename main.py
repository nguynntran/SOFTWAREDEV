

import pygame
from checkers.constants import Cons
from checkers.game import Game

FPS = 60
SCREEN = pygame.display.set_mode((Cons.WIDTH, Cons.HEIGHT))
pygame.display.set_caption('Овца и волки')

def main():
    pygame.init()  # Initialize pygame
    run = True
    clock = pygame.time.Clock()
    game = Game()  # Use Game class instead of Board
    
    while run:
        clock.tick(FPS) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.handle_click(pos)  # Handle mouse clicks
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press 'R' to reset game
                    game.reset_game()
        
        game.draw(SCREEN)  # Draw game state
        pygame.display.update()
    
    pygame.quit()  # Fix: add parentheses

if __name__ == "__main__":
    main()
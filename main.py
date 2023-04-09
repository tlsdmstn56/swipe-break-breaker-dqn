import pygame

from swipe_brick_breaker import Config, Game

def main():
    parser = Config.get_parser()
    args = parser.parse_args()
    config = Config.from_args(args)
    pygame.init()
    game = Game(config)
    game.run()
    pygame.quit()

if __name__ == '__main__':
    main()


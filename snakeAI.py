import pygame
import time
import random
import neat
import os
pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Edureka')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def gameLoop(genomes, config):
    nets = []
    snakes_genomes = []
    ge = []
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0
    ticks = 0
    snake_List = []
    Length_of_snake = 1

    # Init for netverket
    # print(genomes)
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        starts = [snake_block, -snake_block]  # Init direction
        # snake_object = [x1, y1] # Keep track of each snakes position
        snake_object = {"x1": x1, "y1": y1, "x1_change": random.choice(
            starts), "y1_change": random.choice(starts)}
        snakes_genomes.append(snake_object)
        ge.append(genome)
    # print("genomes: ", genomes) Printing genomes, mutating best from prev generation
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over and len(snakes_genomes) > 0:
        while game_close == True:
            dis.fill(blue)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
            game_over = True
            game_close = False
            break
            # Dont need to see score and restart
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # When playing
        ticks += 1
        for x, snake in enumerate(snakes_genomes):
            ge[x].fitness += 0.1  # Removed points for staying alive
            output = nets[x].activate((snake["x1"], snake["y1"], foodx, foody))
            if output[0] > 0:  # snake x go left
                snake["x1_change"] = -snake_block
                snake["y1_change"] = 0
            if output[0] < 0:  # snake x go right
                snake["x1_change"] = snake_block
                snake["y1_change"] = 0
            if output[1] < 0:  # snake x go up
                snake["y1_change"] = -snake_block
                snake["x1_change"] = 0
            if output[1] > 0:  # snake x go down
                snake["y1_change"] = snake_block
                snake["x1_change"] = 0

        # Speed up the program
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    global snake_speed
                    snake_speed = 1000
                elif event.key == pygame.K_DOWN:
                    snake_speed = 15

        dis.fill(blue)
        pygame.draw.rect(
            dis, green, [foodx, foody, snake_block, snake_block])  # Draw food
        for x, snake in enumerate(snakes_genomes):
            if ticks > 1000:
                ge[x].fitness -= 150
                snakes_genomes.remove(snake)
            snake["x1"] += snake["x1_change"]
            snake["y1"] += snake["y1_change"]
            if snake["x1"] >= dis_width or snake["x1"] < 0 or snake["y1"] >= dis_height or snake["y1"] < 0:
                ge[x].fitness -= 5
                snakes_genomes.remove(snake)
                # print(f"Remove {snake} because it hits the wall")
            # Draw the snake moving
            snake_Head = []
            snake_Head.append(snake["x1"])
            snake_Head.append(snake["y1"])  # snake_Head = [x1, y1]
            snake_List.append(snake_Head)  # snake_List = [[x1, y1]]
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            # for i in snake_List[:-1]:
            #     if i == snake_Head:
            #         game_close = True
            our_snake(snake_block, snake_List)

            Your_score(Length_of_snake - 1)
            pygame.display.update()
            # Check if someone wins and add new "food"
            if snake["x1"] == foodx and snake["y1"] == foody:
                foodx = round(random.randrange(
                    0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(
                    0, dis_height - snake_block) / 10.0) * 10.0
                Length_of_snake += 1
                ge[x].fitness += 10
                ticks = 0
        clock.tick(snake_speed)
    # pygame.quit()
    # quit()


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 50 generations.
    p.add_reporter(neat.Checkpointer(40))
    winner = p.run(gameLoop, 500)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)

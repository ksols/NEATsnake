import pygame
import time
import random
import neat
import math
import os
pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 300
dis_height = 200

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


def check_direction(x1_change, y1_change):
    if (x1_change == -snake_block and y1_change == 0):  # Direciton for moving west
        return "west"
    elif (x1_change == snake_block and y1_change == 0):  # ------- || -----------
        return "east"
    elif (y1_change == -snake_block and x1_change == 0):  # ------- || -----------
        return "up"
    elif (y1_change == snake_block and x1_change == 0):  # ------- || -----------
        return "down"


def get_direction(direction):
    if direction == "west":
        return [-snake_block, 0]  # [x1,y1]
    elif direction == "east":
        return [snake_block, 0]  # [x1,y1]
    elif direction == "up":
        return [0, -snake_block]  # [x1,y1]
    elif direction == "down":
        return [0, snake_block]  # [x1,y1]


def gameLoop(single_genome, config):
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0
    x1_change, y1_change = get_direction("up")

    snake_List = []
    Length_of_snake = 1

    # Init the fitness of the genome to 0
    single_genome.fitness = 0

    # The network playing from the genome
    net = neat.nn.FeedForwardNetwork.create(single_genome, config)

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    ticks = 0
    while not game_over:
        ticks += 1
        while game_close == True:
            dis.fill(blue)
            # message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
            game_over = True
            game_close = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Code for speeding up / down
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    global snake_speed
                    snake_speed = 10000
                elif event.key == pygame.K_DOWN:
                    snake_speed = 15

        output = net.activate([
            x1, y1, math.dist([x1, y1], [foodx, foody]), ticks])

        max_value = max(output)

        if output[0] == max_value:
            x1_change = x1_change
            y1_change = y1_change
        elif output[1] == max_value:  # Move left
            # If current direction is west we move down
            if (check_direction(x1_change, y1_change) == "west"):
                x1_change, y1_change = get_direction("down")
            elif (check_direction(x1_change, y1_change) == "east"):
                x1_change, y1_change = get_direction("up")
            elif (check_direction(x1_change, y1_change) == "up"):
                x1_change, y1_change = get_direction("west")
            elif (check_direction(x1_change, y1_change) == "down"):
                x1_change, y1_change = get_direction("east")
        elif output[2] == max_value:  # Move right
            if (check_direction(x1_change, y1_change) == "west"):
                x1_change, y1_change = get_direction("up")
            elif (check_direction(x1_change, y1_change) == "east"):
                x1_change, y1_change = get_direction("down")
            elif (check_direction(x1_change, y1_change) == "up"):
                x1_change, y1_change = get_direction("east")
            elif (check_direction(x1_change, y1_change) == "down"):
                x1_change, y1_change = get_direction("west")

        # Gain fitness from getting close
        # if (math.dist([x1, y1], [foodx, foody])) != 0:
        #     single_genome.fitness += 40 / \
        #         (math.dist([x1, y1], [foodx, foody]))

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
            # Loose means decrease of fitness
            single_genome.fitness -= 5
        elif (ticks > 200):  # Also loose if ticks go over 1000 | Restarts when getting point
            game_close = True
            # single_genome.fitness -= 100 # Possible to give negative fitness for looping for more than 200 ticks
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(
            dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:

            foodx = round(random.randrange(
                0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(
                0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            # HUGE reward for hitting the "apple" at [foodx, foody]
            ticks = 0
            single_genome.fitness += 100

        clock.tick(snake_speed)


def eval_genomes(genomes, config):
    print("Ny poppulation incoming!")
    for _, x in genomes:
        gameLoop(x, config)


def run(config_file):
    print("config_file: ", config_file)
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    p = neat.Population(config)
    # p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-99") # Restore from checkpoints
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(50))
    winner = p.run(eval_genomes, 500)
    print("Winner, ", winner)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)

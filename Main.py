import random
import pygame

x = 230
y = 115
pixel = 5

def home_screen():
    houses = int(input('Houses: '))
    if houses == 69:
        return 60, 10, 320, 20, 20, 5, -1, 1 #type '69' for automatic values
    hospitals = int(input('Hospitals: '))
    humans = int(input('Humans: '))
    infection_length = int(input('Infection length: '))
    infection_recovery = int(input('Infection recovery: '))
    initial_infected = int(input('Initial infected: '))
    hospital_effectiveness = int(input('Hospital effectiveness: '))
    hospital_willingness = int(input('Hospital willingness: '))
    return houses, hospitals, humans, infection_length, infection_recovery, initial_infected, hospital_effectiveness, hospital_willingness

def objective(houses, hospitals, hospital_willingness):
    choice = random.randint(0, 8 + hospital_willingness)
    if choice <= 3:
        return (random.randint(1, x), random.randint(1, y))
    elif choice >= 4 and choice <= 7:
        house_of_choice = random.choice(houses)
        return (house_of_choice[0], house_of_choice[1] + 1)
    elif choice >= 8:
        hospital_of_choice = random.choice(hospitals)
        return (hospital_of_choice[0], hospital_of_choice[1])

def movement(current_position, target, blocks) -> tuple:
    choi = random.randint(0, 15)
    x, y = current_position
    if choi == 0:
        return (0, 0)
    nothing = (0, 0)
    up = (0, -1)
    down = (0, 1)
    left = (-1, 0)
    right = (1, 0)
    down_right = (1, 1)
    down_left = (-1, 1)
    up_right = (1, -1)
    up_left = (-1, -1)
    moves = [nothing, up, down, left, right, down_left, down_right, up_right, up_left]
    closest_move, distance = up, 99999
    for move in moves:
        new_pos = (x + move[0], y + move[1])
        type_shi = abs(target[0] - new_pos[0]) + abs(target[1] - new_pos[1]) #distance from target
        if new_pos not in blocks:
            if type_shi < distance:
                distance = type_shi
                closest_move = move
    return closest_move

def environment(h, ho):
    global x, y
    houses = h
    hospitals = ho

    house_pos = [0 for h in range(houses)]
    hospital_pos = [0 for h in range(hospitals)]

    for idx in range(houses):
        found_coordinates = False
        while not found_coordinates:
            random_location = (random.randint(1, x), random.randint(1, y))
            if random_location not in house_pos and random_location not in hospital_pos:
                found_coordinates = True
                house_pos[idx] = random_location
    for idx in range(hospitals):
        found_coordinates = False
        while not found_coordinates:
            random_location = (random.randint(1, x), random.randint(1, y))
            if random_location not in house_pos and random_location not in hospital_pos:
                found_coordinates = True
                hospital_pos[idx] = random_location

    return house_pos, hospital_pos

def in_contact(my_point, all_infected, sickness, infection_length):
    if sickness > 1:
        return sickness
    x, y = my_point
    up = (x, y - 1)
    down = (x, y + 1)
    left = (x - 1, y)
    right = (x + 1, y)
    if (up in all_infected or
    down in all_infected or
    left in all_infected or
    right in all_infected):
        return sickness + 1
    else:
        return sickness

def main(housess, hospitalss, humanss, infection_length, infection_recovery_chance, initial_infected, hospital_medicine, hospital_willingness):
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((x * pixel, (y + 20) * pixel))
    pygame.display.set_caption('Virus simulator')
    font = pygame.font.SysFont('Arial', 25)

    #COLORS
    BLACK = (0, 0, 0)
    HUMAN = (120, 120, 120)
    WHITE = (255, 255, 255)
    RED = (255, 30, 30)
    BLUE = (20, 20, 230)
    BROWN = (250, 175, 0)
    GREEN = (30, 180, 30)
    screen.fill(BLACK)

    #environment maker
    houses, hospitals = environment(housess, hospitalss)
    for i in range(2):
        result = (houses if i == 1 else hospitals)
        for pos in result:
            cors = pos
            pygame.draw.rect(screen, (BROWN if i == 1 else WHITE), (cors[0] * pixel, cors[1] * pixel,2*pixel,(pixel if i == 1 else 2*pixel)))

    #humans maker
    infected = []
    healthy = []
    recovered = []
    normal = []
    human_pos_block = []
    infected_positions = []
    humans = dict()
    for i in range(humanss):
        breeding = True
        while breeding: #human class breeder
            randi = (random.randint(1, x), random.randint(1, y))
            human_pos_block.append(randi)
            humans[i] = [randi, 1, objective(houses, hospitals, hospital_willingness), 8, 0]    #key = human number.  value = [coordinates, infection level]
            if humans[i][0] not in houses or humans[i][0] not in hospitals:
                breeding = False
    for i in range(humanss + initial_infected):
        infected_positions.append((0, 0))
        infected.append(0)
        healthy.append(0)
        recovered.append(0)
        normal.append(0)
    
    #zombies
    for i in range(initial_infected):
        randi = (random.randint(1, 230), random.randint(1, 130))
        human_pos_block.append(randi)
        humans[humanss + i] = [randi, 2, objective(houses, hospitals, hospital_willingness), 8, 1]  #first human is infected

    for i in range (6969696969696969696969):
        clock.tick(15)

        #Graph over time
        if i > (x * pixel) * 2:
            i = i - ((x * pixel) * 2)
        H = sum(normal) / len(humans) * 19
        G = sum(healthy) / len(humans) * 19
        B = sum(recovered) / len(humans) * 19
        R = sum(infected) / len(humans) * 19
        pygame.draw.rect(screen, HUMAN, pygame.Rect(i / 2, (y + 1) * pixel + 1, pixel, H * pixel))
        pygame.draw.rect(screen, GREEN, pygame.Rect(i / 2, (y + 1) * pixel + 1 + (H * pixel), pixel, G * pixel))
        pygame.draw.rect(screen, BLUE, pygame.Rect(i / 2, (y + 1) * pixel + 1 + (G * pixel) + (H * pixel), pixel, B * pixel + 1))
        pygame.draw.rect(screen, RED, pygame.Rect(i / 2, (y + 1) * pixel + 1 + (G * pixel) + (B * pixel) + (H * pixel), pixel, R * pixel))

        #human statistics
        pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, pixel * 8, pixel * 30))
        letter_surface = font.render((f'{sum(infected)}'), True, (RED))
        screen.blit(letter_surface, (pixel, pixel))
        letter_surface = font.render((f'{sum(healthy)}'), True, (GREEN))
        screen.blit(letter_surface, (pixel, pixel * 8))
        letter_surface = font.render((f'{sum(recovered)}'), True, (BLUE))
        screen.blit(letter_surface, (pixel, pixel * 16))
        letter_surface = font.render((f'{sum(normal)}'), True, (HUMAN))
        screen.blit(letter_surface, (pixel, pixel * 24))

        for i in range(2):  #envi draw
            result = (houses if i == 1 else hospitals)
            for pos in result:
                cors = pos
                pygame.draw.rect(screen, (BROWN if i == 1 else WHITE), (cors[0] * pixel, cors[1] * pixel,2*pixel,(pixel if i == 1 else 2*pixel)))

        for i, human in enumerate(humans.values()): #human loop
            if human[0] in hospitals and human[1] >= hospital_effectiveness:  #if human is at the hospital and not infected
                human[1] = hospital_medicine
                human[4] -= 1

            choi = random.randint(0, infection_recovery_chance)
            if human[2] == human[0]: #if human is at the target
                if human[3] != 0:
                    human[3] -= 1
                else:
                    human[2] = objective(houses, hospitals, hospital_willingness)
                    human[3] = 8

            #human infection
            human[1] = in_contact(human[0], infected_positions, human[1], infection_length)
            if human[1] >= 2 and human[1] != infection_length: #if human is infected
                if choi == 0:
                    human[1] += 1
            elif human[1] == infection_length:  #if human is recovered and not infected
                human[4] -= 1
                human[1] = -1 + human[4]
                infected[i] = 0
            elif human[1] <= 1:
                infected[i] = 0
                infected_positions[i] = (0, 0)
            
            pygame.draw.rect(screen, BLACK, pygame.Rect(human[0][0] * pixel, human[0][1] * pixel, pixel, pixel))
            blocks = (human_pos_block)
            h_x, h_y = movement(human[0], human[2], blocks)
            human_pos_block[i] = (h_x, h_y)
            humans[i][0] = (human[0][0] + h_x, human[0][1] + h_y)
            if human[1] == 1:
                healthy[i] = 0
                recovered[i] = 0
                infected[i] = 0
                normal[i] = 1
                pygame.draw.rect(screen, HUMAN, pygame.Rect(human[0][0] * pixel, human[0][1] * pixel, pixel - 1, pixel - 1))
            elif human[1] <= 0 and human[1] > -3:
                healthy[i] = 1
                recovered[i] = 0
                infected[i] = 0
                normal[i] = 0
                pygame.draw.rect(screen, GREEN, pygame.Rect(human[0][0] * pixel, human[0][1] * pixel, pixel - 1, pixel - 1))
            elif human[1] <= -3:
                recovered[i] = 1
                healthy[i] = 0
                infected[i] = 0
                normal[i] = 0
                infected_positions[i] = (0, 0)
                pygame.draw.rect(screen, BLUE, pygame.Rect(human[0][0] * pixel, human[0][1] * pixel, pixel - 1, pixel - 1))
            else:
                recovered[i] = 0
                healthy[i] = 0
                infected[i] = 1
                normal[i] = 0
                infected_positions[i] = human[0]
                pygame.draw.rect(screen, RED, pygame.Rect(human[0][0] * pixel, human[0][1] * pixel, pixel, pixel))

        for event in pygame.event.get():    #event loop
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                return True

        pygame.display.flip()

if __name__ == '__main__':
    houses, hospitals, humans, infection_length, infection_recovery_chance, initial_infected, hospital_effectiveness, h_w = home_screen()
    while main(houses, hospitals, humans, infection_length, infection_recovery_chance, initial_infected, hospital_effectiveness, h_w):
        main(houses, hospitals, humans, infection_length, infection_recovery_chance, initial_infected, hospital_effectiveness, h_w)
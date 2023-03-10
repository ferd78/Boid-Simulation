# Main Class

from utils import v_sub, boid_pointlist, agent_degree_rotation, limit
from Agent import DEFAULT_SPEED, Agent
from Obstacle import Obstacle
import shared
import domain
import sys
import pygame as pyg

#pygame variables
TITLE = "Flocking Simulation using Boids"
BACKGROUND = (0,0,0)
AGENT_COLOR = [(0,0,255),(255, 165, 0)] # [agent 1, agent 2]
OBSTACLE_COLOR = (250,250,250)
TEXT_COLOR = (255,255,255)
TRI_BASE = [12,10] # [agent 1, agent 2]
TRI_HEIGHT = [18,15] # [agent 1, agent 2]
MAX_AGENT_COUNT = 65

#Initialize Display
shared.init()
pyg.init()
clock = pyg.time.Clock()
screen = pyg.display.set_mode((shared.WIDTH, shared.HEIGHT))
pyg.display.set_caption(TITLE)

def make_agent_inbound():
    for agent in shared.agent_array:
        agent.pos = agent.pos[0] % shared.WIDTH, agent.pos[1] % shared.HEIGHT

#Draws the following specifications on the pygame window screen
def draw_text():
    font = pyg.font.SysFont("consolas",16)
    text_array = [
                  font.render("Clock FPS: {}".format(int(clock.get_fps())),20,TEXT_COLOR),
                  font.render("Clock Ticks: {}".format(pyg.time.get_ticks()),10,TEXT_COLOR),
                  font.render("Boid Count: {}".format(len(shared.agent_array)),20,TEXT_COLOR),
                  font.render("Obstacle Count: {}".format(len(shared.obstacle_array)),20,TEXT_COLOR),
                  font.render("Orange Boid Speed: {}".format(DEFAULT_SPEED + shared.speed_adjustment + 6),20,TEXT_COLOR),
                  font.render("Blue Boid Speed: {}".format(DEFAULT_SPEED + shared.speed_adjustment),20,TEXT_COLOR)
                 ]

    #display "Agents Reached Max" when agent count reaches max
    if MAX_AGENT_COUNT == len(shared.agent_array):
        text_array[2] = font.render("Agent Count: {} (Agents Reached Max)".format(len(shared.agent_array)),20,TEXT_COLOR)

    #display text
    for i in range(len(text_array)):
        text = text_array[i]
        screen.blit(text,(2,3 + i*15))

def draw_agent():
    agent_array_size = len(shared.agent_array)

    for i in range(agent_array_size):
        agent = shared.agent_array[i]
        make_agent_inbound()
        pointlist = boid_pointlist(TRI_BASE[i%2],TRI_HEIGHT[i%2])
        surface = pyg.Surface((TRI_BASE[i%2], TRI_HEIGHT[i%2]), pyg.SRCALPHA).convert_alpha()
        pyg.draw.polygon(surface,AGENT_COLOR[i%2],pointlist, 0)
        rotate = pyg.transform.rotate(surface,-agent_degree_rotation(agent))
        center = v_sub(agent.pos,(TRI_BASE[i%2] / 2, TRI_HEIGHT[i%2] / 2))
        screen.blit(rotate, center)

def draw_obstacle():
    for obs in shared.obstacle_array:
        width = obs.width
        pyg.draw.rect(screen, OBSTACLE_COLOR, (obs.pos[0] - width/2, obs.pos[1] - width/2, width, width), 0)

def run():
    #game loop
    while True:

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                #quit game
                pyg.quit()
                sys.exit()
            elif pyg.key.get_pressed()[pyg.K_c]:
                #clear canvas
                domain.clear_all_item()
            elif pyg.key.get_pressed()[pyg.K_r]:
                #randomize all agents' position
                domain.randomize_position()
            elif pyg.key.get_pressed()[pyg.K_UP]:
                #increase agent speed
                domain.adjust_speed(1)
            elif pyg.key.get_pressed()[pyg.K_DOWN]:
                #decrease agent speed
                domain.adjust_speed(0)
            elif pyg.mouse.get_pressed()[0] and MAX_AGENT_COUNT > len(shared.agent_array):
                # append new agent
                shared.agent_array.append(Agent(pyg.mouse.get_pos()))
            elif pyg.mouse.get_pressed()[2]:
                # append new obstacle
                shared.obstacle_array.append(Obstacle(pyg.mouse.get_pos()))

        screen.fill(BACKGROUND)
        draw_agent()
        draw_obstacle()
        draw_text()

        domain.agent_update()
        pyg.display.update()
        clock.tick(shared.FPS)

run()


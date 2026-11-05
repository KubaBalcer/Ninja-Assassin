import pygame
import sys
import random


# Initialize Pygame
pygame.init()

# Grid settings
ROWS, COLS = 10, 10
CELL_SIZE = 50
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("10x10 Grid")

# Example positions
# obstacles = [(1, 2), (3, 8), (9, 8),(1,8), (1,5), (1,3), (2,6), (2,5), (2,1), (2,2), (3,2),
#               (4,2), (5,2), (6,2), (7,2), (8,2), (4,0), (5,4), (5,5), (5,8), (6,1), (6,4),
#                 (7,2), (8,2), (8,3), (8,5), (8,6), (8,8)]
# enemies = [(0, 0), (4, 4), (9, 4)]

# enemy_one_path = []
# enemy_two_path = []
# enemy_three_path = []

# ninja = [(6, 5)]
# #ambush_spots = [(4, 4), (7, 3)]
# patrol_one = [(0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8), (0,9),
#               (1,9), (2,9), (3,9), (4,9), (5,9), (6,9), (7,9), (7,8), (7,7),
#               (8,7), (9,7), (9,6)]
# patrol_two = [(9,3), (9,2), (9,1), (9,0), (8,0), (7,0), (6,0), (5,0), (5,1),
#                (4,1), (3,1), (3,0), (2,0), (1,0)]
# patrol_three = [(4,3), (5,3), (6,3), (7,3), (7,4), (7,5), (7,6), (7,7), (6,7),
#                  (5,7), (4,7), (4,6), (4,5)]

obstacles = [[1, 2], [3, 8], [9, 8], [1, 8], [1, 5], [1, 3], [2, 6], [2, 5], [2, 1], [2, 2], [3, 2],
             [4, 2], [5, 2], [6, 2], [7, 2], [8, 2], [4, 0], [5, 4], [5, 5], [5, 8], [6, 1], [6, 4],
             [7, 2], [8, 2], [8, 3], [8, 5], [8, 6], [8, 8]]

enemies = [[0, 0], [4, 4], [9, 4]]

enemy_one_path = []
enemy_two_path = []
enemy_three_path = []

ninja = [6, 5]
#ambush_spots = [[4, 4], [7, 3]]

patrol_one = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9],
              [1, 9], [2, 9], [3, 9], [4, 9], [5, 9], [6, 9], [7, 9], [7, 8], [7, 7],
              [8, 7], [9, 7], [9, 6]]

patrol_two = [[9, 3], [9, 2], [9, 1], [9, 0], [8, 0], [7, 0], [6, 0], [5, 0], [5, 1],
              [4, 1], [3, 1], [3, 0], [2, 0], [1, 0]]

patrol_three = [[4, 3], [5, 3], [6, 3], [7, 3], [7, 4], [7, 5], [7, 6], [7, 7], [6, 7],
                [5, 7], [4, 7], [4, 6], [4, 5]]



global patrol_one_count
global patrol_two_count
global patrol_three_count
patrol_one_count = -1
patrol_two_count = -1
patrol_three_count = -1
GameCount = 0


def avoid_obstacle(x, y):
    if [x,y] in obstacles:
        return False
    else:
        return True

def determine_positioning(movelist):
    DangerZone = []
    CurrentPosition = movelist[-1]
    PreviousPosition = movelist[-2]
    CurrentX, CurrentY = CurrentPosition
    PreviousX, PreviousY = PreviousPosition
    if PreviousX + 1 == CurrentX:
        for index in range(0,4): #East
            for ConeIndex in range(1,4):
                if index == 0:
                    DangerZone.append([(CurrentX + ConeIndex),CurrentY])
                else:
                    DangerZone.append([CurrentX + ConeIndex,(CurrentY + index)])
                    DangerZone.append([CurrentX + ConeIndex,(CurrentY - index)])

    elif PreviousX - 1 == CurrentX:
        for index in range(0,4): #West
            for ConeIndex in range(1,4):
                if index == 0:
                    DangerZone.append([(CurrentX - ConeIndex),CurrentY])
                else:
                    DangerZone.append([CurrentX - ConeIndex,(CurrentY + index)])
                    DangerZone.append([CurrentX - ConeIndex,(CurrentY - index)])

    elif PreviousY + 1 == CurrentY:
        for index in range(0,4): #North
            for ConeIndex in range(1,4):
                if index == 0:
                    DangerZone.append([CurrentX,(CurrentY + ConeIndex)])
                else:
                    DangerZone.append([CurrentX + index,(CurrentY + ConeIndex)])
                    DangerZone.append([CurrentX - index,(CurrentY + ConeIndex)])
    
    elif PreviousY - 1 == CurrentY:
        for index in range(0,4): #South
            for ConeIndex in range(1,4):
                if index == 0:
                    DangerZone.append([CurrentX,(CurrentY - ConeIndex)])
                else:
                    DangerZone.append([CurrentX + index,(CurrentY - ConeIndex)])
                    DangerZone.append([CurrentX - index,(CurrentY - ConeIndex)])




def patrol_movement(path,count):
    if count < len(path):
        return path[count]
    elif len(path) <= count < 2*len(path):
        reverse_count = (2 * len(path) - 1) - count
        print(str(reverse_count) + " Vs " + str(len(path)))
        print(str(path[reverse_count]) + " POS")
        #print(reverse_count)
        return path[reverse_count]
    else:
        print(str(count) + " count " + str(len(path)))



def movement(elements):
        #new_positions = []
        #for index in elements:
            #print(index)
            #x, y = index
            x, y = elements
            valid_move = False
            while valid_move == False:
                move = random.randint(1,4)
                if move == 1 and (x+1) < 10 and avoid_obstacle(x+1, y):
                    x += 1
                    valid_move = True
                elif move == 2 and (y+1) < 10 and avoid_obstacle(x, y+1):
                    y += 1
                    valid_move = True
                elif move == 3 and (x-1) > -1 and avoid_obstacle(x-1, y):
                    x -= 1
                    valid_move = True
                elif move == 4 and (y-1) > -1 and avoid_obstacle(x, y-1):
                    y -= 1
                    valid_move = True
            print('random move')
            return [x,y]
            #new_positions.append([x, y])
        #return new_positions

count = 0
clock = pygame.time.Clock()


# def determine_positioning_agent(movelist):
#     DangerZone = []
#     FinalDangerZone = []
#     CurrentPosition = movelist[-1]
#     PreviousPosition = movelist[-2]
#     print(CurrentPosition)
#     CurrentX, CurrentY = CurrentPosition
#     PreviousX, PreviousY = PreviousPosition
#     if PreviousX + 1 == CurrentX:
#         for index in range(0,5): #East
#             for ConeIndex in range(0,5-index):
#                 if index == 0:
#                     DangerZone.append([(CurrentX + ConeIndex),CurrentY])
#                 else:
#                     DangerZone.append([CurrentX + ConeIndex,(CurrentY + index)])
#                     DangerZone.append([CurrentX + ConeIndex,(CurrentY - index)])

#     elif PreviousX - 1 == CurrentX:
#         for index in range(0,5): #West
#             for ConeIndex in range(0,5-index):    
#                 if index == 0:
#                     DangerZone.append([(CurrentX - ConeIndex),CurrentY])
#                 else:
#                     DangerZone.append([CurrentX - ConeIndex,(CurrentY + index)])
#                     DangerZone.append([CurrentX - ConeIndex,(CurrentY - index)])
                

#     elif PreviousY + 1 == CurrentY:
#         for index in range(0,5): #North
#             for ConeIndex in range(0,5-index):
#                 if index == 0:
#                     DangerZone.append([CurrentX,(CurrentY + ConeIndex)])
#                 else:
#                     DangerZone.append([CurrentX + index,(CurrentY + ConeIndex)])
#                     DangerZone.append([CurrentX - index,(CurrentY + ConeIndex)])
    
#     elif PreviousY - 1 == CurrentY:
#         for index in range(0,5): #South
#             for ConeIndex in range(0,5-index):
#                 if index == 0:
#                     DangerZone.append([CurrentX,(CurrentY - ConeIndex)])
#                 else:
#                     DangerZone.append([CurrentX + index,(CurrentY - ConeIndex)])
#                     DangerZone.append([CurrentX - index,(CurrentY - ConeIndex)])
#     # print('before dangerzone ' + str(DangerZone))
#     for AddedNode in DangerZone:
#         AddedNode_x,AddedNode_y = AddedNode
#         if not (AddedNode_x < 0 or AddedNode_y < 0 or AddedNode_x > 9 or AddedNode_y > 9):
#             if AddedNode not in obstacles:
#                 FinalDangerZone.append(AddedNode)
#     # print('after dangerzone: ' + str(FinalDangerZone))
#     if CurrentPosition in FinalDangerZone:
#         FinalDangerZone.remove(CurrentPosition)
#     return FinalDangerZone

def determine_positioning_agent(movelist):
    CurrentPosition = movelist[-1]
    PreviousPosition = movelist[-2]

    CurrentX, CurrentY = CurrentPosition
    PreviousX, PreviousY = PreviousPosition

    # Determine direction
    if CurrentX == PreviousX + 1:
        direction = "EAST"
    elif CurrentX == PreviousX - 1:
        direction = "WEST"
    elif CurrentY == PreviousY + 1:
        direction = "NORTH"
    elif CurrentY == PreviousY - 1:
        direction = "SOUTH"
    else:
        return []  # no movement → no vision

    FinalDangerZone = []

    # Raycast helper
    def add_if_visible(x, y):
        if not (0 <= x <= 9 and 0 <= y <= 9):
            return False  # out of bounds → stop ray
        if [x, y] in obstacles:
            return False  # obstacle blocks further tiles
        FinalDangerZone.append([x, y])
        return True  # continue ray

    # Build cone with raycasting
    for dist in range(1, 5):  # distance 1 to 4
        for side in range(-(dist), dist + 1):
            if direction == "EAST":
                x = CurrentX + dist
                y = CurrentY + side
            elif direction == "WEST":
                x = CurrentX - dist
                y = CurrentY + side
            elif direction == "NORTH":
                x = CurrentX + side
                y = CurrentY + dist
            elif direction == "SOUTH":
                x = CurrentX + side
                y = CurrentY - dist

            # Raycast: stop if obstacle blocks this line
            if not add_if_visible(x, y):
                continue

    # Remove agent tile if present
    if CurrentPosition in FinalDangerZone:
        FinalDangerZone.remove(CurrentPosition)

    return FinalDangerZone

def determine_positioning_enemy(movelist):
    DangerZone = []
    CurrentPosition = movelist[-1]
    PreviousPosition = movelist[-2]
    CurrentX, CurrentY = CurrentPosition
    PreviousX, PreviousY = PreviousPosition
    if PreviousX + 1 == CurrentX:
        for index in range(0,3): #East
            for ConeIndex in range(0,3-index):
                if index == 0:
                    DangerZone.append([(CurrentX + ConeIndex),CurrentY])
                else:
                    DangerZone.append([CurrentX + ConeIndex,(CurrentY + index)])
                    DangerZone.append([CurrentX + ConeIndex,(CurrentY - index)])

    elif PreviousX - 1 == CurrentX:
        for index in range(0,3): #West
            for ConeIndex in range(0,3-index):    
                if index == 0:
                    DangerZone.append([(CurrentX - ConeIndex),CurrentY])
                else:
                    DangerZone.append([CurrentX - ConeIndex,(CurrentY + index)])
                    DangerZone.append([CurrentX - ConeIndex,(CurrentY - index)])
                

    elif PreviousY + 1 == CurrentY:
        for index in range(0,3): #North
            for ConeIndex in range(0,3-index):
                if index == 0:
                    DangerZone.append([CurrentX,(CurrentY + ConeIndex)])
                else:
                    DangerZone.append([CurrentX + index,(CurrentY + ConeIndex)])
                    DangerZone.append([CurrentX - index,(CurrentY + ConeIndex)])
    
    elif PreviousY - 1 == CurrentY:
        for index in range(0,3): #South
            for ConeIndex in range(0,3-index):
                if index == 0:
                    DangerZone.append([CurrentX,(CurrentY - ConeIndex)])
                else:
                    DangerZone.append([CurrentX + index,(CurrentY - ConeIndex)])
                    DangerZone.append([CurrentX - index,(CurrentY - ConeIndex)])
    #print('danger check')
    # for IsLegalCoordinate in DangerZone:
    #     IsLegalCoordinate_x, IsLegalCoordinate_y = IsLegalCoordinate
    #     if IsLegalCoordinate_x < 0 or IsLegalCoordinate_y < 0 or IsLegalCoordinate_x > 9 or IsLegalCoordinate_y > 9:
    #         DangerZone.remove(IsLegalCoordinate)
    DangerZone = [coord for coord in DangerZone if 0 <= coord[0] <= 9 and 0 <= coord[1] <= 9]
    #print('danger result = ' + str(DangerZone))

    if CurrentPosition in DangerZone:
        DangerZone.remove(CurrentPosition)
    return DangerZone

def facing_where(tilepos,agentpos):
    agentpos_x, agentpos_y = agentpos
    tilepos_x, tilepos_y = tilepos
    option = 'none at all'
    for delta in range(0,10):
        if delta + tilepos_x == agentpos_x and agentpos_y == tilepos_y:
            option = 'West'
        elif delta + tilepos_y == agentpos_y and agentpos_x == tilepos_x:
            option = 'North'
        elif tilepos_x - delta == agentpos_x and agentpos_y == tilepos_y:
            option = 'East'
        elif tilepos_y - delta == agentpos_y and agentpos_x == tilepos_x:
            option = 'South'
    return option

def determine_vision(VisibleSquaresList,AgentPosition):
    vision = []
    obstaclesused = []
    for square in VisibleSquaresList:
        square_x, square_y = square
        if not (square_x > 9 or square_x < 0 or square_y > 9 or square_y < 0):
            vision.append(square)
    visible = []
    #print(AgentPosition)
    AgentX, AgentY = AgentPosition
    for tile in vision:
        tile_x, tile_y = tile
        blocked = False
        TileDistanceToAgent_x = abs(tile_x - AgentX)
        TileDistanceToAgent_y = abs(tile_y - AgentY)

        for obstacle in obstacles:
            obstacle_x, obstacle_y = obstacle
            ObstacleDistanceToAgent_x = abs(obstacle_x - AgentX)
            ObstacleDistanceToAgent_y = abs(obstacle_y - AgentY)
            if ObstacleDistanceToAgent_x <= TileDistanceToAgent_x and ObstacleDistanceToAgent_y <= TileDistanceToAgent_y:
                if obstacle not in vision:
                    continue
                if obstacle not in obstaclesused:
                    obstaclesused.append(obstacle)

                same_line = (
                    (obstacle_x == AgentX == tile_x and facing_where(obstacle,AgentPosition) == facing_where(tile,AgentPosition)) or
                    (obstacle_y == AgentY == tile_y and facing_where(obstacle,AgentPosition) == facing_where(tile,AgentPosition)) or
                    ((obstacle_x == tile_x and facing_where(obstacle,AgentPosition) == facing_where(tile,AgentPosition) and (AgentY != obstacle_y) and
                      ((tile_y > AgentY and obstacle_y > AgentY) or (tile_y < AgentY and obstacle_y < AgentY)))
                    ) or
                    ((obstacle_y == tile_y and facing_where(obstacle,AgentPosition) == facing_where(tile,AgentPosition)) and (AgentX != obstacle_x) and
                      ((tile_x > AgentX and obstacle_x > AgentX) or (tile_x < AgentX and obstacle_x < AgentX))
                    ) or
                    (ObstacleDistanceToAgent_x == ObstacleDistanceToAgent_y and 
                        TileDistanceToAgent_x == TileDistanceToAgent_y  and (((tile_y > AgentY and 
                        obstacle_y > AgentY) or (tile_y < AgentY and obstacle_y < AgentY)) and ((tile_x > AgentX and 
                        obstacle_x > AgentX) or (tile_x < AgentX and obstacle_x < AgentX))))
                    )
                    #(abs(ObstacleDistanceToAgent_x - ObstacleDistanceToAgent_y) <= 1)
                #)

                if same_line:
                    blocked = True
                    # print('')
                    # print('for ' + str(tile) + 'with obstacle: ' + str(obstacle) + ' with agent ' + str(AgentPosition))

                    # print('same x(agent) and facing same way ' + str(obstacle_x == AgentX == tile_x and
                    #     facing_where(obstacle,AgentPosition) == facing_where(tile,AgentPosition)))
                    # print('same y(agent) same direction ' + str(obstacle_y == AgentY == tile_y and 
                    #     facing_where(obstacle,AgentPosition) == facing_where(tile,AgentPosition)))
                    # print('on same x, face same direction, between agent ' + str(obstacle_x == tile_x and 
                    #     facing_where(obstacle,AgentPosition) == facing_where(tile,AgentPosition) and (AgentY != obstacle_y) and 
                    #     ((tile_y > AgentY and obstacle_y > AgentY) or (tile_y < AgentY and obstacle_y < AgentY))))
                    # print('on same y, face some direction, between agent')
                    # print(str((obstacle_y == tile_y and facing_where(obstacle,AgentPosition) == facing_where(tile,AgentPosition))) and (AgentX != obstacle_x) and 
                    #     ((tile_x > AgentX and obstacle_x > AgentX) or (tile_x < AgentX and obstacle_x < AgentX)))
                    # print('diagonals, between agent ' + str(ObstacleDistanceToAgent_x == ObstacleDistanceToAgent_y and 
                    #     TileDistanceToAgent_x == TileDistanceToAgent_y  and (((tile_y > AgentY and 
                    #     obstacle_y > AgentY) or (tile_y < AgentY and obstacle_y < AgentY)) and ((tile_x > AgentX and 
                    #     obstacle_x > AgentX) or (tile_x < AgentX and obstacle_x < AgentX)))
                    #     )
                    #         )
                    #             #)
                    # print('')

                    break

        if not blocked:
            visible.append(tile)
    # print('obstacles below')
    # print(obstaclesused)
    # print('-----')
    return visible


#   #  ###   ###  ###   ###   #   #
#   #   #   #      #   #   #  ##  #
#   #   #    ###   #   #   #  # # #
 # #    #       #  #   #   #  #  ##
  #    ###  ####  ###   ###   #   #

  #    ####   ###  #   #  #####
 # #   #   # #   # #   #  #    
#####  ####  #   # #   #  #### 
#   #  #   # #   #  # #   #    
#   #  ####   ###    #    #####


def map_navigation_route(vision,DestinationNode,CurrentLocation):
    CompletePath = []
    while DestinationNode not in CompletePath:
        ReachableTiles = []
        for node in vision:
            node_x, node_y = node
            CurrentLocation_x, CurrentLocation_y = CurrentLocation
            if abs(node_x - CurrentLocation_x) < 2 and abs(node_y - CurrentLocation_y) < 2 and node not in obstacles:
                ReachableTiles.append(node)
        # print(ReachableTiles)
        ClosestNodeValue = 100
        ClosestNode = [0,0]
        DestinationNode_x, DestinationNode_y = DestinationNode
        for PotentialStep in ReachableTiles:
            PotentialStep_x, PotentialStep_y = PotentialStep
            if abs(abs(PotentialStep_x - DestinationNode_x) + abs(PotentialStep_y - DestinationNode_y)) < ClosestNodeValue:
                ClosestNodeValue = abs(abs(PotentialStep_x - DestinationNode_x) + abs(PotentialStep_y - DestinationNode_y))
                ClosestNode = PotentialStep
        CompletePath.append(ClosestNode)
        CurrentLocation = ClosestNode
    return CompletePath

def map_navigation(vision,DestinationNode,CurrentLocation):
    ReachableTiles = []
    for node in vision:
        node_x, node_y = node
        CurrentLocation_x, CurrentLocation_y = CurrentLocation
        if abs(node_x - CurrentLocation_x) < 2 and abs(node_y - CurrentLocation_y) < 2 and node not in obstacles:
            ReachableTiles.append(node)
    # print(ReachableTiles)
    ClosestNodeValue = 100
    ClosestNode = [0,0]
    DestinationNode_x, DestinationNode_y = DestinationNode
    for PotentialStep in ReachableTiles:
        PotentialStep_x, PotentialStep_y = PotentialStep
        if abs(abs(PotentialStep_x - DestinationNode_x) + abs(PotentialStep_y - DestinationNode_y)) < ClosestNodeValue:
            ClosestNodeValue = abs(abs(PotentialStep_x - DestinationNode_x) + abs(PotentialStep_y - DestinationNode_y))
            ClosestNode = PotentialStep
    return ClosestNode

def should_agent_escape(RecentPathOfEnemies,RecentPathOfAgent,AgentPosition):

    FirstEscapeNodes = []
    SecondEscapeNodes = []
    newpath = [AgentPosition]
    AgentNewPosition = [0,0]
    AgentFinalPosition = [0,0]
    Escape = False
    for EnemyPath in RecentPathOfEnemies:
        enemyvision = determine_positioning_enemy(EnemyPath)
        print('the enemy vision is ' + str(enemyvision))
        if AgentPosition in enemyvision:
            Escape = True
            agentvision = determine_positioning_agent(RecentPathOfAgent)
            print('agent vision is' + str(agentvision))
            for AgentPath in agentvision:
                if AgentPath not in enemyvision and AgentPath not in obstacles:
                    FirstEscapeNodes.append(AgentPath)
                else:
                    print('cannot escape')
                    FirstEscapeNodes.append([6,5])
                    break
    print('hehe')
    print('the escape nodes: ' + str(FirstEscapeNodes))
    if Escape == True:
        #print(FirstEscapeNodes)
        AgentNewPosition = FirstEscapeNodes[0]
        AgentNewPosition_x,AgentNewPosition_y = AgentNewPosition
        for node in FirstEscapeNodes: 
            node_x,node_y = node
            AgentPosition_x,AgentPosition_y = AgentPosition
            if abs(abs(node_x - AgentPosition_x) + abs(node_y - AgentPosition_y)) > abs(abs(AgentPosition_x - AgentNewPosition_x) + abs(AgentPosition_y - AgentNewPosition_y)):
                AgentNewPosition = node
        newpath.append(AgentNewPosition)
        TheNewPath = map_navigation_route(agentvision,newpath[1],newpath[0])
        AgentSecondVisionList = determine_positioning_agent(TheNewPath)
        AgentFinalPosition = AgentSecondVisionList[0]
        for cell in AgentSecondVisionList:
            if cell not in enemyvision and cell not in obstacles:
                SecondEscapeNodes.append(cell)
        for coordinate in SecondEscapeNodes:
            coordinate_x,coordinate_y = coordinate
            AgentFinalPosition_x,AgentFinalPosition_y = AgentFinalPosition
            if abs(abs(coordinate_x - AgentNewPosition_x) + abs(coordinate_y - AgentNewPosition_y)) > abs(abs(AgentNewPosition_x - AgentFinalPosition_x) + abs(AgentNewPosition_y - AgentFinalPosition_y)):
                AgentFinalPosition = coordinate
        return [AgentNewPosition,AgentFinalPosition]

def should_enemy_chase(RecentPathOfEnemies,RecentPathOfAgent,AgentPosition):
    Escape = False
    VisionOfEnemyX = []
    ChasingEnemies = []
    for EnemyPath in RecentPathOfEnemies:
        enemyvision = determine_positioning_enemy(EnemyPath)
        if AgentPosition in enemyvision:
            Escape = True
            VisionOfEnemyX.append([EnemyPath[0],enemyvision,EnemyPath[-1]])
    if Escape == True:
        for EnemyID, EnemyPerception, CurrentEnenmyPosition in VisionOfEnemyX:
            PathToFollow = map_navigation_route(EnemyPerception,AgentPosition,CurrentEnenmyPosition)
            ChasingEnemies.append(EnemyID,PathToFollow)
    return ChasingEnemies

def within_assassination_range(TargetLoc,ExecutionerLoc):
    TargetLoc_x, TargetLoc_y = TargetLoc
    ExecutionerLoc_x, ExecutionerLoc_y = ExecutionerLoc
    Within_Range = False
    if TargetLoc_x + 1 == ExecutionerLoc_x:
        Within_Range = True
    elif TargetLoc_x - 1 == ExecutionerLoc_x:
        Within_Range = True
    elif TargetLoc_y + 1 == ExecutionerLoc_y:
        Within_Range = True
    elif TargetLoc_y - 1 == ExecutionerLoc_y:
        Within_Range = True


    if TargetLoc_x + 1 == ExecutionerLoc_x and TargetLoc_y + 1 == ExecutionerLoc_y:
            Within_Range = False
    elif TargetLoc_x - 1 == ExecutionerLoc_x and TargetLoc_y - 1 == ExecutionerLoc_y:
            Within_Range = False
    elif TargetLoc_x + 1 == ExecutionerLoc_x and TargetLoc_y - 1 == ExecutionerLoc_y:
            Within_Range = False
    elif TargetLoc_x - 1 == ExecutionerLoc_x and TargetLoc_y + 1 == ExecutionerLoc_y:
            Within_Range = False

    return Within_Range

def kill_target(RecentPathOfEnemies,RecentPathOfAgent,Vision,TeamName):
    killed_charachters = []
    AgentPos = RecentPathOfAgent[-1]
    AgentPosBefore = RecentPathOfAgent[-2]
    if TeamName == 'Agent':
        EnemyLocations = []
        for loc in RecentPathOfEnemies:
            EnemyLocations.append([loc[-1],loc[-2]])
        for EnemyPos, EnemyPosBefore in EnemyLocations:
            if EnemyPos in Vision and within_assassination_range(EnemyPos,AgentPos) == True and(facing_where(EnemyPosBefore,EnemyPos) == facing_where(AgentPosBefore,AgentPos)):
                killed_charachters.append(EnemyPos)
    elif TeamName == 'Enemies':
        EnemyLocations = []
        print(RecentPathOfEnemies)
        # for loc in RecentPathOfEnemies:
        #     EnemyLocations.append([loc[-1],loc[-2]])
        EnemyPos = RecentPathOfEnemies[-1]
        EnemyPosBefore = RecentPathOfEnemies[-2]
        print(EnemyLocations)
        # for EnemyPos, EnemyPosBefore in EnemyLocations:
        #     print('agent pos is ' + str(AgentPos) + ' | and enemy pos is ' + str(EnemyPos))
        #     if AgentPos in Vision and within_assassination_range(AgentPos,EnemyPos) == True and(facing_where(EnemyPosBefore,EnemyPos) == facing_where(AgentPosBefore,AgentPos)):
        #         killed_charachters.append(AgentPos)
        if AgentPos in Vision and within_assassination_range(AgentPos,EnemyPos) == True and(facing_where(EnemyPosBefore,EnemyPos) == facing_where(AgentPosBefore,AgentPos)):
                        killed_charachters.append(AgentPos)
                        print('HES DEAD NOOOOOOOOOOOOOOOOOO')
    return killed_charachters




# Game loop

NinjaMoveList = []
EscapeNodes = []
EnemyOnePursuitOfNinja = []
EnemyTwoPursuitOfNinja = []
EnemyThreePursuitOfNinja = []
AgentDead = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)

    # Draw grid lines
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

    # Draw obstacles
    for col, row in obstacles:
        pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw enemies
    for col, row in enemies:
        #print(str(col) + " and " + str(row))
        #print("UNSEEN")
        pygame.draw.rect(screen, RED, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw ninja
    print(ninja)#ninja[0][0] and ninja[0][1]
    pygame.draw.rect(screen, BLUE, (ninja[0] * CELL_SIZE, ninja[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    


    clock.tick(1)
    patrol_one_count += 1
    patrol_two_count += 1
    patrol_three_count += 1

    if patrol_one_count > ((2*len(patrol_one)) - 1) :
        patrol_one_count = 0
        print("ERROR 1")
        #print("count is " + str(patrol_one_count))
    if patrol_two_count > ((2*len(patrol_two)) - 1):
        print("ERROR 2" + str(enemies[1]))
        print(patrol_two_count)
        patrol_two_count = 0
        print(" NEWER " + str(patrol_two_count))
    if patrol_three_count > ((2*len(patrol_three)) - 1):
        print("ERROR 3" + str(enemies[2]))
        #print(patrol_three_count)
        patrol_three_count = 0
        print(" NEW " + str(patrol_three_count))


    ###    ####    ####    #       #   ######
    #  #   #  #   #    #    #     #    #
    #   # #   #   #    #     #   #     ######
    #    #    #   #    #      # #      #
    #         #    ####        #       ######

    if [67,67] not in NinjaMoveList and GameCount > 1 and AgentDead == False:
        NinjaMoveList.append(ninja)
        print(str(NinjaMoveList) + ' game count is ' + str(GameCount))
        NinjaVision = determine_vision(determine_positioning_agent(NinjaMoveList),ninja)
        dead_charachters = kill_target([enemy_one_path,enemy_two_path,enemy_three_path],NinjaMoveList,NinjaVision,'Agent')
        if dead_charachters is not None:
            for charachter in dead_charachters:
                if charachter in enemy_one_path:
                    enemy_one_path.append([67,67])
                if charachter in enemy_two_path:
                    enemy_two_path.append([67,67])
                if charachter in enemy_three_path:
                    enemy_three_path.append([67,67])

        if len(enemy_one_path) > 1:
            ShouldAgentEscapeEnemies = should_agent_escape([enemy_one_path,enemy_two_path,enemy_three_path],NinjaMoveList,ninja)
        if ShouldAgentEscapeEnemies is not None and len(EscapeNodes) == 0:
            EscapeNodes = ShouldAgentEscapeEnemies

        if ShouldAgentEscapeEnemies is None and len(EscapeNodes) == 0:
            if enemies[0] in NinjaVision:
                ninja = map_navigation(NinjaVision,enemies[0],ninja)
            elif enemies[1] in NinjaVision:
                    ninja = map_navigation(NinjaVision,enemies[1],ninja)
            elif enemies[2] in NinjaVision:
                    ninja = map_navigation(NinjaVision,enemies[2],ninja)
            else:
                ninja = movement(ninja)
        else:
            if ninja in EscapeNodes:
                EscapeNodes.remove(ninja)
            ninja = map_navigation(NinjaVision,EscapeNodes[0],ninja)
    elif [67,67] not in NinjaMoveList and AgentDead == False:
        NinjaMoveList.append(ninja)
        ninja = movement(ninja)
    else:
        print('GAME OVER')
        print('Ninja: ' + str(NinjaMoveList))
        print('Ninja can see '  + str(NinjaVision))
        print('Enemy One: ' + str(enemy_one_path))
        print('Enemy Two: ' + str(enemy_two_path))
        print('Enemy Three: ' + str(enemy_three_path))
        AgentDead == True
        break
        


    if [67,67] not in enemy_one_path and GameCount > 2:
        EnemyOneVision = determine_vision(determine_positioning_enemy(enemy_one_path),enemies[0])
        enemy_one_path.append(enemies[0])
        dead_ninja = kill_target(enemy_one_path,NinjaMoveList,EnemyOneVision,'Enemies')
        if len(dead_ninja) != 0: #is not None:
            NinjaMoveList.append([67,67])
            print('ninja is dead ' + str(dead_ninja))
            print(NinjaMoveList)
            print('gap')
            AgentDead == True
        if ninja in EnemyOneVision and len(EnemyOnePursuitOfNinja) == 0:
            EnemyOnePursuitOfNinja = map_navigation_route(EnemyOneVision,enemies[0],ninja)
        if len(EnemyOnePursuitOfNinja) != 0:
            enemies[0] = EnemyOnePursuitOfNinja[0]
            EnemyOnePursuitOfNinja.remove(enemies[0])
        if len(EnemyOnePursuitOfNinja) == 0 and ninja not in EnemyOneVision:
            enemies[0] = patrol_movement(patrol_one,patrol_one_count)
    elif [67,67] not in enemy_one_path:
        enemy_one_path.append(enemies[0])
        enemies[0] = patrol_movement(patrol_one,patrol_one_count)

    if [67,67] not in enemy_two_path and GameCount > 2:
        EnemyTwoVision = determine_vision(determine_positioning_enemy(enemy_two_path),enemies[1])
        enemy_two_path.append(enemies[1])
        dead_ninja = kill_target(enemy_two_path,NinjaMoveList,EnemyTwoVision,'Enemies')
        if len(dead_ninja) != 0:# is not None:
            NinjaMoveList.append([67,67])
            AgentDead == True
        if ninja in EnemyTwoVision and len(EnemyTwoPursuitOfNinja) == 0:
            EnemyTwoPursuitOfNinja = map_navigation_route(EnemyTwoVision,enemies[1],ninja)
        if len(EnemyTwoPursuitOfNinja) != 0:
            enemies[1] = EnemyTwoPursuitOfNinja[0]
            EnemyTwoPursuitOfNinja.remove(enemies[1])
        if len(EnemyTwoPursuitOfNinja) == 0 and ninja not in EnemyTwoVision:
            enemies[1] = patrol_movement(patrol_two,patrol_two_count)
    elif [67,67] not in enemy_two_path:
        enemy_two_path.append(enemies[1])
        enemies[1] = patrol_movement(patrol_two,patrol_two_count)

    if [67,67] not in enemy_three_path and GameCount > 2:
        EnemyThreeVision = determine_vision(determine_positioning_enemy(enemy_three_path),enemies[2])
        enemy_three_path.append(enemies[2])
        dead_ninja = kill_target(enemy_three_path,NinjaMoveList,EnemyThreeVision,'Enemies')
        if len(dead_ninja) != 0:# is not None:
            NinjaMoveList.append([67,67])
            AgentDead == True
        if ninja in EnemyThreeVision and len(EnemyThreePursuitOfNinja) == 0:
            EnemyThreePursuitOfNinja = map_navigation_route(EnemyThreeVision,enemies[2],ninja)
        if len(EnemyThreePursuitOfNinja) != 0:
            enemies[2] = EnemyThreePursuitOfNinja[0]
            EnemyThreePursuitOfNinja.remove(enemies[2])
        if len(EnemyThreePursuitOfNinja) == 0 and ninja not in EnemyThreeVision:
            enemies[2] = patrol_movement(patrol_three,patrol_three_count)
    elif [67,67] not in enemy_three_path:
        enemy_three_path.append(enemies[2])
        enemies[2] = patrol_movement(patrol_three,patrol_three_count)

    if AgentDead == True:
        break


    GameCount += 1
    pygame.display.flip()

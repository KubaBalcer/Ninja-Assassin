import random
obstacles = [
    [1, 2], [3, 8], [9, 8], [1, 8], [1, 5], [1, 3], [2, 6], [2, 5], [2, 1], [2, 2], [3, 2],
    [4, 2], [5, 2], [6, 2], [7, 2], [8, 2], [4, 0], [5, 4], [5, 5], [5, 8], [6, 1], [6, 4],
    [7, 2], [8, 2], [8, 3], [8, 5], [8, 6], [8, 8]
]


def determine_positioning_agent(movelist):
    DangerZone = []
    FinalDangerZone = []
    CurrentPosition = movelist[-1]
    PreviousPosition = movelist[-2]
    CurrentX, CurrentY = CurrentPosition
    PreviousX, PreviousY = PreviousPosition
    if PreviousX + 1 == CurrentX:
        for index in range(0,5): #East
            for ConeIndex in range(0,5-index):
                if index == 0:
                    DangerZone.append([(CurrentX + ConeIndex),CurrentY])
                else:
                    DangerZone.append([CurrentX + ConeIndex,(CurrentY + index)])
                    DangerZone.append([CurrentX + ConeIndex,(CurrentY - index)])

    elif PreviousX - 1 == CurrentX:
        for index in range(0,5): #West
            for ConeIndex in range(0,5-index):    
                if index == 0:
                    DangerZone.append([(CurrentX - ConeIndex),CurrentY])
                else:
                    DangerZone.append([CurrentX - ConeIndex,(CurrentY + index)])
                    DangerZone.append([CurrentX - ConeIndex,(CurrentY - index)])
                

    elif PreviousY + 1 == CurrentY:
        for index in range(0,5): #North
            for ConeIndex in range(0,5-index):
                if index == 0:
                    DangerZone.append([CurrentX,(CurrentY + ConeIndex)])
                else:
                    DangerZone.append([CurrentX + index,(CurrentY + ConeIndex)])
                    DangerZone.append([CurrentX - index,(CurrentY + ConeIndex)])
    
    elif PreviousY - 1 == CurrentY:
        for index in range(0,5): #South
            for ConeIndex in range(0,5-index):
                if index == 0:
                    DangerZone.append([CurrentX,(CurrentY - ConeIndex)])
                else:
                    DangerZone.append([CurrentX + index,(CurrentY - ConeIndex)])
                    DangerZone.append([CurrentX - index,(CurrentY - ConeIndex)])
    # print('before dangerzone ' + str(DangerZone))
    for AddedNode in DangerZone:
        AddedNode_x,AddedNode_y = AddedNode
        if not (AddedNode_x < 0 or AddedNode_y < 0 or AddedNode_x > 9 or AddedNode_y > 9):
            FinalDangerZone.append(AddedNode)
    # print('after dangerzone: ' + str(FinalDangerZone))
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
                    print('')
                    print('for ' + str(tile) + 'with obstacle: ' + str(obstacle) + ' with agent ' + str(AgentPosition))

                    print('same x(agent) and facing same way ' + str(obstacle_x == AgentX == tile_x and
                        facing_where(obstacle,AgentPosition) == facing_where(tile,AgentPosition)))
                    print('same y(agent) same direction ' + str(obstacle_y == AgentY == tile_y and 
                        facing_where(obstacle,AgentPosition) == facing_where(tile,AgentPosition)))
                    print('on same x, face same direction, between agent ' + str(obstacle_x == tile_x and 
                        facing_where(obstacle,AgentPosition) == facing_where(tile,AgentPosition) and (AgentY != obstacle_y) and 
                        ((tile_y > AgentY and obstacle_y > AgentY) or (tile_y < AgentY and obstacle_y < AgentY))))
                    print('on same y, face some direction, between agent')
                    print(str((obstacle_y == tile_y and facing_where(obstacle,AgentPosition) == facing_where(tile,AgentPosition))) and (AgentX != obstacle_x) and 
                        ((tile_x > AgentX and obstacle_x > AgentX) or (tile_x < AgentX and obstacle_x < AgentX)))
                    print('diagonals, between agent ' + str(ObstacleDistanceToAgent_x == ObstacleDistanceToAgent_y and 
                        TileDistanceToAgent_x == TileDistanceToAgent_y  and (((tile_y > AgentY and 
                        obstacle_y > AgentY) or (tile_y < AgentY and obstacle_y < AgentY)) and ((tile_x > AgentX and 
                        obstacle_x > AgentX) or (tile_x < AgentX and obstacle_x < AgentX)))
                        )
                            )
                                #)
                    print('')

                    break

        if not blocked:
            visible.append(tile)
    print('obstacles below')
    print(obstaclesused)
    print('-----')
    return visible

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
        if AgentPosition in enemyvision:
            Escape = True
            agentvision = determine_positioning_agent(RecentPathOfAgent)
            for AgentPath in agentvision:
                if AgentPath not in enemyvision and AgentPath not in obstacles:
                    FirstEscapeNodes.append(AgentPath)
    if Escape == True:
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
        for loc in RecentPathOfEnemies:
            EnemyLocations.append([loc[-1],loc[-2]])
        for EnemyPos, EnemyPosBefore in EnemyLocations:
            if AgentPos in Vision and within_assassination_range(AgentPos,EnemyPos) == True and(facing_where(EnemyPosBefore,EnemyPos) == facing_where(AgentPosBefore,AgentPos)):
                killed_charachters.append(AgentPos)
    return killed_charachters


# movingpattern = [[7,4], [7,5], [6,5]]
movingpattern = [[7,3], [7,4]]

exmplist = [[5,6],[5,7],[4,7]]

enemy1movement = [[6,0],[7,0]]
enemy2movement = [[8,7],[9,7]]
enemy3movement = [[4,7],[4,6]]
enemymovelist = [enemy1movement,enemy2movement,enemy3movement]
agentpath = [[4,3],[4,4]]
if should_agent_escape(enemymovelist,agentpath,[4,4]) is not None:
    print(should_agent_escape(enemymovelist,agentpath,[4,4]))
    print('done')
# dangerlist = determine_positioning_agent(movingpattern)
# #dangerlist = determine_positioning_enemy(movingpattern)
# print(dangerlist)
# print('DUN DUN DUN')
# # print(determine_vision(dangerlist,[7,4]))
# print(map_navigation(dangerlist,[3,7],[7,4]))



















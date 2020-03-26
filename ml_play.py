"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    ball_y=399
    ball_x=50
    #pre_ball_x = 100  ##初始化預測結果位置
    #pre_ball_y = 399
    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        if not ball_served: ##如果球沒有發射的話就往左邊發射
            
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            print(1)
            ball_served = True
        else:

            dir_x=ball_x-scene_info.ball[0] ##上一個球的位置-目前球的位置為方向,負往右正往左
            #print(scene_info,ball)
            dir_y=ball_y-scene_info.ball[1] ##負往下正往上
            '''if dir_x==0:
                slope=0
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            else:
                slope = dir_y / dir_x ##斜率
            '''
            ball_x = scene_info.ball[0] ##目前(x,y)
            ball_y = scene_info.ball[1]
            platform_x = scene_info.platform[0] + 20

            pre_ball_x=ball_x
            pre_ball_y=ball_y
            if dir_y < 0:##球向下才要預測
                if ball_y > 125:#開始預測
                    while pre_ball_y<400:
                            pre_ball_x -= dir_x
                            pre_ball_y -= dir_y
                    
                    if pre_ball_x >= 200:
                        pre_ball_x = 400 - pre_ball_x
                        dir_x= 0 - dir_x
                    elif pre_ball_x <= 0:
                        pre_ball_x = 0 - pre_ball_x
                        dir_x= 0 - dir_x
                    
                        ''' 
                        if pre_ball_x >= 200:
                            if pre_ball_x >=600:
                                pre_ball_x -= 400
                            else:
                                pre_ball_x = pre_ball_x - 200
                                dir_x= 0 - dir_x
                        elif pre_ball_x <= 0:
                            if pre_ball_x <= -200:
                                pre_ball_x += 400
                            else:
                                pre_ball_x = 0 - pre_ball_x
                                dir_x= 0 - dir_x
                    
                    
                    
                     while pre_ball_y<400:
                        if pre_ball_x > 0 and pre_ball_x < 200 :
                            pre_ball_x -= dir_x
                            pre_ball_y -= dir_y
                        else:
                            if pre_ball_x >=200:
                                #pre_ball_x = 400-(pre_ball_x-dir_x)
                                pre_ball_x = 400 - pre_ball_x
                                pre_ball_y -= dir_y
                                dir_x= 0 - dir_x
                            else:
                                pre_ball_x = dir_x+pre_ball_x
                                #pre_ball_x += dir_x
                                pre_ball_y -= dir_y
                                dir_x = 0 - dir_x
                    
                    if pre_ball_x > platform_x:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                    elif pre_ball_x < platform_x:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    else:
                        comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                    '''
            else :#球往上不預測
                if platform_x < 100:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                elif platform_x >100:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                else:
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE)



                
            


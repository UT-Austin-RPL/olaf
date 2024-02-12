# the "initial" system prompt to simulate chatGPT behavior.
system_prompt_behavior = """
You are a helpful assistant who is good at employing math and computer science tools to arrive at the solution. 
You analyze numerical values carefully and think step by step.
"""

system_prompt_behavior_human = """
You are a helpful assistant who is good at employing math and computer science tools to arrive at the solution. 
You analyze numerical values carefully and think step by step. 
You will also pay close attention to the human language correction, interpret the human intention, and use it to arrive at the solution.
Please describe in detail how you apply your mathematical and computational abilities, to arrive at solutions.
"""

prompt_robot = """
You have a robot arm which is the Franka Emika Panda robot arm, a single robot arm with 7 degrees of freedom.
The robot a parallel-jaw gripper equipped with two small finger pads, that comes shipped with the robot arm.
The robot comes with a controller that takes in actions. 
The expected action space of the OSC_POSE controller (without a gripper) is (dx, dy, dz, droll, dpitch, dyaw). 
The manual reads like the following: 
( dx,  0,  0,  0,  0,  0, grip)     <-- Translation in x-direction (forward/backward)         
(  0, dy,  0,  0,  0,  0, grip)     <-- Translation in y-direction (left/right) 
(  0,  0, dz,  0,  0,  0, grip)     <-- Translation in z-direction (up/down)     
(  0,  0,  0, droll,  0,  0, grip)     <-- Rotation in roll axis       
(  0,  0,  0,  0, dpitch,  0, grip)     <-- Rotation in pitch axis  
(  0,  0,  0,  0,  0, dyaw, grip)     <-- Rotation in yaw axis 
If the grip = 100, the robot is having gripper closed. if the grip = -100, the robot is having gripper open.
"""

prompt_task_square = """
In this task, the robot must pick a square nut and place it on a rod. The nut has a handle to be grasped.

The task has the following stages:

1. Grasping the Handle: Approach the square nut's handle. The robot will move closer to the square nut handle and the distance between robot position
and handle position will be closer. The robot will grasp the nut by its handle, according to the angles of the handle (roll, pitch, yaw). The robot will need to move to the correct angles (roll, pitch, yaw) and perform the grasp action.

2. Peg Insertion: Lift the nut and get closer to the peg and aligning with its angles (roll, pitch, yaw) at the same time. The distance between robot position will be closer. It then inserts the nut in the peg by moving the nut down the peg.

Here are some example input, and the stage they correspond to:

    Example 1:
    
        Input:

        Information relevant to grasping the handle:
        Robot Position: [-3 16 91]
        Robot Angles: [ 3 -3 44]
        Handle Position: [-8 17 83]
        Handle Angles: [ 0  0 54]
        Gripper State: [-100]

        Information relevant to peg insertion:
        Nut Position: [-11  13  83]
        Nut Angles: [ 0  0 54]
        Peg Position: [23 10 85]
        Peg Angles: [0 0 0]
        Gripper State: [-100]

        Stage: Grasping the Handle
    
    Example 2:
    
        Input:

        Information relevant to grasping the handle:
        Robot Position: [24  2 97]
        Robot Angles: [  4   0 -89]
        Handle Position: [24  4 97]
        Handle Angles: [ -5  -5 -90]
        Gripper State: [100]

        Information relevant to peg insertion:
        Nut Position: [24  9 96]
        Nut Angles: [17 16 12]
        Peg Position: [23 10 85]
        Peg Angles: [0 0 0]
        Gripper State: [100]

        Stage: Peg Insertion

You are given the state information, which include:
1. robot end effector position
2. robot end effector angle in roll, pitch, yaw axis 
3. handle position 
4. handle angle in roll, pitch, yaw axis
5. nut position 
6. nut angle in roll, pitch, yaw axis 
7. peg position 
8. peg angle in roll, pitch, yaw axis 
9. gripper status (100 for closed, -100 for open)

"""


prompt_task_can = """

In this task, the robot must pick up the can and put it in the correct position in the box

The task has the following stages:

1. Grasping the can: Approach the can. The robot will move closer to the can object and the distance between robot position and can position will be closer. The robot will then perform the grasp action.

2. Placing the can in the box: The robot will move the can closer to the box, and then release the gripper to place the can in the box.

You are given the state information, which include:
1. robot end effector position
2. robot end effector angle in roll, pitch, yaw axis
3. gripper status (100 for closed, -100 for open)
4. can position
5. box position

"""

prompt_task_coffee = """
In this task, the robot must pick the coffee pod, insert it in the coffee pod holder and close the coffee lid.

The task has the following stages:

1. Grasping the Coffee pod: Approach the coffee pod. The robot will move closer to the coffee pod and the distance between robot position and coffee pod position will be closer. The robot will then perform the grasp action.

2. Inserting the Coffee Pod in the Coffee Pod Holder: Lift the coffee pod and get closer to the coffee pod holder. The distance between the coffee pod and coffee pod holder will be closer. It then inserts the coffee pod by moving it down; and releases the gripper to place the coffee pod into the coffee pod holder.

3. Closing the Coffee Lid: The robot should position its grippers to the location of the coffee lid. The robot will then press down on the lid until the lid is closed. 

You are given the state information, which include:

1. robot end effector position
2. robot end effector angle in roll, pitch, yaw axis
3. gripper status (100 for closed, -100 for open)
4. coffee pod position
5. coffee pod holder position
6. coffee machine lid position
7. coffee machine lid angle in roll, pitch, yaw axis
"""

prompt_task_threading = """
In this task, the robot must pick the needle and insert it in the thread hole. The needle has a handle to be grasped.

The task has the following stages:
1. Grasping the Handle: Approach the needle's handle. The robot will move closer to the needle handle and the distance between robot position and handle position will be closer. The robot will grasp the needle by its handle, according to the angles of the handle (roll, pitch, yaw). The robot will need to move to the correct angles (roll, pitch, yaw) and perform the grasp action.
2. Needle Insertion: Position the needle tip in alignment with the thread hole. The robot needs to adjust the needle tip's angles (roll, pitch, yaw) with angles (roll, pitch, yaw) of the thread hole to ensure that the thread can be inserted. Once aligned, the robot will insert the needle tip into the thread hole so that the thread passes through the thread hole smoothly. 

You are given the state information, which include:
1. robot end effector position
2. robot end effector angle in roll, pitch, yaw axis
3. gripper status (100 for closed, -100 for open)
4. needle handle position
5. needle handle angle in roll, pitch, yaw axis
6. needle tip position
7. needle tip angle in roll, pitch, yaw axis
8. thread hole position     
9. thread hole angle in roll, pitch, yaw axis
"""

prompt_task_toolhang = """
In this task, the robot must pick the frame hook piece and insert it into the base hole, and then pick the tool piece and hang on the hook piece.

The task has the following stages:
1. Grasping the Hook: Approach the frame hook's handle. The robot will move closer to the frame hook's handle and the distance between robot position and frame hook hook handle position will be closer. The robot will grasp the nut by its handle, according to the angles of the handle (roll, pitch, yaw). The robot will need to move to the correct angles (roll, pitch, yaw) and perform the grasp action.
2. Inserting the Frame Hook piece: Lift the frame hook and get closer to the base and align with its angles (roll, pitch, yaw) at the same time. The distance between frame hook and base positions will be closer. It then inserts the frame hook in the base hole by moving the frame hook down the base hole.
3. Grasping the Tool: Approach the tool's handle. The robot will move closer to the tool's handle and the distance between robot position and tool handle position will be closer. The robot will grasp the tool by its handle, according to the angles of the handle (roll, pitch, yaw). The robot will need to move to the correct angles (roll, pitch, yaw) and perform the grasp action.
4. Hanging the Tool: Lift the tool piece and get closer to the frame hook's hook position and align with its angles (roll, pitch, yaw) at the same time. The distance between tool hole position and frame hook's hook position will be closer. It then hooks the tool hole in the frame hook's hook position by moving the tool piece down. Finally, it will release the gripper. 

You are given the state information, which include:
1. robot end effector position
2. robot end effector angle in roll, pitch, yaw axis
3. gripper status (100 for closed, -100 for open)
4. Base Hole Position
5. Base Hole Orientation
6. Frame Hook Handle Position
7. Frame Hook Handle Orientation
8. Frame Hook Needle Position
9. Frame Hook Needle Orientation
10. Frame Hooks Hook Position
11. Frame Hook's Hook Orientation
12. Tool Handle Position
13. Tool Handle Orientation
14. Tool Hole Position
15. Tool Hole Orientation 
"""

prompt_task = {
    "square": prompt_task_square,
    "can": prompt_task_can,
    "coffee": prompt_task_coffee,
    "threading": prompt_task_threading,
    "toolhang": prompt_task_toolhang
}

prompt_instruction = """
Your task is that, given a few choices of actions to perform at the current state, you will choose the correct action for the robot to perform.

Note on the position and angle:
You should consider the position and angle of the robot end effector and object, and how they are related to each other.
For example, if the robot end effector is on the left of the object, you should consider moving the robot end effector to the right.
If the robot end effector is not aligned with the object in rotation, you should consider rotating the robot end effector to align with the object.

Note on the gripper:
The robot's gripper should be closed if it is beginning to grasp the object, or when it is holding the object. 
When it is approaching the object, the gripper is open.
If the robot gripper needs to be closed, you should continue to close the gripper, even if it is closed.
Similarly, if the robot gripper needs to be open, you should continue to open the gripper, even if it is already open.
"""

prompt_instruction_cot = """

Given the robot and object position, first explain what stage is the task currently in, and what is the relationship between the robot and object. Explain what a good action is supposed to do.
Then based on your result, look at the given actions, and return which of the following actions is the correct action to take.

Let's think step by step.
Explaining your reasoning before arriving at the solution. 

You always produce a single Action value in the end, which is a single number. You must follow this format!
If there are multiple actions, you must only return one of them.
"""

prompt_instruction_cot_return_action = """
Given the robot and object position, first explain what stage is the task currently in, and what is the relationship between the robot and object. Explain what a good action is supposed to do.
Then based on your result, return a correct action to take on the current state in the format of [dx, dy, dz, droll, dpitch, dyaw, grip] as mentioned above. The action value should be in the appropriate action scale (between -100 to 100).

Let's think step by step.
Explaining your reasoning before arriving at the solution. 

You always produce an action being in a list of length 7. You must follow this format! You must follow this format!

"""

prompt_instruction_cot_edit_action = """
Given the robot and object position, first explain what stage is the task currently in, and what is the relationship between the robot and object. 

Explain what a good action is supposed to do.

Based on your result, identify the action dimension indices that requires modification. 

Then modify the original action in these action dimension indices in the appropriate action scale (between -100 to 100).

Finally, return a correct action to take on the current state in the format of [dx, dy, dz, droll, dpitch, dyaw, grip] as mentioned above.

Let's think step by step.
Explaining your reasoning before arriving at the solution. 

You always produce an action being in a list of length 7. You must follow this format! You must follow this format!

"""

prompt_instruction_cot_combine_onedim = """

Given the robot and object position, first explain what stage is the task currently in, and what is the relationship between the robot and object. 
Explain what a good action is supposed to do. 
You are also given 8 actions, that can move on different axis. 
You can combine the 8 actions together to generate a new action. 
You will output the final action to take given these actions.

Let's think step by step.
Explaining your reasoning before arriving at the solution. 
"""

prompt_instruction_cot_backup = """

Follow the instructions below to complete the task:

# 1. Given the robot and object position, first identify which stage of the task the robot is in, based on the information above.

# 2. Then explain what is the relationship between the robot and object. Explain what a good action is supposed to do here.

# 3. Then based your result, look at the given actions, and return which of the following two actions is the correct action to take.

Then based your result, look at the given actions, and return which of the following two actions is the correct action to take.

"""

prompt_language_correction = """
You also receive the following human language correction at the current state. Pay close attention to the human language correction,
 interpret the human intention, and use it to arrive at the solution.

Some pointers for human language correction interpretation:

Move backward: decrease the x position
Move forward: increase the x position
Move left: decrease the y position
Move right: increase the y position
Move up: increase the z position
Move down: decrease the z position
Rotate: changing the yaw angle

Human language correction:

"""

template_obs_square = """
    Input: 
    
    Information relevant to grasping the handle:
    Robot Position: {}
    Robot Angles: {}
    Handle Position: {}
    Handle Angles: {}
    Gripper State: {}
    
    Information relevant to peg insertion:
    Nut Position: {}
    Nut Angles: {}
    Peg Position: {}
    Peg Angles: {}
    Gripper State: {}
    """

template_obs_can = """
    Input: 
    
    Information relevant to grasping the can:
    Robot Position: {}
    Robot Angles: {}
    Can Position: {}
    Gripper State: {}
    
    Information relevant to placing the can:
    Can Position: {}
    Box Position: {}
    Gripper State: {}
"""

template_obs_coffee = """
    Input: 
    
    Information relevant to grasping the coffee pod:
    Robot Position: {}
    Robot Angles: {}
    Coffee Pod Position: {}
    Gripper State: {}
    
    Information relevant to coffee pod insertion:
    Coffee Pod Position: {}
    Coffee Pod Holder Position: {}
    Gripper State: {}

    Information relevant to closing the coffee lid:
    Robot Position: {}
    Robot Angles: {}
    Coffee Lid Position: {}
    Coffee Lid Angles: {}
    Gripper State: {}
"""

template_obs_threading = """
    Input: 
    
    Information relevant to grasping the needle handle:
    Robot Position: {}
    Robot Angles: {}
    Needle Handle Position: {}
    Needle Handle Angles: {}
    Gripper State: {}
    
    Information relevant to needle insertion:
    Needle Position: {}
    Needle Angles: {}
    Thread Hole Position: {}
    Thread Hole Angles: {}
    Gripper State: {}
"""

template_obs_toolhang = """
    Input: 
    
    Information relevant to grasping the frame hook:
    Robot Position: {}
    Robot Angles: {}
    Frame Hook Position: {}
    Frame Hook Angles: {}
    Gripper State: {}
    
    Information relevant to frame hook insertion:
    Frame Hook Needle Position: {}
    Frame Hook Needle Angles: {}
    Base Hole Position: {}
    Base Hole Angles: {}
    Gripper State: {}

    Information relevant to grasping the tool:
    Robot Position: {}
    Robot Angles: {}
    Tool Handle Position: {}
    Tool Handle Angles: {}
    Gripper State: {}

    Information relevant to hanging the tool:
    Frame Hook's Hook Position: {}
    Frame Hook's Hook Angles: {}
    Tool Hole Position: {}
    Tool Hole Angles: {}
    Gripper State: {}
"""

template_obs = {
    "square": template_obs_square,
    "can": template_obs_can,
    "coffee": template_obs_coffee,
    "threading": template_obs_threading,
    "toolhang": template_obs_toolhang
}
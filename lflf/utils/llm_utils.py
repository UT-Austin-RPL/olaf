import numpy as np

def format_value(arr, angle=False, convert_int=True):            
    if angle:
        #arr = arr[-1]
        arr = np.where(np.sign(arr) == 0, 0.0, arr)
        arr = np.int8(arr)
        return str(arr)
        
    arr = arr.round(2)
    arr = np.where(np.sign(arr) == 0, 0.0, arr)
    if convert_int:
        arr = np.int8(arr * 100)
    return str(arr)

def format_obs_square(one_step, template_obs):
    robot_pos = one_step['robot_pos']
    robot_angle = one_step['robot_angle']
    
    handle_pos = one_step['handle_pos']
    handle_angle = one_step['handle_angle']
    
    nut_pos = one_step['nut_pos']
    nut_angle = one_step['nut_angle']
    
    peg_pos = one_step['peg_pos']
    peg_angle = one_step['peg_angle']
    
    gripper_state = one_step['gripper_state']
    
    
    template = template_obs.format(
        format_value(robot_pos),
        format_value(robot_angle, angle=True),
        
        format_value(handle_pos),
        format_value(handle_angle, angle=True),        

        format_value(gripper_state),
        
        
        format_value(nut_pos),
        format_value(nut_angle, angle=True),
        
        format_value(peg_pos),
        format_value(peg_angle, angle=True),
        
        format_value(gripper_state),
    )

    return template


def format_obs_can(one_step, template_obs):
    robot_pos = one_step['robot_pos']
    robot_angle = one_step['robot_angle']
    
    can_pos = one_step['can_pos']
    can_angle = one_step['can_angle']
    
    bin_pos = one_step['bin_pos']
    bin_angle = one_step['bin_angle']
    
    gripper_state = one_step['gripper_state']
    
    template = template_obs.format(
        format_value(robot_pos),
        format_value(robot_angle, angle=True),
        format_value(can_pos), 

        format_value(gripper_state),

        format_value(can_pos),
        format_value(bin_pos),
        
        format_value(gripper_state),
    )

    return template


def format_obs_threading(one_step, template_obs):
    robot_pos = one_step['robot_pos']
    robot_angle = one_step['robot_angle']
    
    needle_needle_pos = one_step['needle_needle_pos']
    needle_needle_angle = one_step['needle_needle_angle']
    
    needle_handle_pos = one_step['needle_handle_pos']
    needle_handle_angle = one_step['needle_handle_angle']
    
    ring_pos = one_step['ring_pos']
    ring_angle = one_step['ring_angle']

    gripper_state = one_step['gripper_state']
    
    template = template_obs.format(
        format_value(robot_pos),
        format_value(robot_angle, angle=True),
        format_value(needle_handle_pos), 
        format_value(needle_handle_angle, angle=True),
        format_value(gripper_state),

        format_value(needle_needle_pos),
        format_value(needle_needle_angle, angle=True),
        format_value(ring_pos),
        format_value(ring_angle, angle=True),
        format_value(gripper_state),
    )

    return template


def format_obs_toolhang(one_step, template_obs):
    robot_pos = one_step['robot_pos']
    robot_angle = one_step['robot_angle']
    
    # base 
    base_pos = one_step['base_pos']
    base_angle = one_step['base_angle']

    # hook handle, bottom (tip), hang
    hook_handle_pos = one_step['hook_handle_pos']
    hook_handle_angle = one_step['hook_handle_angle']

    hook_bottom_pos = one_step['hook_bottom_pos']
    hook_bottom_angle = one_step['hook_bottom_angle']

    hook_hang_pos = one_step['hook_hang_pos']
    hook_hang_angle = one_step['hook_hang_angle']

    # tool handle, hole
    tool_handle_pos = one_step['tool_handle_pos']
    tool_handle_angle = one_step['tool_handle_angle']

    tool_hole_pos = one_step['tool_hole_pos']
    tool_hole_angle = one_step['tool_hole_angle']

    gripper_state = one_step['gripper_state']

    template = template_obs.format(
        format_value(robot_pos),
        format_value(robot_angle, angle=True),
        format_value(hook_handle_pos), 
        format_value(hook_handle_angle, angle=True),
        format_value(gripper_state),

        format_value(hook_bottom_pos),
        format_value(hook_bottom_angle, angle=True),
        format_value(base_pos),
        format_value(base_angle, angle=True),
        format_value(gripper_state),

        format_value(robot_pos),
        format_value(robot_angle, angle=True),
        format_value(tool_handle_pos), 
        format_value(tool_handle_angle, angle=True),
        format_value(gripper_state),

        format_value(hook_hang_pos),
        format_value(hook_hang_angle, angle=True),
        format_value(tool_hole_pos),
        format_value(tool_hole_angle, angle=True),
        format_value(gripper_state),
    )
    return template

def format_obs_coffee(one_step, template_obs):
    robot_pos = one_step['robot_pos']
    robot_angle = one_step['robot_angle']
    
    pod_pos = one_step['pod_pos']
    pod_holder_pos = one_step['pod_holder_pos']
    lid_pos = one_step['lid_pos']
    lid_angle = one_step['lid_angle']
    gripper_state = one_step['gripper_state']
    
    template = template_obs.format(
        format_value(robot_pos),
        format_value(robot_angle, angle=True),
        format_value(pod_pos), 
        format_value(gripper_state),

        format_value(pod_pos), 
        format_value(pod_holder_pos),
        format_value(gripper_state),

        format_value(robot_pos),
        format_value(robot_angle, angle=True),
        format_value(lid_pos),
        format_value(lid_angle, angle=True),

        format_value(gripper_state),
    )

    return template


def format_obs(one_step, template_obs, task):
    if task == "square":
        return format_obs_square(one_step, template_obs)
    if task == "can":
        return format_obs_can(one_step, template_obs)
    if task == "threading":
        return format_obs_threading(one_step, template_obs)
    if task == "toolhang":
        return format_obs_toolhang(one_step, template_obs)
    if task == "coffee":
        return format_obs_coffee(one_step, template_obs)


def format_action(action_candidates):
    template_action = """
        Action Choices:         
        """
    num_actions = len(action_candidates)
    for i in range(num_actions):
        a = """
            Action {}: {}
            """.format(
            i,
            format_value(action_candidates[i])
        )
        template_action += a

    return template_action

def format_action_single(action):
    a = """
        Action: {}
        """.format(
        format_value(action)
    )

    return a

onedim_actions = [
    [0.2,0,  0,  0,0,0,  ],
    [0,  0.2,0,  0,0,0,  ],
    [0,  0,  0.2,0,0,0,  ],
    [0,  0,  0,  0,0,0.2,],
    
    [-0.2,0,  0,  0,0,0, ],
    [0,  -0.2,0,  0,0,0, ],
    [0,  0,  -0.2,0,0,0, ],
    [0,  0,  0,  0,0,-0.2],
]
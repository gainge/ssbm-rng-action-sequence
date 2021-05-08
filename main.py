import sys

# Define the actions + their rolls to serve as the "coins"
class Action:

    def __init__(self, label, rolls, frames = 100, is_css = False):
        self.label = label
        self.rolls = rolls
        self.frames = frames
        self.is_css = is_css

    def getValue(self):
        # return int((self.rolls / self.frames) * 1000)
        return int((self.frames / self.rolls) * 1000)

    def __str__(self):
        return f'Action: \'{self.label}\', Rolls: {self.rolls}'


# Define RNG-calling actions in the form (label, rolls, frames, is css action)
# Frame measurements are approximate
# TODO: Adjust roll/frame ratios based on how things feel :P
items = [
    Action('Idle Animation', 1, 360, False),
    Action('Random Tag', 1, 20, True),
    Action('Random Character', 2, 20, True),
    Action('Shield', 9, 40, False),
    Action('Stage Load', 12, 60, True),         # Early pause code, also hardware dependent lol
    Action('Standing Grab', 15, 35, False),
    Action('Up Tilt', 27, 39, False),
    Action('Upsmash', 40, 45, False),
    Action('Jump Airdodge', 62, 96, False),
    Action('Jump Land', 63, 86, False),         # fairly rough
    Action('Downsmash', 70, 55, False),         # SUUPER ROUGH ESTIMATE
    Action('Jump Double Jump Airdodge', 72, 165, False),
    Action('Jump Double Jump Land', 73, 150, False),
    Action('Jump Fair Land', 88, 96, False),
    Action('Jump Double Jump Fair Land', 98, 144, False),
]

MAX = 10000000000
STAGE_LOAD_ROLLS = 12
IN_GAME_THRESHOLD = 60 # approx no. rolls where in-game actions become faster than css manip
idle_animation_action = items[0]
stage_load_action = items[4]


def find_action_sequence(total, actions):
    # Initialize dp array
    dp = [MAX] * (total + 1)
    dp[0] = 0

    for i in range(1, total + 1):
        for action in actions:
            if action.rolls <= i:
                # Does this action offer a more efficient way to achieve the current rolls?
                dp[i] = min(dp[i - action.rolls] + action.getValue(), dp[i])
    
    # Now can we just backtrack like regular
    action_sequence = {}
    remainingValue = dp[total]
    remainingRolls = total

    while remainingRolls > 0:
        for action in reversed(actions):
            if (action.rolls <= remainingRolls and
                dp[remainingRolls - action.rolls] == (remainingValue - action.getValue())
                ):
                # Add to action sequence and decrement remaining rolls
                action_sequence[action] = action_sequence.get(action, 0) + 1
                remainingRolls = remainingRolls - action.rolls
                remainingValue = remainingValue - action.getValue()
                break
    
    return action_sequence



def print_action(action, count):
    print(f'{count} - {action.label} ({action.rolls})')

def display_results(action_sequence, target_rolls):
    num_actions = sum(action_sequence.values())

    print()
    print('----------------------------------')
    print(f'Achievable in {num_actions} action{"s" if num_actions > 1 else ""}!')
    print('----------------------------------')
    print(f'Target: {target_rolls} rolls')

    # Always attempt to print the stage loads first
    if action_sequence.get(stage_load_action):
        print()
        print_action(stage_load_action, action_sequence.get(stage_load_action))
    else:
        # Give warning for low roll count
        print('!!! --- Assumed CSS Manip due to low roll count')
        print()

    # Now iterate normally, skipping stage load
    for action, count in action_sequence.items():
        if action == stage_load_action:
            continue
        else:
            print_action(action, count)
    print()




def is_quit(val):
    return val == 'x' or val == 'X'

def get_user_input():
    while True:
        user_input = input('Please enter roll target (x to quit): ')

        if is_quit(user_input):
            return user_input

        try:
            rolls = int(user_input)
            return rolls
        except ValueError:
            print('!! -- Please input a number!')
            print()




# Start execution, look for CSS flag
CSS_MANIP_FLAG = 'n';
IS_CSS_MANIP = False;

if len(sys.argv) > 1:
    IS_CSS_MANIP = sys.argv[1] == CSS_MANIP_FLAG


# Main loop I guess lol
print('-------------------------------')
print('In-Game RNG Manipulation Helper')
print('-------------------------------')
print()
while True:
    rolls = get_user_input()

    if is_quit(rolls):
        print('Goodbye!')
        break

    
    adjusted_rolls = rolls
    available_actions = items

    # Adjust data for css manip if applicable
    if IS_CSS_MANIP and rolls > IN_GAME_THRESHOLD:
        adjusted_rolls -= 12
    else:
        # don't use CSS manip items
        available_actions = list(filter(lambda x: not x.is_css, items))

    # Determine the action sequence
    action_sequence = find_action_sequence(adjusted_rolls, available_actions)

    # Add in the extra stage load if in-game actions are used
    if IS_CSS_MANIP and rolls > IN_GAME_THRESHOLD:
        action_sequence[stage_load_action] = action_sequence.get(stage_load_action, 0) + 1

    # Show the world what we cooked up!
    display_results(action_sequence, rolls)
    



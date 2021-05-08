import sys

# Define the actions + their rolls to serve as the "coins"
class Action:

    def __init__(self, label, rolls, frames = 100, is_css = False):
        self.label = label
        self.rolls = rolls
        self.frames = frames
        self.is_css = is_css

    def getRollsPerFrame(self):
        return self.rolls / self.frames

    def __str__(self):
        return f'Action: \'{self.label}\', Rolls: {self.rolls}'


MAX = 100000000
STAGE_LOAD_ROLLS = 12
IN_GAME_THRESHOLD = 60 # approx no. rolls where in-game actions become faster than css manip
idle_animation_action = Action('Idle Animation', 1)

# Define RNG-calling actions in the form (label, rolls, frames, is css action)
# Frame measurements are approximate :P
items = [
    Action('Random Tag', 1, 10, True),
    Action('Random Character', 2, 10, True),
    Action('Shield', 9, 40, False),
    Action('Stage Load', 12, 60, True),         # Early pause code, also hardware dependent lol
    Action('Standing Grab', 15, 29, False),
    Action('Up Tilt', 27, 39, False),
    Action('Upsmash', 40, 44, False),
    Action('Jump Airdodge', 62, 96, False),
    Action('Jump Land', 63, 86, False),         # fairly rough
    Action('Downsmash', 70, 55, False),         # SUUPER ROUGH ESTIMATE
    Action('Jump Double Jump Airdodge', 72, 165, False),
    Action('Jump Double Jump Land', 73, 150, False),
    Action('Jump Fair Land', 88, 96, False),
    Action('Jump Double Jump Fair Land', 98, 144, False),
]



def build_sequence(total, dp, actions):
    sequence = []
    sequence_dict = {}

    # Actually I think we can just loop based off the final entry
    min_actions = dp[total]
    count = total

    for i in reversed(range(min_actions)):
        # Find which action gets us to the next step in the line
        for action in reversed(actions): # reversed to start with the most rolls
            if action.rolls <= count and dp[count - action.rolls] == i:
                sequence_dict[action] = sequence_dict.get(action, 0) + 1
                sequence.append(action.label)
                count = count - action.rolls
                break # continue to the next step in our DP array
    
    return sequence, sequence_dict
    


def find_action_sequence(total, actions):
    dp = [MAX] * (total + 1)
    dp[0] = 0 # initialize first sequence as zero to facilitate algorithm


    for action in actions:
        for i in range(1, total + 1):
            if action.rolls <= i:
                dp[i] = min(dp[i - action.rolls] + 1, dp[i])
    

    # Check for lingering rolls needed
    if dp[total] == MAX:
        print('Solution not found, will append Idle Animations')

    # Compute # of idle animation rolls needed to complete the sequence
    idle_count = 0

    while dp[total - idle_count] == MAX:
        idle_count += 1

    # Trim dp array in preparation for backtracking
    if idle_count > 0:
        dp = dp[:-idle_count]


    num_actions = dp[-1] + idle_count

    # Build action sequence using backtracking on dp array
    sequence, sequence_dict = build_sequence(total - idle_count, dp, actions)

    # Append idle animations to sequence, if appropriate
    if idle_count > 0:
        sequence_dict[idle_animation_action] = idle_count

    return sequence_dict



def display_results(action_sequence, target_rolls):
    num_actions = len(action_sequence)

    print()
    print('----------------------------------')
    print(f'Achievable in {num_actions} action{"s" if num_actions > 1 else ""}!')
    print('----------------------------------')
    print(f'Target: {target_rolls} rolls')

    print()
    for action, count in action_sequence.items():
        print(f'{count} - {action.label} ({action.rolls})')
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


CSS_MANIP_FLAG = 'n';
IS_CSS_MANIP = False;

if len(sys.argv) > 1:
    IS_CSS_MANIP = sys.argv[1] == CSS_MANIP_FLAG

# Modify action set based on in-game vs standard manip flag


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

    # Adjust data for css manip if applicable
    if IS_CSS_MANIP:
        adjusted_rolls -= 12
    else:
        # don't use CSS manip items


    adjusted_rolls = rolls - (12 if IS_CSS_MANIP else 0)

    action_sequence = find_action_sequence(adjusted_rolls, items)


    display_results(action_sequence, rolls)
    



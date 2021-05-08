import sys

# Define the actions + their rolls to serve as the "coins"
class Action:

    def __init__(self, label, rolls):
        self.label = label
        self.rolls = rolls

    def __str__(self):
        return f'Action: \'{self.label}\', Rolls: {self.rolls}'


MAX = 100000000
STAGE_LOAD_ROLLS = 12
IN_GAME_THRESHOLD = 60 # approx no. rolls where in-game actions become faster than css manip
idle_animation_action = Action('Idle Animation', 1)

items = [
    # Action('Random Tag', 1),
    # Action('Random Character', 2),
    Action('Shield', 9),
    Action('Standing Grab', 15),
    Action('Up Tilt', 27),
    Action('Upsmash', 40),
    Action('Jump Airdodge', 62),
    Action('Jump Land', 63),
    Action('Downsmash', 70),
    Action('Jump Double Jump Airdodge', 72),
    Action('Jump Double Jump Land', 73),
    Action('Jump Fair Land', 88),
    Action('Jump Double Jump Fair Land', 98),
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


STANDARD_MANIP_FLAG = 'n';
STANDARD_MANIP = False;

if len(sys.argv) > 1:
    STANDARD_MANIP = sys.argv[1] == STANDARD_MANIP_FLAG

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

    # Adjust rolls for standard manip

    action_sequence = find_action_sequence(rolls, items)

    display_results(action_sequence, rolls)
    



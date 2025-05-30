import argparse
import sys
import time
from airis_aux import AIRIS

import gym
from gym import wrappers, logger


class AIAgent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.vis_env = [[0]]
        self.aux_env = [0, 0, 0, 0]
        self.action_space = [0, 1]
        self.action = 0
        self.action_output_list = [
            [1, 2, 1],
            [1, 2, 1]
        ]
        self.airis = AIRIS(self.vis_env, self.aux_env, self.action_space, self.action_output_list)
        self.airis.goal_type = 'Fixed'
        self.airis.goal_type_default = 'Fixed'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('env_id', nargs='?', default='CartPole-v0', help='Select the environment to run')
    args = parser.parse_args()

    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)

    env = gym.make(args.env_id)

    # You provide the directory to write to (can be an existing
    # directory, including one with existing data -- all monitor files
    # will be namespaced). You can also dump to a tempdir if you'd
    # like: tempfile.mkdtemp().
    # outdir = '/tmp/random-agent-results'
    # env = wrappers.Monitor(env, directory=outdir, force=True)
    env.seed(0)
    agent = AIAgent(env.action_space)

    #for n in range(1000):
    start_time = time.time()
    episode_count = 100
    episode_score = 0
    reward = 0
    done = False
    run_total = 0
    round_to = 2
    dupes = 0

    for i in range(episode_count):
        ob = env.reset()
        run_total += episode_score
        episode_score = 0
        while True:
            action, _, _ = agent.airis.capture_input([[0]], [round(ob[2], round_to), round(ob[1], round_to), round(ob[0], round_to), round(ob[3], round_to)], 0, prior=True)
            if action is None:
                action = env.action_space.sample()
                print ('AI took no action')
            print(action, [round(ob[2], round_to), round(ob[1], round_to), round(ob[0], round_to), round(ob[3], round_to)])
            ob, reward, done, _ = env.step(action)
            episode_score += reward
            if action is not None:
                if not done or episode_score >= 199:
                    agent.airis.capture_input([[0]], [round(ob[2], round_to), round(ob[1], round_to), round(ob[0], round_to), round(ob[3], round_to)], action, prior=False)
                else:
                    agent.airis.capture_input([[0]], [1, round(ob[1], round_to), round(ob[0], round_to), round(ob[3], round_to)], action, prior=False)

            if i > 0:
                print(action, [round(ob[2], round_to), round(ob[1], round_to), round(ob[0], round_to), round(ob[3], round_to)], reward, done, i, run_total / i, 'duration: ', str(time.time() - start_time), agent.airis.knowledge['last condition id'])
            if done:
                print('episode score: ', episode_score)
                break

            # Note there's no env.render() here. But the environment still can open window and
            # render if asked by env.monitor: it calls env.render('rgb_array') to record video.
            # Video is not recorded every episode, see capped_cubic_video_schedule for details.

    run_total += episode_score
    # Close the env and write monitor result info to disk
    print('average score: ', run_total, run_total / 100)
    with open('cartpole_2Rounded_200Depth_FixedNoDupe_FixedGoal_2Assume_moe_PrevCheck_Optimized_relative_NoInterrupt.txt', 'a') as file:
        file.write(str(run_total / 100)+' | '+str(time.time() - start_time)+' | '+str(agent.airis.knowledge['last condition id'])+'\n')
    agent.airis.save_knowledge()

    env.close()

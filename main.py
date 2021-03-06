#!/usr/bin/env python3

from game import Game, IllegalActionException
from ai import AI


def human_move(game):
    while True:
        my_move = Game.coord_to_action(input("Enter your move: "))
        if my_move is None:
            print("Unknown move... Try like A3.")
            continue
        try:
            print(game.apply(my_move))
            break
        except IllegalActionException:
            print("Illegal move... Try again.")


def main(args):

    ai = AI(load=args.input, filepath=args.output,
            num_episodes=args.num_episodes,
            update_freq=args.update_freq,
            eval_episodes=args.eval_episodes,
            mcts_iters=args.mcts_iterations,
            tau_cutoff=args.tau_cutoff)

    if not args.skip_training:
        print('=' * 80)
        print("Training...")
        print('=' * 80)
        ai.train()
        print("AI is ready!")

    while True:
        print("Starting new game...")
        game = Game(ai)
        print(game)

        first = input("Do you wish to play first? ")
        if first and first[0].lower() == 'y':
            human_move(game)

        while not game.over:
            ai_move = game.best_action
            print("AI plays:", Game.action_to_coord(ai_move))
            print(game.apply(ai_move))
            if game.over:
                break
            human_move(game)

        print(f"Game over: {game.winner} wins!")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="UltimateTicTacToe AI")
    parser.add_argument('-n', '--num-episodes', default=400, type=int,
                        help="Number of self-play simulations to run.")
    parser.add_argument('-f', '--update-freq', default=80, metavar="IVAL",
                        type=int,
                        help="Train a new model every IVAL simulations.")
    parser.add_argument('-e', '--eval-episodes', default=20, type=int,
                        metavar="EVALS",
                        help="How many duels used to evaluate new models.")
    parser.add_argument('-o', '--output', default='best_estimator.h5',
                        help="File path to store the best model.")
    parser.add_argument('-s', '--skip-training', action='store_true',
                        help="Skip training (requires pre-trained model).")
    parser.add_argument('-c', '--tau-cutoff', default=20, type=int,
                        help="Reduce exploration after this many moves.")
    parser.add_argument('-m', '--mcts-iterations', default=100, type=int,
                        help="Number of iterations for "
                             "Monte Carlo Tree Search.")
    parser.add_argument('input', nargs='?',
                        help="Load model from this file.")
    main(parser.parse_args())

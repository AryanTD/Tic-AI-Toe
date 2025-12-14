from board import TicTacToe
from agents.qlearning_agent import QLearningAgent
from agents.random_agent import RandomAgent
import matplotlib.pyplot as plt

def train_qlearning(num_episodes=50000, save_filename="q_table.pkl"):
    """
    Train Q-Learning agent by playing against Random opponent.
    """
    print("=" * 50)
    print("TRAINING Q-LEARNING AGENT VS RANDOM")
    print("=" * 50)
    
    # Create learning agent
    agent = QLearningAgent(
        player=1,  # Always play as X for now
        learning_rate=0.1,
        discount_factor=0.9,
        epsilon=0.3
    )
    
    # Epsilon decay
    epsilon_start = 0.3
    epsilon_end = 0.05
    epsilon_decay = (epsilon_start - epsilon_end) / num_episodes
    
    # Track progress
    wins = 0
    losses = 0
    draws = 0
    
    # For plotting
    window_size = 1000
    win_rates = []
    
    print(f"\nTraining for {num_episodes:,} episodes...")
    print("Agent plays as X, Random plays as O\n")
    
    for episode in range(num_episodes):
        game = TicTacToe()
        agent.reset_history()
        random_opponent = RandomAgent(player=-1)
        
        while not game.is_game_over():
            if game.current_player == 1:
                # Agent's turn
                move = agent.get_move(game, training=True)
            else:
                # Random opponent's turn
                move = random_opponent.get_move(game)
            
            game.make_move(move)
        
        # Determine outcome and learn
        winner = game.check_winner()
        
        if winner == 1:
            wins += 1
            agent.learn(reward=1)  # Win!
        elif winner == -1:
            losses += 1
            agent.learn(reward=-1)  # Loss
        else:
            draws += 1
            agent.learn(reward=0)  # Draw
        
        # Decay epsilon
        agent.epsilon = max(epsilon_end, agent.epsilon - epsilon_decay)
        
        # Track progress
        if (episode + 1) % window_size == 0:
            win_rate = wins / window_size * 100
            loss_rate = losses / window_size * 100
            draw_rate = draws / window_size * 100
            win_rates.append(win_rate)
            
            print(f"Episode {episode + 1:6,} | "
                  f"W: {win_rate:5.1f}% | L: {loss_rate:5.1f}% | D: {draw_rate:5.1f}% | "
                  f"ε: {agent.epsilon:.3f} | States: {len(agent.q_table):,}")
            
            wins = 0
            losses = 0
            draws = 0
    
    print("\n" + "=" * 50)
    print("Now training as O (playing second)...")
    print("=" * 50)
    
    # Train as O too
    agent.player = -1
    wins = 0
    losses = 0
    draws = 0
    
    for episode in range(num_episodes // 2):  # Half as many episodes as O
        game = TicTacToe()
        agent.reset_history()
        random_opponent = RandomAgent(player=1)
        
        while not game.is_game_over():
            if game.current_player == 1:
                # Random goes first
                move = random_opponent.get_move(game)
            else:
                # Agent plays as O
                move = agent.get_move(game, training=True)
            
            game.make_move(move)
        
        winner = game.check_winner()
        
        if winner == -1:
            wins += 1
            agent.learn(reward=1)
        elif winner == 1:
            losses += 1
            agent.learn(reward=-1)
        else:
            draws += 1
            agent.learn(reward=0)
        
        if (episode + 1) % window_size == 0:
            win_rate = wins / window_size * 100
            loss_rate = losses / window_size * 100
            draw_rate = draws / window_size * 100
            
            print(f"Episode {episode + 1:6,} | "
                  f"W: {win_rate:5.1f}% | L: {loss_rate:5.1f}% | D: {draw_rate:5.1f}% | "
                  f"States: {len(agent.q_table):,}")
            
            wins = 0
            losses = 0
            draws = 0
    
    # Save
    agent.save_q_table(save_filename)
    
    print("\n" + "=" * 50)
    print("TRAINING COMPLETE!")
    print("=" * 50)
    print(f"Total states learned: {len(agent.q_table):,}")
    
    # Plot
    plot_learning_curve(win_rates)
    
    return agent

def plot_learning_curve(win_rates):
    """Visualize learning progress."""
    plt.figure(figsize=(10, 6))
    episodes = [i * 1000 for i in range(1, len(win_rates) + 1)]
    plt.plot(episodes, win_rates, linewidth=2, color='blue', marker='o', markersize=4)
    plt.xlabel('Training Episodes', fontsize=12)
    plt.ylabel('Win Rate vs Random (%)', fontsize=12)
    plt.title('Q-Learning Agent: Learning Curve (Agent as X vs Random as O)', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 100)
    
    # Reference line
    plt.axhline(y=63, color='red', linestyle='--', alpha=0.5, label='Random X baseline (63%)')
    plt.axhline(y=95, color='green', linestyle='--', alpha=0.5, label='Heuristic level (95%)')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('qlearning_training_curve.png', dpi=300)
    print("\nLearning curve saved to: qlearning_training_curve.png")
    plt.show()

if __name__ == "__main__":
    trained_agent = train_qlearning(num_episodes=50000)
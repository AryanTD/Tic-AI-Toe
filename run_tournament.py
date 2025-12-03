from tournament.runner import Tournament

def main():
    """Run the complete tournament."""
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║         TIC-TAC-TOE AI TOURNAMENT                        ║
    ║         Battle of the Algorithms                          ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Create tournament
    tournament = Tournament(games_per_side=100)
    
    # Setup
    tournament.setup_agents()
    
    # Run
    tournament.run()
    
    # Display results
    tournament.print_standings()
    tournament.print_head_to_head_matrix()
    
    # Save details
    tournament.save_detailed_results()
    
    print("\n✨ Tournament complete! Check tournament_results.txt for details.\n")

if __name__ == "__main__":
    main()
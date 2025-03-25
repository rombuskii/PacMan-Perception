## Structure

The code is organized into several modules:

- `config.py` - Game constants and settings
- `map.py` - Map generation and management
- `entities.py` - Player and enemy entity classes
- `render.py` - Rendering and visualization
- `game.py` - Game logic and main loop with entry point

## How to Run
```bash
# Install requirements
pip install pygame numpy

# Run the game
python game.py
```
## Gameplay

- Use arrow keys to move the player (yellow square)
- Collect all green dots to win
- Avoid the red enemies

## Action Plan

### Week 1 (March 26 - April 2)
1. **Basic AI Infrastructure**
   - Implement Dijkstra's algorithm to create a distance map
   - Create helper functions for distance calculations
   - Set up basic state management for AI modes

2. **Patrol Mode Implementation**
   - Design patrol patterns
   - Implement basic movement logic
   - Just moving left and right?

3. **Sound Perception System**
   - Add sound event handling for pellet collection
   - Create sound-based position tracking

### Week 2 (April 2 - 9)
1. **Chase Mode Implementation**
   - Implement pathfinding towards sound source (We would have distance map from dijkstra?)
   - Add behavior for when sound source is reached

2. **Run Away Mode Implementation**
   - Implement pathfinding away from player
   - Add power pellet effect detection
   - Just running as far as they can from player. (like the assignment we did?)

3. **Testing and Refinement**
   - Test all AI behaviors
   - Fix any bugs or edge cases

### Success Criteria
- Enemies should smoothly transition between different behaviors
- AI should make reasonable decisions based on game state
- Game should remain challenging but fair

# 🏏 Hand Cricket Game

A fun and interactive computer vision-based cricket game where you play cricket using hand gestures! Show different numbers of fingers to bat, bowl, and score runs against the computer opponent.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎮 Game Overview

Hand Cricket is a digital version of the popular hand game where players use finger counting to simulate cricket matches. Using computer vision and hand tracking technology, this game detects your hand gestures in real-time and lets you play an exciting cricket match against an AI opponent.

### 🎯 Game Features

- **Real-time Hand Detection**: Uses MediaPipe for accurate finger counting
- **Immersive Gameplay**: Full-screen gaming experience with dynamic UI
- **Sound Effects**: Engaging audio feedback for different game events
- **Animated Celebrations**: Victory and defeat animations with GIF overlays
- **Two Innings System**: Complete cricket match simulation
- **Auto-progression**: Seamless round transitions
- **Score Tracking**: Real-time score display and round counting

## 🎲 How to Play

### Basic Rules
1. **Finger Counting**: Show 1-6 fingers(except 5) to represent runs 
2. **Batting**: When you're batting, your finger count is your score for that ball
3. **Bowling**: When computer is batting, your finger count tries to get them out
4. **Getting Out**: If your finger count matches the computer's, you're OUT!
5. **Winning**: Score more runs than your opponent in two innings

### Game Controls
- **S**: Start the game
- **N**: Restart game (after game over)
- **Q**: Quit the game

### Game Flow
1. **Innings 1**: You bat first, try to score as many runs as possible
2. **Getting Out**: Match the computer's number and your innings ends
3. **Innings 2**: Computer bats, try to prevent them from beating your score
4. **Victory**: Highest score after both innings wins!

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- Webcam/Camera
- Windows/macOS/Linux

### Required Dependencies
```bash
pip install opencv-python
pip install mediapipe
pip install pygame
pip install imageio
pip install tkinter
```

### Quick Install
```bash
# Clone the repository
git clone https://github.com/Aerex0/hand-cricket.git
cd hand-cricket

# Install dependencies
# tkinter is not in this file , install it side by side
pip install -r requirements.txt

# Run the game
python main.py
```

## 📁 Project Structure

```
hand-cricket/
│
├── main.py          # Main game file
├── requirements.txt         # Python dependencies
├── readme.md               # This file
│
├── assets/                 # Game assets
│   ├── out.wav            # Out sound effect
│   ├── score.wav          # Scoring sound effect
│   ├── Win.wav            # Victory sound
│   ├── lose.wav           # Defeat sound
│   ├── tie.wav            # Tie sound
│   ├── Victory.gif        # Victory animation
│   └── game-over-game.gif # Game over animation
│
└── screenshots/           # Game screenshots 
    ├── gameplay.png
    ├── lose.png
    └── Victory.png
    
```

## 🎵 Asset Requirements

### Audio Files (assets/ folder)
- `out.wav` - Played when player gets out
- `score.wav` - Background music during active gameplay
- `Win.wav` - Victory celebration sound
- `lose.wav` - Defeat sound effect
- `tie.wav` - Tie game sound

### Animation Files (assets/ folder)
- `Victory.gif` - Celebration animation for winning
- `game-over-game.gif` - Game over animation for losing

## 🔧 Technical Details

### Core Technologies
- **OpenCV**: Video capture and image processing
- **MediaPipe**: Hand landmark detection and finger counting
- **Pygame**: Audio management and sound effects
- **ImageIO**: GIF animation loading and processing
- **Tkinter**: Screen resolution detection

### Hand Detection Algorithm
The game uses MediaPipe's hand tracking to detect finger positions:
- Tracks 21 hand landmarks in real-time
- Counts extended fingers based on tip vs. PIP joint positions
- Maps finger count to runs (1-6 range)
- Special handling for thumb detection

### Game Architecture
- **Modular Design**: Separated functions for different game components
- **Resource Loading**: Dedicated functions for assets with error handling
- **State Management**: Clean game state tracking and transitions
- **UI Rendering**: Organized drawing functions for consistent interface

## 🎨 Customization

### Modifying Game Rules
Edit the `get_hand_run()` function to change finger counting logic:
```python
def get_hand_run(hand_landmarks):
    # Modify finger counting algorithm here
    # Current: 0 fingers = 1 run, 1-5 fingers = 1-5 runs, thumb special case = 6 runs
```

### Changing Game Timing
Adjust clock values in the main game loop:
```python
# Modify these ranges for different game pacing
elif 0 <= clock < 5:      # Get Ready phase
elif 5 <= clock < 15:     # Show hand phase  
elif 15 < clock < 25:     # Result display phase
```

### Adding New Sounds
1. Add audio files to `assets/` folder
2. Update the `load_sounds()` function
3. Play sounds using pygame channels in game logic

## 🐛 Troubleshooting

### Common Issues

**Camera not detected:**
```bash
# Check if camera is working
# Try changing camera index in cv.VideoCapture(0) to cv.VideoCapture(1)
```

**Hand detection not working:**
```bash
# Ensure good lighting
# Keep hand clearly visible in camera frame
# Try adjusting MediaPipe confidence parameters
```

**Audio not playing:**
```bash
# Check if audio files exist in assets/ folder
# Verify pygame mixer initialization
# Test system audio settings
```

**Performance issues:**
```bash
# Lower camera resolution in video setup
# Reduce MediaPipe model complexity
# Close other applications using camera/CPU
```

## 🎯 Game Tips

### For Better Hand Detection
- **Good Lighting**: Ensure well-lit environment
- **Clear Background**: Plain background works best
- **Steady Hand**: Keep hand stable during detection phase
- **Proper Distance**: Maintain 1-2 feet from camera
- **Full Hand Visible**: Keep entire hand in camera frame

### Strategy Tips
- **Vary Your Numbers**: Don't be predictable with finger patterns
- **Watch Computer Patterns**: AI uses random selection
- **Timing**: Hand detection happens exactly at clock = 15
- **Practice**: Get comfortable with quick finger transitions

## 📈 Future Enhancements

### Potential Features
- [ ] Multiplayer support (two human players)
- [ ] Difficulty levels for AI opponent
- [ ] Tournament mode with multiple matches
- [ ] Hand gesture training mode
- [ ] Statistics tracking and player profiles
- [ ] Custom team selection and player names
- [ ] Enhanced graphics and animations
- [ ] Mobile app version
- [ ] Online leaderboards
- [ ] Replay system for exciting moments

### Technical Improvements
- [ ] Better hand detection algorithms
- [ ] Gesture recognition for different shot types
- [ ] Machine learning for smarter AI opponent
- [ ] Performance optimizations
- [ ] Cross-platform packaging

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Contribution Ideas
- Bug fixes and performance improvements
- New game modes or features
- Better UI/UX design
- Additional sound effects and animations
- Documentation improvements
- Cross-platform testing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@Aerex0](https://github.com/Aerex0)
- Email: suyashranjan07@gmail.com

## 🙏 Acknowledgments

- **MediaPipe Team**: For excellent hand tracking technology
- **OpenCV Community**: For computer vision tools
- **Pygame Developers**: For audio management capabilities
- **Cricket Fans**: For inspiring this digital version of the classic game

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#🐛-troubleshooting) section
2. Search existing [Issues](https://github.com/Aerex0/hand-cricket-game/issues)
3. Create a new issue with detailed description
4. Join our community discussions

---

**Enjoy playing Hand Cricket! 🏏✋**

*Star ⭐ this repository if you found it helpful!*

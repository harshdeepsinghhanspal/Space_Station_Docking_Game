# 🚀 Sci-Fi Space Docking Game
A retro-styled 2D spacecraft docking simulation built with Pygame. Use realistic thruster controls to align your ship and safely dock with the space station. A fun and visually engaging test of control and precision.

## 🎮 Gameplay Features
- Manual Thruster Navigation: Forward, reverse, strafe, and rotate your spacecraft using realistic vector thrust.
- Thruster Effects: Visual afterburner flames match your movement direction and rotation.
- Radar Mini-Map: Tracks the docking station relative to your ship's position.

## Docking Conditions:
- Safe docking only if your ship is facing upward (330°–30°).
- Speed-based docking evaluation: Green (safe), Orange (caution), Red (crash).
- Collision Detection:
- Colliding with the station body or solar panels causes a crash.
- Docking port allows safe docking if angle and speed are within limits.

## UI: Real-time feedback on forward speed, strafe speed, and angle status.

Pause Menu with Continue and Restart options.

## 🕹️ Controls
Key	Action
↑	Forward thrust
↓	Reverse thrust
←	Strafe left
→	Strafe right
,	Rotate clockwise
.	Rotate counter-clockwise
P	Pause/Unpause
Mouse	Use buttons during pause or restart

## ✅ Win Conditions
Dock safely by:
- Aligning angle between 330°–30°
- Maintaining forward speed in green or orange range
- Touching only the green docking port

## ❌ Fail Conditions
Crash occurs if:
- You touch the station or panels at red speed
- Dock at the wrong angle or at red speed
- Hit any part of the station besides the dock

## 🖥️ Requirements
- Python 3.8+
- Pygame (pip install pygame)

## 🚀 How to Run
Clone or download this repo.

## Install dependencies:
```
pip install pygame
```

## Run the game:
```
python Space_Dock.py
```

## 🧠 Concepts Involved
- Vector math for realistic movement
- Rotational transformations for ship orientation and thrusters
- Collision detection with bounding rectangles
- Radar tracking using scaled vectors
- Game state management and UI design with Pygame

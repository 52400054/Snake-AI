# 🐍 Snake AI: A* Pathfinding & Deep Reinforcement Learning

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame--CE-2.5+-green?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-ML-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

A modernized, ultra-smooth implementation of the classic Snake game in Python. This project is not just a game; it's an AI playground featuring classical pathfinding algorithms and modern Deep Q-Learning (Reinforcement Learning) agents.

---

## ✨ Key Features

*   🎮 **Manual Play:** Enjoy the classic game with responsive controls.
*   🧠 **A* Algorithm Mode:** Watch the AI flawlessly compute the shortest path to the food in real-time, utilizing Manhattan distance heuristics and a custom survival fallback mechanism to avoid self-trapping.
*   🤖 **Deep Q-Learning (DQN):** A Reinforcement Learning agent built with `PyTorch`. The neural network observes its environment (11-state array), makes decisions, and learns from rewards/penalties to train itself.
*   🌟 **Butter-Smooth Rendering:** Built with a decoupled game loop (Fixed Update + Variable Rendering). It utilizes **Linear Interpolation (Lerp)** to ensure fluid graphics at high FPS, regardless of the grid-based game logic speed.

---

## 🛠️ Tech Stack & Architecture

*   **Language:** Python
*   **Engine:** `pygame-ce` (Pygame Community Edition)
*   **Machine Learning:** `torch` (PyTorch)
*   **Architecture:** Clean OOP architecture separating Game Logic (`core`), Graphics/Menu (`ui`), and Artificial Intelligence (`ai`).

### Folder Structure

```text
snake_game/
├── ai/
│   ├── classical/   # A* algorithm and survival logic
│   └── ml/          # Neural Network model and DQN Agent
├── core/            # Config, Fixed-timestep logic, Snake & Food entities
├── ui/              # Main menu state machine & Lerp Renderer
└── main.py          # Unified game loop & event pump
```

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/snake-game-ai.git
   cd snake_game
   ```

2. **Create a Virtual Environment (Optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🕹️ How to Play

Run the main game file:
```bash
python main.py
```

### Controls in Menu:
*   **UP / DOWN Arrows:** Navigate menu options.
*   **ENTER:** Select game mode (Manual, A*, or Machine Learning).

### Controls in Manual Mode:
*   **UP / DOWN / LEFT / RIGHT:** Move the snake.

---

## 🧠 Machine Learning Details

The DQN agent learns by playing the game repeatedly. 
*   **State Space (11 values):** Defines danger (straight, right, left), current direction, and relative food location.
*   **Action Space (3 values):** Go straight, turn right, turn left.
*   **Rewards:** Earning points for grabbing food; receiving penalties for dying.

**Note on Inference Mode:** 
If a `best_model.pth` file is present in the repository, the ML mode is configured to run in **Evaluation/Inference Mode** (`epsilon = 0`). This allows you to immediately watch the fully-trained, optimal AI without waiting for it to learn from scratch!

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Created by Linh - Feel free to ⭐ star the repository if you find it interesting!*


# 🚀 ROS2 Action-Based TurtleBot3 Control

**(Gazebo Simulation | ROS2 Jazzy | Concurrency-Safe Motion Architecture)**

---

## 📌 Overview

This project implements a custom Action-Based motion control architecture for TurtleBot3 (Waffle) running inside Gazebo using ROS2 Jazzy.

The system demonstrates how ROS2 Actions, Executors, and concurrency mechanisms can be applied to control a realistic robot simulation safely and sequentially.

Unlike basic publisher-based control, this architecture enforces structured goal handling, validation policies, and thread-safe execution.

---

## 🤖 Robot Platform

* TurtleBot3 (Waffle model)
* Gazebo Simulation
* Velocity interface: `/cmd_vel`
* Frame reference: `base_link`

---

## 🧠 System Architecture

### Node: turtlebot (Action Server)

Implements:

* Custom `MoveTurtle` Action
* Goal validation policy
* Single active goal enforcement
* Thread-safe goal handling
* Timer-based motion execution
* Cancel support
* MultiThreadedExecutor execution model

---

## 🎯 Custom Action: MoveTurtle

### Goal

* `linear_vel_x`
* `angular_vel_z`
* `duration_sec`

### Result

* `success`
* `message`

---

## ⚙️ Goal Policy & Validation

Goals are rejected if:

* |linear_vel_x| > 3.0
* |angular_vel_z| > 2.0
* duration_sec ≤ 0
* Another goal is currently active

This prevents unsafe or conflicting motion commands.

---

## 🔁 Execution Flow

1️⃣ Goal received
2️⃣ Validation performed
3️⃣ Goal accepted
4️⃣ Velocity published at 10 Hz using timer
5️⃣ Robot moves inside Gazebo
6️⃣ After duration_sec → robot stops
7️⃣ Goal marked as succeeded
8️⃣ Result returned

---

## 🧵 Concurrency & Thread Safety

This project uses:

* MultiThreadedExecutor
* ReentrantCallbackGroup
* Python thread locks
* threading.Event synchronization
* Timers for motion and stop handling

These mechanisms ensure:

✔ Safe parallel callback execution
✔ No race conditions
✔ Controlled goal lifecycle
✔ Proper cancellation behavior

This reflects realistic robotic control architecture rather than simple topic publishing.

---

## ▶ How to Run

### 1️⃣ Set TurtleBot Model

```bash
export TURTLEBOT3_MODEL=waffle
```

---

### 2️⃣ Launch Gazebo Simulation

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

---

### 3️⃣ Run Action Server Node

```bash
ros2 run turtlebot_action_control turtlebot
```

---

### 4️⃣ Send Action Goal

```bash
ros2 action send_goal /move_turtle_turtle2 my_robot_interfaces/action/MoveTurtle \
"{linear_vel_x: 1.0, angular_vel_z: 0.5, duration_sec: 8}"
```

---

## 🧪 Observed Behavior

✔ Valid goal → Robot moves smoothly
✔ Concurrent goal → Rejected
✔ Invalid parameters → Rejected
✔ Cancel request → Motion stops immediately
✔ Sequential goals → Executed correctly

---

## 📊 Concepts Demonstrated

* ROS2 Action Server (Python)
* Custom Action definition
* Goal policy enforcement
* MultiThreadedExecutor
* Callback Groups
* Thread synchronization
* Timer-based motion control
* Gazebo robot simulation
* TwistStamped command publishing
* Frame-aware motion control

---

## 🎯 Why This Project Matters

This project moves beyond basic ROS2 concepts and demonstrates structured robot control architecture applied to a realistic simulation.

It reflects:

* Scalable action-based control design
* Concurrency-aware system thinking
* Safe execution patterns
* Simulation-ready robotics software engineering

These principles are essential before working with:

* ros2_control
* Nav2
* MoveIt2
* Real hardware robots

---

## 🛠 Tech Stack

* ROS2 Jazzy
* Python
* Gazebo
* TurtleBot3
* Actions
* MultiThreadedExecutor
* TF (base_link frame)

---

## 🚀 Future Improvements

* ros2_control integration
* Navigation stack (Nav2) integration
* SLAM mapping
* MoveIt2 arm integration
* Real hardware deployment


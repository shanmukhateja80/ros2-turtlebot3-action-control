#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.action import MoveTurtle
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.action.server import ServerGoalHandle
from geometry_msgs.msg import TwistStamped

from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
import threading


class MoveTurtleNode(Node):
    def __init__(self):
        super().__init__("turtlebot")

        self.goal_lock_ = threading.Lock()
        self.goal_done_event = threading.Event()
        self.goal_handle = None

        # ✅ NORMAL publisher
        self.move_publisher = self.create_publisher(
            TwistStamped, "/cmd_vel", 10
        )

        self.move_turtle_action = ActionServer(
            self,
            MoveTurtle,
            "move_turtle_turtle2",
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            callback_group=ReentrantCallbackGroup()
        )

        self.get_logger().info("Move turtlebot node started ")

    # ------------------- TURTLE CONTROL -------------------

    def start_moving(self, linear_x, angular_z):
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "base_link"

        msg.twist.linear.x = linear_x
        msg.twist.angular.z = angular_z

        self.move_publisher.publish(msg)

    def stop_turtle(self):
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "base_link"

        msg.twist.linear.x = 0.0
        msg.twist.angular.z = 0.0

        self.move_publisher.publish(msg)

    # ---------------- ACTION CALLBACKS ----------------

    def goal_callback(self, goal_request: MoveTurtle.Goal):
        self.get_logger().info("Goal request received")

        with self.goal_lock_:
            if self.goal_handle is not None and self.goal_handle.is_active:
                self.get_logger().warn("Another goal is already running")
                return GoalResponse.REJECT

        if (abs(goal_request.linear_vel_x) > 3.0 or
                abs(goal_request.angular_vel_z) > 2.0 or
                goal_request.duration_sec <= 0):
            self.get_logger().warn("Goal rejected due to limits")
            return GoalResponse.REJECT

        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info("Cancel request received")
        self.stop_turtle()
        self.move_timer.cancel()
        self.stop_timer.cancel()
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle: ServerGoalHandle):
        self.goal_done_event.clear()

        linear_x = goal_handle.request.linear_vel_x
        angular_z = goal_handle.request.angular_vel_z
        duration = goal_handle.request.duration_sec

        with self.goal_lock_:
            self.goal_handle = goal_handle

        self.move_timer = self.create_timer(
            0.1,
            lambda: self.start_moving(linear_x, angular_z)
        )

        self.stop_timer = self.create_timer(
            duration,
            lambda: self.finish_goal(goal_handle)
        )

        self.get_logger().info("Executing turtle movement")

        self.goal_done_event.wait()

        result = MoveTurtle.Result()
        result.success = True
        result.message = "turtle movement completed"
        return result

    def finish_goal(self, goal_handle):
        self.stop_turtle()
        self.move_timer.cancel()
        self.stop_timer.cancel()

        goal_handle.succeed()

        with self.goal_lock_:
            self.goal_handle = None

        self.goal_done_event.set()
        self.get_logger().info("Goal succeeded")


def main(args=None):
    rclpy.init(args=args)
    node = MoveTurtleNode()
    rclpy.spin(node, MultiThreadedExecutor())
    rclpy.shutdown()


if __name__ == "__main__":
    main()

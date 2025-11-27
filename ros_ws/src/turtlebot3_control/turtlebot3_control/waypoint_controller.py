#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import numpy as np
import math

class WaypointController(Node):

    def __init__(self):
        super().__init__('waypoint_controller')

        # Publisher dei comandi
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Subscriber odom
        self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # Waypoints: (x_d, y_d, theta_d)
        self.waypoints = [
            (1.0, 0.0, 0.0),
            (1.0, 1.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 0.0)
        ]
        self.index = 0

        # Guadagni
        self.k1 = 0.5
        self.k2 = 1.5

        self.timer = self.create_timer(0.05, self.control_loop)


    def odom_callback(self, msg):
        """Aggiorna la posa del robot."""
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        # Estrai yaw dal quaternion
        q = msg.pose.pose.orientation
        siny_cosp = 2.0 * (q.w*q.z + q.x*q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y*q.y + q.z*q.z)
        self.theta = math.atan2(siny_cosp, cosy_cosp)


    def control_loop(self):
        if self.index >= len(self.waypoints):
            return

        x_d, y_d, theta_d = self.waypoints[self.index]

        # errore nel frame globale
        ex = self.x - x_d
        ey = self.y - y_d

        # distanza dal waypoint
        dist = math.sqrt(ex**2 + ey**2)

        # se vicino al waypoint → passa al prossimo
        if dist < 0.05:
            self.index += 1
            self.get_logger().info(f"Arrivato al waypoint {self.index}")
            return

        # --- CARTESIAN REGULATOR ---
        # velocità lineare
        v = -self.k1 * (ex*math.cos(self.theta) + ey*math.sin(self.theta))

        # errore angolare
        angle_error = math.atan2(ey, ex) + math.pi - self.theta

        # normalizzazione [-pi, pi]
        angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))

        # velocità angolare
        w = self.k2 * angle_error

        # saturazioni
        v = max(min(v, 0.3), -0.3)
        w = max(min(w, 1.0), -1.0)

        # publish
        msg = Twist()
        msg.linear.x = v
        msg.angular.z = w
        self.cmd_pub.publish(msg)



def main(args=None):
    rclpy.init(args=args)
    node = WaypointController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

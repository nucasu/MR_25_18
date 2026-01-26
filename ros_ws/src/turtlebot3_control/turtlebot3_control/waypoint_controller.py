#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
 
class WaypointController(Node):
 
    def __init__(self):
        super().__init__('waypoint_controller')
 
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
 
        self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
 
        # Initial robot pose
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
 
        # Waypoints: (x, y)
        self.waypoints = [
            (6.0, 0.0),

            # ROOM 1
            (5.5, -3.5),
            (6.5, -4.5),
            (7.0, -2.5),
            (6.0, -0.5),

            (7.0, 2.5),
            (6.0, 3.5),
            (3.0, 4.0),

            # ROOM 2
            (1.0, 4.0),
            (0.5, 2.5),
            (1.0, 1.5),
            (2.0, 4.0),

            (3.0, 4.0),
            (3.5, 2.5),
            (3.0, 0.0),
            (0.0, 0.0),

            (-1.0, 0.5),
            (-1.0, 2.5),
            (-2.0, 3.0), 
            (-6.0, 3.0),

            # ROOM 3
            (-6.2, 0.5),
            (-6.0, -3.5),
            (-7.0, -2.5),
            (-6.2, 0.5),
            (-7.0, 3.5),
            (-5.0, 3.5),

            (-4.5, 0.5),
            (0.0, 0.0)
        ]
     
        self.index = 0
 
        self.k1 = 0.75   # linear velocity gain
        self.k2 = 1.0  # angular velocity gain
 
        # Timer 20 Hz
        self.timer = self.create_timer(0.05, self.control_loop)
 
    def odom_callback(self, msg):
        
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
 
        # Yaw extraction from quaternion
        q = msg.pose.pose.orientation
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.theta = math.atan2(siny_cosp, cosy_cosp)
    
    def normalize(self, a):
        return math.atan2(math.sin(a), math.cos(a)) # Normalize angle to [-pi, pi]

    def control_loop(self):
        
        if self.index >= len(self.waypoints):
            # All waypoints reached, stop the robot
            stop_msg = Twist()
            stop_msg.linear.x = 0.0
            stop_msg.angular.z = 0.0
            self.cmd_pub.publish(stop_msg)
            return
 
        x_d, y_d = self.waypoints[self.index] # Desired posture

        # Cartisian position errors
        ex = x_d - self.x
        ey = y_d - self.y
 
        #dist = math.hypot(ex, ey) # Distance to the desired posture
        dist = math.sqrt(ex**2 + ey**2)
 
        # Check if waypoint is reached
        if dist < 0.05:
            self.get_logger().info(f"Waypoint {self.index + 1} reached!")
            self.index += 1
            return

        # --- CARTESIAN REGULATOR CONTROLLER ---
        v = self.k1 * (ex * math.cos(self.theta) + ey * math.sin(self.theta))
        w = self.k2 * self.normalize(math.atan2(ey, ex) - self.theta)

        # Saturations
        v = max(min(v, 0.8), -0.8)
        w = max(min(w, 1.0), -1.0)
 
        # Publish command
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

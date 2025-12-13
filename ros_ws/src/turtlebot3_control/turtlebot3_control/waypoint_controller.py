#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
 
class WaypointController(Node):
 
    def __init__(self):
        super().__init__('waypoint_controller')
 
        # Publisher dei comandi
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
 
        # Subscriber odom
        self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
 
        # Posa del robot
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
 
        # Waypoints: (x, y)
        self.waypoints = [
            (6.0, 0.0),

            # STANZA 1
            (5.5, -3.5),
            (6.5, -4.5),
            (7.0, -2.5),
            (6.0, -0.5),

            (7.0, 2.5),
            (6.0, 3.5),

            # STANZA 2
            (1.0, 4.0),
            (0.5, 2.5),
            (1.0, 1.5),
            (2.0, 4.0),

            (3.0, 4.0),
            (3.0, 0.0),
            (0.0, 0.0),

            (-1.0, 0.5),
            (-1.0, 2.5),
            (-6.0, 3.0),

            #STANZA 3
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
 
        # Guadagni
        self.k1 = 1.5   # velocità lineare
        self.k2 = 1.5   # velocità angolare
 
        # Timer di controllo (20 Hz)
        self.timer = self.create_timer(0.05, self.control_loop)
 
    def odom_callback(self, msg):
        """Aggiorna la posa del robot dal topic /odom."""
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
 
        # Estrai yaw dal quaternion
        q = msg.pose.pose.orientation
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.theta = math.atan2(siny_cosp, cosy_cosp)
 
    def control_loop(self):
        
        if self.index >= len(self.waypoints):
            # Tutti i waypoint completati, ferma il robot
            stop_msg = Twist()
            self.cmd_pub.publish(stop_msg)
            return
 
        x_d, y_d = self.waypoints[self.index]
 
        # --- ERRORE NEL FRAME DEL ROBOT ---
        dx = x_d - self.x
        dy = y_d - self.y
 
        ex = math.cos(self.theta) * dx + math.sin(self.theta) * dy
        ey = -math.sin(self.theta) * dx + math.cos(self.theta) * dy
 
        dist = math.hypot(ex, ey)
 
        # Se vicino al waypoint → passa al prossimo
        if dist < 0.05:
            self.get_logger().info(f"Waypoint {self.index + 1} raggiunto!")
            self.index += 1
            return

        # --- CARTESIAN REGULATOR ---
        v = self.k1 * ex
        w = self.k2 * math.atan2(ey, ex)

        # Saturazioni
        v = max(min(v, 0.8), -0.8)
        w = max(min(w, 1.0), -1.0)
 
        # Pubblica comandi
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

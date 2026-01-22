import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np
from cv_bridge import CvBridge

class SemanticToMono(Node):
    def __init__(self):
        super().__init__('semantic_converter')

        self.bridge = CvBridge()

        self.sub = self.create_subscription(
            Image,
            '/semantic/labels_map',
            self.callback,
            10
        )

        self.pub = self.create_publisher(
            Image,
            '/semantic/labels',
            10
        )

        self.get_logger().info('RGB8 → mono8 converter started ...')

    def callback(self, msg):
        
        rgb = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
        class_id = rgb[:, :, 2].astype(np.uint8)
        mono_msg = self.bridge.cv2_to_imgmsg(class_id, encoding='mono8')
        mono_msg.header = msg.header
        self.pub.publish(mono_msg)

def main(args=None):
    rclpy.init(args=args)
    node = SemanticToMono()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


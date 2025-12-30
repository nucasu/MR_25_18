import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np

class LabelConverter(Node):
    def __init__(self):
        super().__init__('label_converter')

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

    def callback(self, msg):
        # Converti il buffer in array numpy
        img = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3)

        # Estrai il canale giusto (semantic segmentation)
        labels = img[:, :, 0]

        # Crea il nuovo messaggio mono8
        out = Image()
        out.header = msg.header
        out.height = msg.height
        out.width = msg.width
        out.encoding = 'mono8'
        out.step = msg.width
        out.data = labels.tobytes()

        self.pub.publish(out)

def main(args=None):
    rclpy.init(args=args)
    node = LabelConverter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

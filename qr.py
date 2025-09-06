import cv2
from pyzbar.pyzbar import decode

def main():
    # Open default camera (0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        return

    print("Press 'q' to quit.")

    while True:
        # Read frame from camera
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Decode QR codes/barcodes in the frame
        decoded_objects = decode(frame)

        for obj in decoded_objects:
            # Decode data
            qr_data = obj.data.decode('utf-8')
            qr_type = obj.type

            # Print data
            print(f"[{qr_type}] Data: {qr_data}")

            # Draw bounding box
            points = obj.polygon
            if len(points) > 4:  # Sometimes the polygon has more than 4 points
                hull = cv2.convexHull(
                    np.array([point for point in points], dtype=np.float32)
                )
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points

            # Draw lines between points
            for i in range(len(hull)):
                pt1 = hull[i]
                pt2 = hull[(i + 1) % len(hull)]
                cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

            # Display data on the frame
            cv2.putText(frame, qr_data, (obj.rect.left, obj.rect.top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # Show the result
        cv2.imshow("QR Code Scanner", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import numpy as np  # Needed for polygon processing
    main()

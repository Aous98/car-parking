import cv2
import pickle
import os

# Load the image
image = cv2.imread('carParkImg.png')
original_image = image.copy()
width, height = 107, 47

# Load existing positions from the pickle file or create an empty list
if os.path.exists('parking_positions.pkl'):
    with open('parking_positions.pkl', 'rb') as f:
        positions = pickle.load(f)
else:
    positions = []


# Function to draw rectangles
def draw_rectangle(event, x, y, flags, param):
    global image, positions, original_image

    if event == cv2.EVENT_LBUTTONDOWN:
        start_x, start_y = x, y
        end_x, end_y = x + width, y + height
        pos1 = [start_x, start_y]
        pos2 = [end_x, end_y]
        positions.append([pos1, pos2])
        cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

    elif event == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(positions):
            start_x, start_y = pos[0]
            end_x, end_y = pos[1]
            if start_x < x < end_x and start_y < y < end_y:
                positions.pop(i)
                break

        # Redraw all rectangles
        image = original_image.copy()
        for pos in positions:
            start_x, start_y = pos[0]
            end_x, end_y = pos[1]
            cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

    cv2.imshow('Image with Rectangles', image)


# Draw existing rectangles
for pos in positions:
    start_x, start_y = pos[0]
    end_x, end_y = pos[1]
    cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

# Set up mouse callback
cv2.namedWindow('Image with Rectangles')
cv2.setMouseCallback('Image with Rectangles', draw_rectangle)

# Main loop
while True:
    cv2.imshow('Image with Rectangles', image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        # Save positions to pickle file
        with open('parking_positions.pkl', 'wb') as f:
            pickle.dump(positions, f)
        print("Positions saved to parking_positions.pkl")
        break

cv2.destroyAllWindows()

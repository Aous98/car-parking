import cv2
import cvzone
import pickle
import numpy as np

with open('parking_positions.pkl', 'rb') as f:
    positions = pickle.load(f)

width, height = 107, 47

# Video
cap = cv2.VideoCapture('carPark.mp4')

def put_text_with_background(img, text, position, font_scale, thickness, text_color, bg_color):
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
    text_offset_x, text_offset_y = position
    box_coords = ((text_offset_x, text_offset_y + 5), (text_offset_x + text_width + 2, text_offset_y - text_height - 5))
    cv2.rectangle(img, box_coords[0], box_coords[1], bg_color, cv2.FILLED)
    cv2.putText(img, text, (text_offset_x, text_offset_y), font, font_scale, text_color, thickness)

while True:
    spaces = 0
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresholdImg = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    medianImg = cv2.medianBlur(thresholdImg, 9)

    cropped_images = []
    cropped_median_images = []

    for pos in positions:
        start_x, start_y = pos[0]
        end_x, end_y = pos[1]
        cropped = img[start_y:end_y, start_x:end_x]
        cropped_median = medianImg[start_y:end_y, start_x:end_x]
        cropped_images.append(cropped)
        cropped_median_images.append(cropped_median)

    for i, (pos, cropped_median) in enumerate(zip(positions, cropped_median_images)):
        start_x, start_y = pos[0]
        white_pixels = np.count_nonzero(cropped_median == 255)

        if white_pixels > 790:
            cv2.rectangle(img, (start_x, start_y), (start_x + width, start_y + height), (0, 0, 255), 2)
            put_text_with_background(img, "Not Available", (start_x, start_y + height - 10),
                                     0.3, 1, (0, 0, 255), (255, 192, 203))  # White text, Pink background
        else:
            spaces += 1
            cv2.rectangle(img, (start_x, start_y), (start_x + width, start_y + height), (0, 255, 0), 4)
            put_text_with_background(img, "You Can Park", (start_x, start_y + height - 10),
                                     0.3, 1, (255, 0, 0), (255, 192, 203))  # White text, Pink background
    cvzone.putTextRect(img, f'Free: {spaces}/{len(positions)}', (20, 40), thickness=3, offset=20,
                       colorR=(0, 200, 0))
    cv2.imshow('Image', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

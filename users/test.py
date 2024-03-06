import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Prepare data generator for standardizing frames before sending them into the model.
data_generator = ImageDataGenerator(samplewise_center=True, samplewise_std_normalization=True)

# Loading the model.
MODEL_NAME = 'users/asl_alphabet_{}.h5'.format(9575)
model = load_model(MODEL_NAME)

# Setting up the input image size and frame crop size.
IMAGE_SIZE = 200
CROP_SIZE = 400

# Creating list of available classes stored in classes.txt.
classes_file = open("users/classes.txt")
classes_string = classes_file.readline()
classes = classes_string.split()
classes.sort()  # The predict function sends out output in sorted order.

# Preparing cv2 for webcam feed
cap = cv2.VideoCapture(0)

# Create a flag to capture a frame when a key is pressed.
capture_frame = False

# Create a separate window for displaying predicted text.
cv2.namedWindow("Prediction", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Prediction", 400, 100)

# Initialize prediction_text outside the loop
prediction_text = ""

while True:
    # Capture frame-by-frame.
    ret, frame = cap.read()

    # Target area where the hand gestures should be.
    cv2.rectangle(frame, (0, 0), (CROP_SIZE, CROP_SIZE), (0, 255, 0), 3)

    # Check if capture_frame is True, then capture a frame.
    if capture_frame:
        # Preprocessing the frame before input to the model.
        cropped_image = frame[0:CROP_SIZE, 0:CROP_SIZE]
        resized_frame = cv2.resize(cropped_image, (IMAGE_SIZE, IMAGE_SIZE))
        reshaped_frame = (np.array(resized_frame)).reshape((1, IMAGE_SIZE, IMAGE_SIZE, 3))
        frame_for_model = data_generator.standardize(np.float64(reshaped_frame))

        # Predicting the frame.
        prediction = np.array(model.predict(frame_for_model))
        predicted_class = classes[prediction.argmax()]  # Selecting the max confidence index.

        # Preparing output based on the model's confidence.
        prediction_text = 'Prediction: {}'.format(predicted_class)
        confidence = 'Confidence: {:.2f}%'.format(prediction[0, prediction.argmax()] * 100)
        print(prediction_text, confidence)

        # Reset the capture_frame flag.
        capture_frame = False

    # Display the image with prediction.
    cv2.imshow('frame', frame)

    # Display the predicted text in the separate window.
    prediction_window = np.zeros((100, 400, 3), dtype=np.uint8)
    cv2.putText(prediction_window, prediction_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Prediction", prediction_window)
    
    # Press 'c' to capture a frame.
    k = cv2.waitKey(1) & 0xFF
    if k == ord('c'):
        capture_frame = True
    elif k == ord('q'):
        break

# When everything is done, release the capture.
cap.release()
cv2.destroyAllWindows()
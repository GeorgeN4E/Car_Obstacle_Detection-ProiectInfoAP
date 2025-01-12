#conda activate myenv

from ultralyticsplus import YOLO, render_result

# Load model
#model = YOLO('keremberke/yolov8m-pothole-segmentation')

model = YOLO("C:\\Users\\georg\\Downloads\\yolov8s.pt")
# Set model parameters
model.overrides['conf'] = 0.1  # Lower confidence threshold
model.overrides['iou'] = 0.45
model.overrides['agnostic_nms'] = False
model.overrides['max_det'] = 1000

# Set image
image = 'pothole_2.jpeg'

# Perform inference
results = model.predict(image)

# Debug output
print("Bounding Boxes:", results[0].boxes)
print("Masks:", results[0].masks)

# Visualize results
render = render_result(model=model, image=image, result=results[0])
render.show()

import supervision as sv
import ultralytics
from ultralytics import YOLO
import numpy as np
import os

MODEL = "yolov8x.pt"
SOURCE_VIDEO_PATH = os.path.join(os.getcwd(), "uploads\\")
model = YOLO(MODEL)
model.fuse()

def model_trainer(videoName):
    print("Model training started")
    print("videoName: ", videoName)

    # dict maping class_id to class_name
    CLASS_NAMES_DICT = model.model.names

    # class_ids of interest - car, motorcycle, bus and truck
    selected_classes = [2, 3, 5, 7]
    # create frame generator
    generator = sv.get_video_frames_generator(f"uploads\\{videoName}")
    # create instance of BoxAnnotator
    box_annotator = sv.BoxAnnotator(
        thickness=4, text_thickness=4, text_scale=2)
    # acquire first video frame
    iterator = iter(generator)
    frame = next(iterator)
    # model prediction on single frame and conversion to supervision Detections
    results = model(frame, verbose=False)[0]

    # convert to Detections
    detections = sv.Detections.from_ultralytics(results)
    # only consider class id from selected_classes define above
    detections = detections[np.isin(detections.class_id, selected_classes)]

    # format custom labels
    labels = [
        f"{CLASS_NAMES_DICT[class_id]} {confidence:0.2f}"
        for confidence, class_id in zip(detections.confidence, detections.class_id)
    ]

    # annotate and display frame
    anotated_frame = box_annotator.annotate(
        scene=frame, detections=detections, labels=labels)

    # TODO: save annotated frame to disk
    # sv.save_image(anotated_frame, "images/annotated_frame.jpg")
    with sv.ImageSink(target_dir_path="images\\", overwrite=True) as sink:
        sink.save_image(anotated_frame, "annotated_frame.jpg", (16, 16))
    # sv.plot_image(anotated_frame, (16,16))
    # settings

    TARGET_VIDEO_PATH = os.path.join(os.getcwd(), "output\\counted.mp4")
    sv.VideoInfo.from_video_path(f"uploads\\{videoName}")

    # process the whole video
    sv.process_video(
        source_path=f"uploads\\{videoName}",
        target_path=f"output\\counted.mp4",
        callback=callback
    )

# define call back function to be used in video processing


def callback(frame: np.ndarray, index: int) -> np.ndarray:
    selected_classes = [2, 3, 5, 7]
    LINE_START = sv.Point(50, 1500)
    LINE_END = sv.Point(3840-50, 1500)
    # create BYTETracker instance
    byte_tracker = sv.ByteTrack(
        track_thresh=0.25, track_buffer=30, match_thresh=0.8, frame_rate=30)
    videoName = "vehicle-counting.mp4"
    # create VideoInfo instance
    video_info = sv.VideoInfo.from_video_path(f"uploads\\{videoName}")

    # create frame generator
    generator = sv.get_video_frames_generator(f"uploads\\{videoName}")

    # create LineZone instance, it is previously called LineCounter class
    line_zone = sv.LineZone(start=LINE_START, end=LINE_END)

    # create instance of BoxAnnotator
    box_annotator = sv.BoxAnnotator(
        thickness=4, text_thickness=4, text_scale=2)

    # create instance of TraceAnnotator
    trace_annotator = sv.TraceAnnotator(thickness=4, trace_length=50)

    # create LineZoneAnnotator instance, it is previously called LineCounterAnnotator class
    line_zone_annotator = sv.LineZoneAnnotator(
        thickness=4, text_thickness=4, text_scale=2)
    # model prediction on single frame and conversion to supervision Detections
    results = model(frame, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)
    # only consider class id from selected_classes define above
    detections = detections[np.isin(detections.class_id, selected_classes)]
    # tracking detections
    detections = byte_tracker.update_with_detections(detections)
    labels = [
        f"#{tracker_id} {model.model.names[class_id]} {confidence:0.2f}"
        for confidence, class_id, tracker_id
        in zip(detections.confidence, detections.class_id, detections.tracker_id)
    ]
    annotated_frame = trace_annotator.annotate(
        scene=frame.copy(),
        detections=detections
    )
    annotated_frame = box_annotator.annotate(
        scene=annotated_frame,
        detections=detections,
        labels=labels)

    # update line counter
    line_zone.trigger(detections)
    # return frame with box and line annotated result
    return line_zone_annotator.annotate(annotated_frame, line_counter=line_zone)


if __name__ == '__main__':
    model_trainer("vehicle-counting.mp4")

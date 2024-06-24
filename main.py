from snapshot import capture_snapshot
from posize import ImageDetector
from crop import VideoProcessor
from folder import get_files_with_extension
from video_edit import FinalVideoCreator
from ocr import detect_text_in_image
from textpng import FinalImageCreator
from whitebgtext import crop_text_from_upper_half

def final_crop_video(input_video, output_path):
    """
    Process a video to capture a snapshot, detect the main image, crop the video, and return the detected text.

    :param input_video: Path to the input video file.
    :param output_path: Path to save the cropped video file.
    :return: Detected text from the snapshot.
    """
    # Step 1: Capture a snapshot from the video
    snapshot_path = 'temp/snapshot.png'
    capture_snapshot(video_path=input_video, output_path=snapshot_path)
    print("Screenshot captured.")

    # Step 2: Detect position and size of the main image in the snapshot
    detector = ImageDetector(snapshot_path, min_width=100, min_height=100)
    detector.process_image()
    x, y, w, h = detector.detect_main_image()
    print("Position defined.")

    # Step 3: Perform OCR on the snapshot to detect text
    crop_text_from_upper_half(snapshot_path, 'temp\\ocrtext.png')
    detected_text = detect_text_in_image('temp\\ocrtext.png')
    print("Text detected:", detected_text)

    # Step 4: Crop the video based on the detected position and size
    processor = VideoProcessor(input_video, x, y, w, h, output=output_path, temp='temp/temp.mp4')
    processor.process_video()
    print("Video processed successfully.")

    return detected_text

# Step 5: Get list of video files with .mp4 extension in the 'ex' folder
file_list = get_files_with_extension('ex', 'mp4')
print(f"Found {len(file_list)} video files.")

# Step 6: Process each video file
for idx, video_file in enumerate(file_list):
    # Process the video and get detected text
    detected_text = final_crop_video(video_file, f'r/{idx}.mp4')

    # Step 7: Create a final image with the detected text
    text_image = FinalImageCreator()
    text_image.create_final_image(detected_text, "temp/outputtext.png")
    print("Text image created.")

    # Step 8: Create the final edited video with overlaid text image
    creator = FinalVideoCreator(f'r/{idx}.mp4', "temp/outputtext.png", "assets/grain.png", f'edit//{idx}.mp4', carousels=True,audio=True,audio_path='assets\\audi.mp3')
    creator.create_final_video()
    print(f"Final video created: r/edit{idx}.mp4")

print("All videos processed successfully.")

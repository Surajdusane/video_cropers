from moviepy.editor import ColorClip, VideoFileClip, CompositeVideoClip, ImageClip, vfx
from moviepy.video.fx.all import resize
from ratio import get_video_recommendation
from delete import delete_file
import json

class FinalVideoCreator:
    def __init__(self, overlay_video_path, overlay_image_path, grain, output_video_path, delete=False):
        self.overlay_video_path = overlay_video_path
        self.overlay_image_path = overlay_image_path
        self.grain = grain
        self.output_video_path = output_video_path
        self.delete = delete

    def video_size(self):
        video_ratio = get_video_recommendation(self.overlay_video_path)
        ratio_map = {
            (1, 1): "1:1",
            (2, 1): "2:1",
            (1, 2): "1:2",
            (9, 16): "9:16",
            (16, 9): "16:9",
            (2, 3): "2:3",
            (3, 2): "3:2",
            None: "9:16"
        }
        ratio_vid_key = ratio_map.get(video_ratio, None)
        if ratio_vid_key is None:
            raise ValueError("Unsupported video ratio")
        
        with open("assets/video_pns.json", 'r') as file:
            ratio_data = json.load(file)
            ratio_vid = ratio_data[ratio_vid_key]
        
        self.main_height = ratio_vid["height"]
        self.main_width = ratio_vid["width"]
        self.main_top = ratio_vid["top"]
        self.main_left = ratio_vid["left"]

    def create_final_video(self):
        # Initialize video size attributes
        self.video_size()

        # Load the overlay video
        overlay_video = VideoFileClip(self.overlay_video_path)
        overlay_video = overlay_video.fx(vfx.mirror_x)

        # Set the duration and resolution for the white screen
        duration = overlay_video.duration  # seconds
        width, height = 1080, 1920  # resolution

        # Create a blank white clip
        white_clip = ColorClip(size=(width, height), color=(255, 255, 255), duration=duration)

        # Set the position and size for the overlay video
        # Assuming 1 cm = 37.7953 pixels (approx)
        def Cm(value):
            return value * 37.7953

        left = Cm(self.main_left)
        top = Cm(self.main_top)
        overlay_width = Cm(self.main_width)
        overlay_height = Cm(self.main_height)

        # Resize the overlay video to the specified width and height
        overlay_video_resized = resize(overlay_video, newsize=(overlay_width, overlay_height))

        # Position the overlay video on the white screen
        overlay_video_positioned = overlay_video_resized.set_position((left, top))

        # Load the image overlay
        overlay_image = ImageClip(self.overlay_image_path)

        # Resize and position the image overlay
        overlay_image = self.resize_and_position_overlay(overlay_image, overlay_video.duration)

        # Load the grain overlay
        grain_overlay = ImageClip(self.grain)

        # Resize and position the grain overlay
        grain_overlay = self.resize_and_position_overlay_grain(grain_overlay, overlay_video.duration)

        # Composite the overlays on top of the white screen
        final_video = CompositeVideoClip([white_clip, overlay_video_positioned, overlay_image, grain_overlay])

        # Write the final video to a file
        final_video.write_videofile(self.output_video_path, codec="libx264")

        #deleting input video
        if(self.delete):
            delete_file(self.overlay_video_path)
            print(f"{self.overlay_video_path} Video is deleted!!")


    def resize_and_position_overlay(self, overlay, duration):
        # Convert centimeters to pixels
        # Assuming 1 cm = 37.7952756 pixels (standard for many videos)
        # You may need to adjust this value based on your specific video resolution
        cm_to_pixels = 37.7952756
        height_pixels = 5.72 * cm_to_pixels
        width_pixels = 17.55 * cm_to_pixels
        top_pixels = 4.07 * cm_to_pixels
        left_pixels = 5.72 * cm_to_pixels

        # Resize the overlay image if needed
        overlay = overlay.set_duration(duration)
        overlay = overlay.resize(newsize=(width_pixels, height_pixels))

        # Position the overlay
        overlay = overlay.set_position((left_pixels, top_pixels))

        return overlay

    def resize_and_position_overlay_grain(self, overlay, duration):
        # Convert centimeters to pixels
        # Assuming 1 cm = 37.7952756 pixels (standard for many videos)
        # You may need to adjust this value based on your specific video resolution
        def Cm(value):
            return value * 37.7953

        height_pixels = Cm(self.main_height)
        width_pixels = Cm(self.main_width)
        top_pixels = Cm(self.main_top)
        left_pixels = Cm(self.main_left)

        # Resize the overlay image if needed
        overlay = overlay.set_duration(duration)
        overlay = overlay.resize(newsize=(width_pixels, height_pixels))

        # Position the overlay
        overlay = overlay.set_position((left_pixels, top_pixels))

        return overlay

import cv2
import moviepy.editor as mp
import threading

class VideoProcessor:
    def __init__(self, input_path, x, y, width, height, output, temp):
        self.input_path = input_path
        self.temp_output_path = temp
        self.final_output_path = output
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def crop_video(self):
        cap = cv2.VideoCapture(self.input_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_size = (int(self.width), int(self.height))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.temp_output_path, fourcc, fps, frame_size)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cropped_frame = frame[self.y:self.y + self.height, self.x:self.x + self.width]
            out.write(cropped_frame)

        cap.release()
        out.release()

    def combine_audio(self):
        video_clip = mp.VideoFileClip(self.temp_output_path)
        audio_clip = mp.VideoFileClip(self.input_path).audio
        
        # Ensure the video and audio have the same duration
        video_duration = video_clip.duration
        audio_clip = audio_clip.subclip(0, video_duration)

        # Trim the last half second
        trim_duration = 0.4
        trimmed_video_clip = video_clip.subclip(0, video_duration - trim_duration)
        trimmed_audio_clip = audio_clip.subclip(0, video_duration - trim_duration)

        final_clip = trimmed_video_clip.set_audio(trimmed_audio_clip)
        final_clip.write_videofile(self.final_output_path, codec='libx264', audio_codec='aac', preset='fast')

    def process_video(self):
        # Create threads for cropping video and combining audio
        crop_thread = threading.Thread(target=self.crop_video)
        crop_thread.start()
        crop_thread.join()  # Ensure cropping is finished before combining audio

        combine_thread = threading.Thread(target=self.combine_audio)
        combine_thread.start()
        combine_thread.join()


# Example usage
# if __name__ == "__main__":
#     input_video_path = 'ex.mp4'
#     x = 178
#     y = 408
#     width = 722
#     height = 1281

#     processor = VideoProcessor(input_video_path, x, y, width, height)
#     processor.process_video()

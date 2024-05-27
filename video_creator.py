import os
from helper import zodiac_signs, clear_and_wait
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from moviepy.video.fx.all import crop

def create_video(phrases):
  clear_and_wait()  # Clear console or perform any necessary setup

  # Verify if folder 'audio' exists, if not, create it
  video_folder = 'video'
  if not os.path.exists(video_folder):
    os.makedirs(video_folder)

  # Define paths for audio and images
  audio_folder = 'audio'
  image_folder = 'image'

  # Frame size for the video in portrait mode
  frame_size = (1080, 1920)

  # Collect all image and audio files for the sign
  for sign_name in zodiac_signs:
    video_clips = []
    phrases_number = len(phrases[sign_name]['phrases'])

    for i in range(phrases_number):
      image_path = f"{image_folder}/{sign_name}_{i}.jpg"
      audio_path = f"{audio_folder}/{sign_name}_{i}.wav"

      # Get audio duration
      audio_clip = AudioFileClip(audio_path)
      video_duration = audio_clip.duration

      # Create an image clip
      image_clip = ImageClip(image_path).set_duration(video_duration)

      # Moving across the image
      image_clip = image_clip.set_position(lambda t: ('center', t * 10 + 50))

      # Combine the image and audio clips
      video_clip = CompositeVideoClip([image_clip.set_audio(audio_clip)])

      # Add the video clip to the list
      video_clips.append(video_clip)
    
    # Concatenate all video clips for the sign
    concatenated_clip = concatenate_videoclips(video_clips)

    # Calculate the crop dimensions
    (concatenated_clip_width, concatenated_clip_height) = concatenated_clip.size
    crop_width = concatenated_clip_height * 9/16

    x1, x2 = (concatenated_clip_width - crop_width)//2, (concatenated_clip_width + crop_width)//2
    y1, y2 = 0, concatenated_clip_height

    # Crop the video clip to the frame size
    concatenated_clip = crop(concatenated_clip, x1=x1, y1=y1, x2=x2, y2=y2)

    # Save the concatenated video cli
    concatenated_clip.write_videofile(f"{video_folder}/{sign_name}.mp4", codec='libx264', fps=24)

  clear_and_wait()  # Clear console or perform any necessary cleanup

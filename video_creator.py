import os
from helper import zodiac_signs, clear_and_wait
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

def create_video(phrases):
  clear_and_wait()  # Clear console or perform any necessary setup

  # Verify if folder 'audio' exists, if not, create it
  video_folder = 'video'
  if not os.path.exists(video_folder):
    os.makedirs(video_folder)

  # Define paths for audio and images
  audio_folder = 'audio'
  image_folder = 'image'

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

      # Combine the image and audio clips
      video_clip = CompositeVideoClip([image_clip.set_audio(audio_clip)])

      # Add the video clip to the list
      video_clips.append(video_clip)
    
    # Concatenate all video clips for the sign
    concatenated_clip = concatenate_videoclips(video_clips)
    concatenated_clip.write_videofile(f"{video_folder}/{sign_name}.mp4", codec='libx264', fps=24)

  clear_and_wait()  # Clear console or perform any necessary cleanup

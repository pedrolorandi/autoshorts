import os
from helper import zodiac_signs, clear_and_wait
from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, TextClip, concatenate_videoclips, CompositeVideoClip, CompositeAudioClip
from moviepy.video.fx.all import crop

def process_clip(image_path, audio_path):
  # Process an image and audio file into a video clip
  audio_clip = AudioFileClip(audio_path).set_start(0.5)
  video_duration = audio_clip.duration + 1

  image_clip = ImageClip(image_path).set_duration(video_duration)
  image_clip = image_clip.resize(lambda t: 1 + (0.047 * t)).set_position(('center'))
  
  return CompositeVideoClip([image_clip.set_audio(audio_clip)])

def crop_clip(video_clip, frame_size):
  # Crop the video clip to the specified frame size
  (video_clip_width, video_clip_height) = video_clip.size
  crop_width = video_clip_height * 9/16

  x1, x2 = (video_clip_width - crop_width)//2, (video_clip_width + crop_width)//2
  y1, y2 = 0, video_clip_height

  return crop(video_clip, x1=x1, y1=y1, x2=x2, y2=y2)

def prepare_particle_clip(particle_video_path, frame_size):
  # Prepare the particle clip by resizing and cropping
  particle_clip = VideoFileClip(particle_video_path)
  particle_clip = particle_clip.resize(width=frame_size[0], height=frame_size[1])
  return crop_clip(particle_clip, frame_size)

def create_video(phrases):
  clear_and_wait()  # Clear console or perform any necessary setup

  video_folder = 'video'
  os.makedirs(video_folder, exist_ok=True)

  audio_folder = 'audio'
  image_folder = 'image'
  particle_video_path = 'video/Particle.mp4'
  background_audio_path = 'audio/BG_music.mp3'
  frame_size = (1080, 1920)

   # Prepare the particle clip
  particle_clip = prepare_particle_clip(particle_video_path, frame_size)

  # Load and adjust the background audio
  background_audio = AudioFileClip(background_audio_path).volumex(0.1)  # Lower the volume

  # Process videos for each zodiac sign
  for sign_name in zodiac_signs:
    video_clips = []

    for i in range(len(phrases[sign_name]['phrases'])):
      image_path = f"{image_folder}/{sign_name}_{i}.jpg"
      audio_path = f"{audio_folder}/{sign_name}_{i}.wav"
      video_clips.append(process_clip(image_path, audio_path))
    
    concatenated_clip = concatenate_videoclips(video_clips)
    concatenated_clip = crop_clip(concatenated_clip, frame_size)

    # Set the duration of the particle clip to match the concatenated clip
    particle_clip = particle_clip.set_duration(concatenated_clip.duration)
    background_audio = background_audio.set_duration(concatenated_clip.duration)

    # Combine the concatenated clip and particle clip
    final_clip = CompositeVideoClip([concatenated_clip, particle_clip.set_position('center').set_opacity(0.25)])
    final_clip = final_clip.set_audio(CompositeAudioClip([final_clip.audio, background_audio]))

    # Save the final video
    final_clip.write_videofile(f"{video_folder}/{sign_name}.mp4", codec='libx264', fps=24, threads=4)

  clear_and_wait()  # Clear console or perform any necessary cleanup

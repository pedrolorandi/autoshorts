import os
from dotenv import load_dotenv
import openai
from helper import zodiac_signs, clear_and_wait
from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, TextClip, concatenate_videoclips, CompositeVideoClip, CompositeAudioClip
from moviepy.video.fx.all import crop

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

frame_size = (1080, 1920)

def get_phrases_timings(audio_path):
  """
  Transcribe the audio and get the timings for each word.
  """
  print(f"Transcribing audio for {audio_path}")
  try:
    client = openai.OpenAI()
    with open(audio_path, "rb") as audio_file:
      transcript = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="verbose_json",
        timestamp_granularities=["word"]
      )
    return transcript.words
  except Exception as e:
    print(f"Error transcribing audio for {audio_path}: {e}")
    return []

def split_sentences(timings, delay):
  """
  Split the transcribed words into sentences based on a delay and punctuation marks.
  """
  sentences = []
  current_sentence = ""
  current_start_time = None

  for timing in timings:
    word = timing['word']
    start_time = timing['start']
    end_time = timing['end']
    
    if not current_start_time:
      current_start_time = start_time
    
    if current_sentence and word not in ",.;!?":
      current_sentence += " "
    current_sentence += word

    if len(current_sentence.split()) >= 3 or word in ",.;!?":
      sentences.append({
        'sentence': current_sentence.strip(), 
        'start': current_start_time + delay, 
        'end': end_time + delay
      })
    current_sentence = ""
    current_start_time = None

  if current_sentence:
    sentences.append({
      'sentence': current_sentence.strip(), 
      'start': current_start_time + delay, 
      'end': end_time + delay
    })

  return sentences

def create_text_clip(text, start_time, end_time, font_size, color, opacity, offset=(0, 0)):
  """
  Create a TextClip with specified properties and position offset.
  """
  clip = TextClip(text, fontsize=font_size, color=color, font='Franklin-Gothic-Heavy').set_opacity(opacity)
  return clip.set_start(start_time).set_end(end_time).set_position(lambda t: (offset[0], offset[1]))

def create_captions(audio_path, frame_size, delay=0.5):
  """
  Create caption clips for the audio file.
  """
  timings = get_phrases_timings(audio_path)
  sentences = split_sentences(timings, delay)
  
  text_clips = []
  for sentence in sentences:
    text = sentence['sentence'].lower()
    start_time = sentence['start']
    end_time = sentence['end']
    shadow_clip = create_text_clip(text, start_time, end_time, 40, 'black', 0.5, (3, 3))
    text_clip = create_text_clip(text, start_time, end_time, 40, 'white', 1)
    composed_clip = CompositeVideoClip([shadow_clip, text_clip])
    text_clips.append(composed_clip.set_position(('center', 'center')))
  
  return text_clips

def process_clip(image_path, audio_path, frame_size, delay=0.5):
  """
  Process an image and audio file into a video clip with captions.
  """
  audio_clip = AudioFileClip(audio_path).set_start(delay)
  video_duration = audio_clip.duration + (delay * 2)

  image_clip = ImageClip(image_path).set_duration(video_duration)
  image_clip = image_clip.resize(lambda t: 1 + (0.047 * t)).set_position(('center'))

  text_clips = create_captions(audio_path, frame_size)

  return CompositeVideoClip([image_clip.set_audio(audio_clip)] + text_clips)

def crop_clip(video_clip, frame_size):
  """
  Crop the video clip to the specified frame size.
  """
  (video_clip_width, video_clip_height) = video_clip.size
  crop_width = video_clip_height * 9 / 16

  x1, x2 = (video_clip_width - crop_width) // 2, (video_clip_width + crop_width) // 2
  y1, y2 = 0, video_clip_height

  return crop(video_clip, x1=x1, y1=y1, x2=x2, y2=y2)

def prepare_particle_clip(particle_video_path, frame_size):
  """
  Prepare the particle clip by resizing and cropping.
  """
  particle_clip = VideoFileClip(particle_video_path)
  particle_clip = particle_clip.resize(width=frame_size[0], height=frame_size[1])
  return crop_clip(particle_clip, frame_size)

def create_video(phrases):
  """
  Create a video for each zodiac sign by processing images and audio files, adding captions, and combining clips.
  """
  clear_and_wait()
  video_folder = 'video'
  os.makedirs(video_folder, exist_ok=True)

  audio_folder = 'audio'
  image_folder = 'image'
  particle_video_path = 'video/Particle.mp4'
  background_audio_path = 'audio/BG_music.mp3'

  particle_clip = prepare_particle_clip(particle_video_path, frame_size)
  background_audio = AudioFileClip(background_audio_path).volumex(0.1)

  for sign_name in zodiac_signs:
    video_clips = []

    for i in range(len(phrases[sign_name]['phrases'])):
      image_path = f"{image_folder}/{sign_name}_{i}.jpg"
      audio_path = f"{audio_folder}/{sign_name}_{i}.wav"
      video_clips.append(process_clip(image_path, audio_path, frame_size))
    
    clear_and_wait()
    concatenated_clip = concatenate_videoclips(video_clips)
    concatenated_clip = crop_clip(concatenated_clip, frame_size)

    particle_clip = particle_clip.set_duration(concatenated_clip.duration)
    background_audio = background_audio.set_duration(concatenated_clip.duration)

    final_clip = CompositeVideoClip([concatenated_clip, particle_clip.set_position('center').set_opacity(0.25)])
    final_clip = final_clip.set_audio(CompositeAudioClip([final_clip.audio, background_audio]))

    final_clip.write_videofile(f"{video_folder}/{sign_name}.mp4", codec='libx264', fps=24, threads=4)

  clear_and_wait()

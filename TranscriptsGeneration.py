from moviepy.editor import VideoFileClip
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechRecognizer
from msrest.authentication import CognitiveServicesCredentials
import os

def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)

def extract_frames(video_path, frame_path):
    video = VideoFileClip(video_path)
    frames = video.iter_frames(with_times=True)

    frame.save(f"{frame_path}/frame_{i}.png")

def speech_to_text(audio_path):
    # Replace with your own subscription key and region identifier from Azure.
    speech_key, service_region = "YourSubscriptionKey", "YourServiceRegion"
    speech_config = SpeechConfig(subscription=speech_key, region=service_region)

    audio_input = AudioConfig(filename=audio_path)
    speech_recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    done = False

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    all_results = []
    def handle_final_result(evt):
        all_results.append(evt.result.text)

    speech_recognizer.recognized.connect(handle_final_result)
    
    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    return all_results

def get_face_attributes(frame_path):
    # Set the FACE_SUBSCRIPTION_KEY and FACE_ENDPOINT environment variables with your key and endpoint from Azure.
    FACE_SUBSCRIPTION_KEY = os.environ['FACE_SUBSCRIPTION_KEY']
    FACE_ENDPOINT = os.environ['FACE_ENDPOINT']

    face_client = FaceClient(FACE_ENDPOINT, CognitiveServicesCredentials(FACE_SUBSCRIPTION_KEY))

    # Detect faces with attributes in a frame.
    detected_faces = face_client.face.detect_with_stream(open(frame_path, 'r+b'), return_face_attributes=['emotion'])

    # Extract facial expressions and timestamps.
    facial_expressions = []
    for face in detected_faces:
        facial_expressions.append(face.face_attributes.emotion)

    return facial_expressions

# Usage:
# extract_audio("path_to_your_video.mp4", "output_audio.mp3")
# extract_frames("path_to_your_video.mp4", "output_frames_directory")
# print(speech_to_text("output_audio.mp3"))
# print(get_face_attributes("output_frames_directory/frame_0.png"))

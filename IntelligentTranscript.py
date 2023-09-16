def combine_transcripts(speech_transcript, facial_transcript):
    # Combine the two transcripts into one list and sort by timestamp.
    combined_transcript = sorted(speech_transcript + facial_transcript, key=lambda x: x[1])

    # Initialize an empty string to hold the final transcript.
    final_transcript = ""

    # Iterate over the combined transcript.
    for i in range(len(combined_transcript)):
        # Add the text or facial expression to the final transcript.
        final_transcript += combined_transcript[i][0]

        # If this is not the last item in the transcript, add a time marker.
        if i < len(combined_transcript) - 1:
            final_transcript += f" ({combined_transcript[i][1]} - {combined_transcript[i+1][1]})\n"
        else:
            final_transcript += f" ({combined_transcript[i][1]} - end)\n"

    return final_transcript

# Usage:
# speech_transcript = speech_to_text("output_audio.mp3")
# facial_transcript = get_face_attributes("output_frames_directory/frame_0.png")
# print(combine_transcripts(speech_transcript, facial_transcript))

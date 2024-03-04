from pydub import AudioSegment


def convert_mp3_to_wav(mp3_file_path, wav_file_path):
    # Load the MP3 file
    audio = AudioSegment.from_mp3(mp3_file_path)

    # Export the audio to WAV format
    audio.export(wav_file_path, format="wav")


if __name__ == "__main__":
    # Specify the path to your MP3 file
    # mp3_file_path = "E:\GIS Lec\My Video1.mp3"

    # # Specify the desired path for the output WAV file
    # wav_file_path = "path/to/your/output/file.wav"
    mp3_file_path = "E:\\GIS Lec\\My Video1.mp3"
    wav_file_path = "E:\\GIS Lec\\outputfile.wav"

    # Convert MP3 to WAV
    convert_mp3_to_wav(mp3_file_path, wav_file_path)

    print(f"Conversion complete. WAV file saved at: {wav_file_path}")

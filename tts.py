import azure.cognitiveservices.speech as speechsdk

AZURE_SPEECH_KEY = "3b7a9dcfc7154d589ecd36d4aad7b921"  
AZURE_REGION = "centralindia"       

def azure_text_to_speech(text, output_filename = "output.mp3"):

    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_filename)

    speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"  

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    
    print(f"Speaking: {text}")
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesis completed successfully!")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation.reason}")
        if cancellation.error_details:
            print(f"Error details: {cancellation.error_details}")


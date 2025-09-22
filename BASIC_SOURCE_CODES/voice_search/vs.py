import speech_recognition as sr

def recognize_voice():
	recognizer = sr.Recognizer()
	try:
		with sr.Microphone(device_index=1) as source:
			print("\n🎤 Listening... Speak something...")
			recognizer.adjust_for_ambient_noise(source,duration=0.2)
			audio = recognizer.listen(source)
			text = recognizer.recognize_google(audio)
			print(f"\n🎙️ You said: {text}")
	except sr.UnknownValueError:
		print("❌ Could not understand audio.")
	except sr.RequestError:
		print("❌ Could not request results from Google Speech Recognition.")
if __name__ == "__main__":
    recognize_voice()
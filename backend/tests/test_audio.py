import unittest
import asyncio
from app.services.audio.stt import STTService
from app.services.audio.tts import TTSService

class TestAudioServices(unittest.TestCase):
    def test_stt_transcribe(self):
        service = STTService()
        async def run():
            result = await service.transcribe(b"dummy_data")
            self.assertIn("text", result)
            self.assertIn("confidence", result)
        asyncio.run(run())

    def test_tts_generation(self):
        service = TTSService()
        async def run():
            audio = await service.generate_audio("Hello", speed=0.8)
            self.assertIsInstance(audio, bytes)
        asyncio.run(run())

if __name__ == '__main__':
    unittest.main()

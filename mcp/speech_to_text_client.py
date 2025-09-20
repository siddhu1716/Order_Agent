import httpx
import logging
import os
from typing import Dict, Any, Optional
import tempfile
import json

logger = logging.getLogger(__name__)

class GroqWhisperClient:
    """Client for Groq's Whisper API (speech-to-text)"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY", "mock_key")
        self.base_url = "https://api.groq.com/openai/v1"
        self.whisper_url = f"{self.base_url}/audio/transcriptions"
        
        logger.info("Groq Whisper client initialized")
    
    async def transcribe_audio(self, audio_file_path: str, language: str = "en") -> Dict[str, Any]:
        """Transcribe audio file using Groq's Whisper API"""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                with open(audio_file_path, "rb") as f:
                    files = {
                        "file": (os.path.basename(audio_file_path), f, "audio/wav")
                    }
                    data = {
                        "model": "whisper-large-v3",
                        "language": language,
                        "response_format": "json"
                    }
                    headers = {
                        "Authorization": f"Bearer {self.api_key}"
                    }
                    
                    response = await client.post(
                        self.whisper_url,
                        files=files,
                        data=data,
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        logger.info(f"Successfully transcribed audio: {audio_file_path}")
                        return {
                            "status": "success",
                            "text": result.get("text", ""),
                            "language": result.get("language", language),
                            "duration": result.get("duration", 0)
                        }
                    else:
                        logger.error(f"Transcription failed: {response.status_code} - {response.text}")
                        return {
                            "status": "error",
                            "message": f"Transcription failed: {response.status_code}",
                            "details": response.text
                        }
                        
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            return {
                "status": "error",
                "message": f"Transcription error: {str(e)}"
            }
    
    async def transcribe_audio_bytes(self, audio_bytes: bytes, filename: str = "audio.wav", 
                                   language: str = "en") -> Dict[str, Any]:
        """Transcribe audio from bytes"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(audio_bytes)
                temp_file_path = temp_file.name
            
            # Transcribe the temporary file
            result = await self.transcribe_audio(temp_file_path, language)
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            return result
            
        except Exception as e:
            logger.error(f"Error transcribing audio bytes: {str(e)}")
            return {
                "status": "error",
                "message": f"Transcription error: {str(e)}"
            }
    
    async def transcribe_with_timestamps(self, audio_file_path: str, language: str = "en") -> Dict[str, Any]:
        """Transcribe audio with word-level timestamps"""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                with open(audio_file_path, "rb") as f:
                    files = {
                        "file": (os.path.basename(audio_file_path), f, "audio/wav")
                    }
                    data = {
                        "model": "whisper-large-v3",
                        "language": language,
                        "response_format": "verbose_json",
                        "timestamp_granularities": ["word"]
                    }
                    headers = {
                        "Authorization": f"Bearer {self.api_key}"
                    }
                    
                    response = await client.post(
                        self.whisper_url,
                        files=files,
                        data=data,
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        logger.info(f"Successfully transcribed audio with timestamps: {audio_file_path}")
                        return {
                            "status": "success",
                            "text": result.get("text", ""),
                            "language": result.get("language", language),
                            "duration": result.get("duration", 0),
                            "words": result.get("words", []),
                            "segments": result.get("segments", [])
                        }
                    else:
                        logger.error(f"Transcription with timestamps failed: {response.status_code} - {response.text}")
                        return {
                            "status": "error",
                            "message": f"Transcription failed: {response.status_code}",
                            "details": response.text
                        }
                        
        except Exception as e:
            logger.error(f"Error transcribing audio with timestamps: {str(e)}")
            return {
                "status": "error",
                "message": f"Transcription error: {str(e)}"
            }
    
    async def get_supported_languages(self) -> Dict[str, Any]:
        """Get list of supported languages"""
        # Whisper supports 99 languages
        supported_languages = [
            {"code": "en", "name": "English"},
            {"code": "hi", "name": "Hindi"},
            {"code": "es", "name": "Spanish"},
            {"code": "fr", "name": "French"},
            {"code": "de", "name": "German"},
            {"code": "it", "name": "Italian"},
            {"code": "pt", "name": "Portuguese"},
            {"code": "ru", "name": "Russian"},
            {"code": "ja", "name": "Japanese"},
            {"code": "ko", "name": "Korean"},
            {"code": "zh", "name": "Chinese"},
            {"code": "ar", "name": "Arabic"},
            {"code": "bn", "name": "Bengali"},
            {"code": "te", "name": "Telugu"},
            {"code": "ta", "name": "Tamil"},
            {"code": "mr", "name": "Marathi"},
            {"code": "gu", "name": "Gujarati"},
            {"code": "kn", "name": "Kannada"},
            {"code": "ml", "name": "Malayalam"},
            {"code": "pa", "name": "Punjabi"}
        ]
        
        return {
            "status": "success",
            "languages": supported_languages,
            "total_count": len(supported_languages)
        }
    
    async def validate_audio_format(self, audio_file_path: str) -> Dict[str, Any]:
        """Validate if audio file format is supported"""
        try:
            import wave
            
            with wave.open(audio_file_path, 'rb') as wav_file:
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                frame_rate = wav_file.getframerate()
                frames = wav_file.getnframes()
                duration = frames / frame_rate
                
                # Check if format is supported
                is_supported = (
                    channels in [1, 2] and  # Mono or stereo
                    sample_width in [1, 2, 4] and  # 8-bit, 16-bit, or 32-bit
                    frame_rate >= 8000 and frame_rate <= 48000  # Reasonable sample rate
                )
                
                return {
                    "status": "success",
                    "is_supported": is_supported,
                    "format_info": {
                        "channels": channels,
                        "sample_width": sample_width,
                        "frame_rate": frame_rate,
                        "duration": duration,
                        "file_size": os.path.getsize(audio_file_path)
                    }
                }
                
        except Exception as e:
            logger.error(f"Error validating audio format: {str(e)}")
            return {
                "status": "error",
                "message": f"Audio validation error: {str(e)}"
            } 
import ffmpeg
import os
from pathlib import Path

class VideoService:
    """Video processing using FFmpeg"""
    
    def extract_audio(self, video_path: str, output_path: str) -> str:
        """
        Extract audio from video
        
        Args:
            video_path: Input video file
            output_path: Output audio file (should be .wav or .mp3)
            
        Returns:
            Path to extracted audio
        """
        try:
            print(f"Extracting audio from: {video_path}")
            
            # Extract audio using ffmpeg
            (
                ffmpeg
                .input(video_path)
                .output(output_path, acodec='pcm_s16le', ac=1, ar='16k')  # Mono, 16kHz for Whisper
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            if os.path.exists(output_path):
                print(f"✓ Audio extracted: {output_path}")
                return output_path
            else:
                raise Exception("Audio extraction failed")
                
        except ffmpeg.Error as e:
            print(f"✗ FFmpeg Error: {e.stderr.decode()}")
            raise Exception(f"Audio extraction failed: {e.stderr.decode()}")
    
    def replace_audio(self, video_path: str, audio_path: str, output_path: str) -> str:
        """
        Replace video audio with new audio
        
        Args:
            video_path: Original video file
            audio_path: New audio file
            output_path: Output video file
            
        Returns:
            Path to output video
        """
        try:
            print(f"Replacing audio in video...")
            
            # Get video input
            video_stream = ffmpeg.input(video_path).video
            audio_stream = ffmpeg.input(audio_path).audio
            
            # Combine video and new audio
            (
                ffmpeg
                .output(
                    video_stream, 
                    audio_stream, 
                    output_path,
                    vcodec='copy',  # Copy video without re-encoding
                    acodec='aac',   # Convert audio to AAC
                    strict='experimental'
                )
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            if os.path.exists(output_path):
                print(f"✓ Video created: {output_path}")
                return output_path
            else:
                raise Exception("Video merge failed")
                
        except ffmpeg.Error as e:
            print(f"✗ FFmpeg Error: {e.stderr.decode()}")
            raise Exception(f"Video merge failed: {e.stderr.decode()}")
    
    def get_video_duration(self, video_path: str) -> float:
        """Get video duration in seconds"""
        try:
            probe = ffmpeg.probe(video_path)
            duration = float(probe['streams'][0]['duration'])
            return duration
        except:
            return 0.0
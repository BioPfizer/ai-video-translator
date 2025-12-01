import os
import uuid
import shutil
from pathlib import Path
from typing import Optional
from fastapi import UploadFile

class FileHandler:
    """Handle file uploads and cleanup"""
    
    def __init__(self, upload_dir: str = "/tmp/uploads", output_dir: str = "/tmp/outputs"):
        self.upload_dir = Path(upload_dir)
        self.output_dir = Path(output_dir)
        
        # Create directories if they don't exist
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save_upload(self, file: UploadFile, prefix: str = "video") -> str:
        """
        Save uploaded file with unique name
        
        Args:
            file: Uploaded file from FastAPI
            prefix: Filename prefix
            
        Returns:
            Path to saved file
        """
        # Generate unique filename
        file_ext = Path(file.filename).suffix
        unique_name = f"{prefix}_{uuid.uuid4().hex[:8]}{file_ext}"
        file_path = self.upload_dir / unique_name
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return str(file_path)
    
    def get_output_path(self, prefix: str, extension: str) -> str:
        """Generate output file path"""
        unique_name = f"{prefix}_{uuid.uuid4().hex[:8]}{extension}"
        return str(self.output_dir / unique_name)
    
    def cleanup_file(self, file_path: str):
        """Delete file if exists"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"✓ Cleaned up: {file_path}")
        except Exception as e:
            print(f"✗ Cleanup error: {e}")
    
    def cleanup_files(self, *file_paths):
        """Delete multiple files"""
        for path in file_paths:
            self.cleanup_file(path)


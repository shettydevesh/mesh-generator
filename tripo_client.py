import os
import requests
import asyncio
import time
from tripo3d import TripoClient, TaskStatus
from dotenv import load_dotenv

load_dotenv()

class TripoWrapper:
    def __init__(self):
        self.api_key = os.getenv("TRIPO_API_KEY")
        if not self.api_key:
            raise ValueError("TRIPO_API_KEY not found in environment variables.")
        self.client = TripoClient(api_key=self.api_key)

    async def generate_text_to_model(self, prompt: str, **kwargs):
        """Generates a 3D model from text.
        
        Args:
            prompt: Text description
            **kwargs: Additional parameters like negative_prompt, model_settings, etc.
        """
        print(f"Starting generation for prompt: '{prompt}'")
        if kwargs:
            print(f"Additional params: {kwargs}")
            
        try:
            task = await self.client.text_to_model(prompt=prompt, **kwargs)
            return task
        except Exception as e:
            print(f"Error starting generation: {e}")
            return None

    async def segment_model(self, task_id: str):
        """Segments an existing model task (Manual implementation to bypass SDK bug)."""
        print(f"Starting segmentation for task ID: {task_id}")
        try:
            # Bug in SDK: mesh_segmentation fails to pass required args.
            # We assume v1.0-20250506 as default per SDK source or similar.
            task_data = {
                "type": "mesh_segmentation",
                "original_model_task_id": task_id,
                # "model_version": "v1.0-20250506" # Optional
            }
            # Directly call create_task on the internal client
            # The SDK's create_task returns the task_id string directly
            seg_task_id = await self.client.create_task(task_data)
            return seg_task_id
        except Exception as e:
            print(f"Error starting segmentation: {e}")
            return None

    async def wait_for_task(self, task_id: str, interval: int = 2):
        """Waits for a task to complete."""
        print(f"Waiting for task {task_id}...")
        while True:
            try:
                task = await self.client.get_task(task_id)
                status = task.status
                if status == TaskStatus.SUCCESS:
                    print(f"Task {task_id} completed successfully.")
                    return task
                elif status in [TaskStatus.FAILED, TaskStatus.CANCELLED]:
                    print(f"Task {task_id} failed with status: {status}")
                    return None
                
                print(f"Status: {status}. Waiting...")
                await asyncio.sleep(interval)
            except Exception as e:
                print(f"Error checking status: {e}")
                await asyncio.sleep(interval)

    def download_model(self, url: str, output_path: str):
        """Downloads a model file from a URL. (Sync)"""
        if not url:
            print("No URL provided for download.")
            return False
            
        print(f"Downloading from {url}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Saved to {output_path}")
            return True
        except Exception as e:
            print(f"Download failed: {e}")
            return False

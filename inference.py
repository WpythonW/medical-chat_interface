#!/usr/bin/env python3
"""
Simple inference module for Multimodal Chat using Google's Gemini API
"""

import os
import logging
from PIL import Image
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Environment variables
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
DEFAULT_MODEL = os.environ.get('MODEL_NAME', 'gemini-2.0-flash')
MAX_CONCURRENT = int(os.environ.get('MAX_CONCURRENT', 3))

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

class InferenceService:
    def process_chat(self, message_dict, history, temperature=0.1, top_p=0.95, top_k=40, max_tokens=1000):
        """Process chat message and generate response with configurable parameters"""
        # Extract text and files
        text = message_dict.get("text", "")
        files = message_dict.get("files", [])
        
        # Initialize history if needed
        if not history:
            history = []
        
        # Add user message to history
        if text.strip() or files:
            history.append({"role": "user", "content": text})
        
        # Prepare content for API
        contents = []
        
        # Add text content
        if text.strip():
            contents.append(text)
        
        # Add images
        for file_path in files:
            try:
                img = Image.open(file_path)
                contents.append(img)
            except Exception as e:
                print(f"Error opening image: {e}")
        
        try:
            # Generate response with user-specified parameters
            if contents:
                response = client.models.generate_content(
                    model=DEFAULT_MODEL,
                    contents=contents,
                    config={
                        "temperature": float(temperature),
                        "top_p": float(top_p),
                        "top_k": int(top_k),
                        "max_output_tokens": int(max_tokens)
                    }
                )
                
                response_text = response.text
            else:
                response_text = "No input provided."
                
            # Add assistant response to history
            history.append({"role": "assistant", "content": response_text})
            
        except Exception as e:
            # Handle any API errors
            error_message = f"Error generating response: {str(e)}"
            print(error_message)
            history.append({"role": "assistant", "content": error_message})
        
        return history
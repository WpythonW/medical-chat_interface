#!/usr/bin/env python3
"""
Gradio Interface for Multimodal Chat with Gemini Models
"""

import os
import gradio as gr
from inference import InferenceService, MAX_CONCURRENT, DEFAULT_MODEL

# Initialize inference service
inference_service = InferenceService()

# Create Gradio interface
with gr.Blocks(theme="soft") as demo:
    gr.Markdown("# Multimodal Chat Interface")
    
    chatbot = gr.Chatbot(
        label="Conversation",
        height=500,
        type="messages"  # Fix for the warning
        # Аватарки отключены
    )
    
    with gr.Row():
        textbox = gr.MultimodalTextbox(
            file_types=["image"],
            file_count="multiple",
            placeholder="Type your message here and/or upload images...",
            scale=9
        )
    
    clear_btn = gr.Button("Clear Chat")
    
    submit_event = textbox.submit(
        fn=inference_service.process_chat,
        inputs=[textbox, chatbot],
        outputs=chatbot,
    ).then(
        fn=lambda: {"text": "", "files": []},
        outputs=textbox
    )
    
    clear_btn.click(fn=lambda: [], outputs=chatbot)
    
    # Add examples directly
    gr.Examples(
        examples=[
            [{"text": "What breed is this dog?", "files": ["examples/dog_pic.jpg"]}],
            [{"text": "Analyze this chest X-ray", "files": ["examples/xray.jpg"]}],
            [{"text": "What medical condition is shown here?", "files": ["examples/medical.jpg"]}],
            [{"text": "Describe what you see in this scan", "files": ["examples/scan.jpg"]}],
            [{"text": "Identify the pathology in this image", "files": ["examples/pathology.jpg"]}]
        ],
        inputs=textbox
    )

# Launch the interface
demo.queue(default_concurrency_limit=MAX_CONCURRENT)
demo.launch()
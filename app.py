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
        avatar_images=("👤", "🤖"),
        height=500,
        type="messages"  # Fix for the warning
    )
    
    with gr.Row():
        textbox = gr.MultimodalTextbox(
            file_types=["image"],
            file_count="multiple",
            placeholder="Type your message here and/or upload images...",
            scale=9
        )
        submit_btn = gr.Button("Send", size="sm", scale=1)
    
    clear_btn = gr.Button("Clear Chat")
    
    # Set up event handlers
    submit_click = submit_btn.click(
        fn=inference_service.process_chat,
        inputs=[textbox, chatbot],
        outputs=chatbot,
    ).then(
        fn=lambda: {"text": "", "files": []},
        outputs=textbox
    )
    
    submit_event = textbox.submit(
        fn=inference_service.process_chat,
        inputs=[textbox, chatbot],
        outputs=chatbot,
    ).then(
        fn=lambda: {"text": "", "files": []},
        outputs=textbox
    )
    
    clear_btn.click(fn=lambda: [], outputs=chatbot)
    
    # Add example images if they exist
    examples = []
    example_images = {
        "dog_pic.jpg": "What breed is this?",
        "newspaper.png": "Extract all information from this document."
    }
    
    for img_name, prompt_text in example_images.items():
        img_path = os.path.join(os.path.dirname(__file__), img_name)
        if os.path.exists(img_path):
            examples.append([{"text": prompt_text, "files": [img_path]}])
    
    if examples:
        gr.Examples(examples=examples, inputs=textbox)
    
    # Display model info
    gr.Markdown(f"### Using Gemini model: {DEFAULT_MODEL}")

# Launch the interface
demo.queue(default_concurrency_limit=MAX_CONCURRENT)
demo.launch()
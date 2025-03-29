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
    
    with gr.Accordion("Generation Parameters", open=False):
        with gr.Row():
            with gr.Column():
                temperature = gr.Slider(
                    minimum=0.0, 
                    maximum=1.0, 
                    value=0.1, 
                    step=0.05, 
                    label="Temperature", 
                    info="Higher values make output more random, lower values more deterministic"
                )
                top_p = gr.Slider(
                    minimum=0.0, 
                    maximum=1.0, 
                    value=0.95, 
                    step=0.05, 
                    label="Top-p", 
                    info="Nucleus sampling: consider tokens with top_p probability mass"
                )
            with gr.Column():
                top_k = gr.Slider(
                    minimum=1, 
                    maximum=100, 
                    value=40, 
                    step=1, 
                    label="Top-k", 
                    info="Consider only top k tokens for each generation step"
                )
                max_tokens = gr.Slider(
                    minimum=100, 
                    maximum=2000, 
                    value=1000, 
                    step=100, 
                    label="Max Tokens", 
                    info="Maximum number of tokens to generate"
                )
    
    submit_event = textbox.submit(
        fn=inference_service.process_chat,
        inputs=[textbox, chatbot, temperature, top_p, top_k, max_tokens],
        outputs=chatbot,
    ).then(
        fn=lambda: {"text": "", "files": []},
        outputs=textbox
    )
    
    clear_btn.click(fn=lambda: [], outputs=chatbot)
    
    # Add examples directly
    gr.Examples(
        examples=[
            [{"text": "What type of tissue is shown in the image?", "files": ["images/type_of_tissue.png"]}],
            [{"text": "What type of CT scans are shown in the image?", "files": ["images/CT.png"]}],
            [{"text": "What type of imaging technique is used in this figure?", "files": ["images/brain.png"]}],
            [{"text": "What organ is shown in the image?", "files": ["images/organ.png"]}],
            [{"text": "What is the relationship between the MRI derived α value and the fractional area of fat vacuoles in the histological section?", "files": ["images/histology.png"]}],
            [{"text": "What does the chest X-ray show?", "files": ["images/XRay.png"]}],
            [{"text": "What is the size of the specimen?", "files": ["images/gross.png"]}],
        ],
        inputs=textbox
    )

# Launch the interface
demo.queue(default_concurrency_limit=MAX_CONCURRENT)
demo.launch()
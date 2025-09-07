# # from vertexai import init
# # from vertexai.preview import generative_models

# # Initialize Vertex AI with location and API key
# init(location="us-central1", api_key="AQ.Ab8RN6IiblviLIbXAnWVfIyzX88PB35JV-2b2bMBcxPO68FErw")

# # Load the latest stable generative model
# model = generative_models.TextGenerationModel("gemini-2.5-pro")

# # Generate text
# try:
#     response = model.generate_text(
#         prompt="Write a summary of Zero Trust security.",
#         temperature=0.7, 
#         max_output_tokens=500
#     )
#     print("Generated Text:\n", response.text)
# except Exception as e:
#     print("Error:", e)

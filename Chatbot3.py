from transformers import pipeline

# Use text-generation for conversational tasks
chatbot = pipeline('text-generation', model='microsoft/DialoGPT-medium')

# Now, when you call the chatbot, use it as a text-generation model
response = chatbot(user_input, max_length=1000, num_return_sequences=1)[0]['generated_text']

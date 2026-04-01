import gradio as gr

def chatbot(input_text):
    # text=input_text.lower().strip()
    if input_text.lower() == "bonjour":
        return "bonjour! Comment puis-je vous aider aujourd'hui?"
    elif input_text.lower()=="comment vas tu?":
        return "je vais bien , merci"
    elif input_text.lower()== "Au revoir!":
        return "passe un bonne journée"
    else:
        return "pardon, peux-tu reformuler ta question?"
    
demo=gr.Interface(fn=chatbot,inputs="text", outputs="text", title="Mon premier chatbot" )
demo.launch()
from llama_cpp import Llama
import sys
class Model:

    def __init__(self):
        self.llm = Llama(
            model_path="models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
            n_ctx=4096,        # context window
            n_threads=8,       # adjust to CPU cores
            n_gpu_layers=0,     # >0 if using GPU
            verbose=False,
        )

    def build_prompt(self, user_question, context_chunks = ""):
        context = "\n\n".join(context_chunks)

        prompt = f"""
        [INST]
        You are a helpful assistant that answers questions using the information in the provided context.
        You can be creative but always be factually correct. Don't hallucinate.
        Be humble, welcoming and use humor time to time.

        Behavior rules:
        - Prioritize factual accuracy over humor or personality.
        - Use clear structure when helpful (bullet points, sections, short paragraphs).
        - Do NOT invent information or use outside knowledge.
        - If the answer is not present, reply exactly:
        "I don't know based on the available information."
        - If no context is provided, reply exactly:
        "Please upload documents to get accurate answers."
        - Do not mention phrases like "context provided" or "provided documents".
        - Do not include unrelated facts or commentary.

        Context:
        {context}

        Question:
        {user_question}
        [/INST]

        """
        # prompt = f"""[INST]
        # You are a helpful assistant that answers questions using ONLY the provided context.

        # Rules:
        # - Do not use outside knowledge.
        # - If the answer is not in the context, reply: "I don't know based on the provided information."
        # - Be concise and factual.
        # - Do not mention the context unless the answer is missing.

        # Context:
        # {context}

        # Question:
        # {user_question}
        # [/INST]"""

        return prompt
    
    def ask_model(self, prompt):
        stream = self.llm(
            prompt,
            max_tokens=450,
            temperature=0.2,
            stop=["</s>"],
            stream=True
        )

        response = ""
        sys.stdout.write("\nBot: ")
        sys.stdout.flush()
        for output in stream:
            token = output["choices"][0]["text"]
            sys.stdout.write(token)
            sys.stdout.flush()
            response += token
        sys.stdout.write("\n")
        return response
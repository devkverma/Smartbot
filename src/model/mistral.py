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

    def build_prompt(self, context_chunks, user_question):
        context = "\n\n".join(context_chunks)

        prompt = f"""
        [INST]
            You are a smart, funny, sarcastic, uncanny but a very helpful assistant (Not a machine).
            You believe in facts and figures rather than myths or rumours. I will ask you questions 
            and you need to answer them correctly by looking through the contexts I gave you. Try to
            make the answers readable by using bullet points, sections and sub-sections.

            IMPORTANT: If you don't know any answer and couldn't find it, just diplomatically deny that 
            you are unaware of it instead of giving wrong answers or hallucinating, if question feels 
            out of place or you don't get the context just reply you don't know the answer. Be clear 
            and concise with your answers, avoid being gibberish. 
            Avoid mentioning "context provided", "provided documents".

            Below is the context and question for you.

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
from groq import Groq


class CAAFR_LLM:

    def __init__(self, llm_api_key=None):
        if not llm_api_key:
            raise ValueError("LLM-API-KEY Not Defined !!")
            # TODO: Add this to .env
            # llm_api_key="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"
        self.client = Groq(api_key=llm_api_key)


    def chat_caafr(self, stats, model_name):

        s1 = stats["azon"]
        s2 = stats["fkart"]
        vector = s1 + s2
        stats_content = "Here is the data for the product: On Amazon: Positive = {0}, Neutral = {1}, Negative = {2}. On Flipkart: Positive = {3}, Neutral = {4}, Negative = {5}.".format(*vector)

        completion = self.client.chat.completions.create(
            # TODO: Add this to .env
            model=model_name, # "llama3-groq-70b-8192-tool-use-preview",
            messages = [
                {"role": "system", "content": "You are a helpful assistant that explains product reviews and comparisons in a simple, clear, and non-technical way. Thus making it user friendly."},
                {"role": "user", "content": "We have review sentiment data for a product on Amazon and Flipkart. Can you help us choose which platform I should prefer based on customer reviews stats?"},
                {"role": "user", "content": stats_content},
                {"role": "user", "content": "Instead of just comparing the data, use percentile/relative comparison formulae calculation and compare by showing few stats systematically in step-wise format"},
                {"role": "user", "content": "use relative comparison, taking into account the positive, negative and neutral counts by giving them reasonable weightage."},
                {"role": "user", "content": "do not give me code, give me suggestions with good reasons and tell the customer why they should opt for that e-commerce in a non-technical way"},
                {"role": "user", "content": "finally in the last line just print the name of the preferred e-commerce (amazon/flipkart)"},
            ],
            temperature=0.5,
            max_tokens=1024,
            top_p=0.65,
            stream=True,
            stop=None,
        )

        response = []
        for chunk in completion:
            response.append(chunk.choices[0].delta.content or "")
        answer = "".join(response)

        return answer



if __name__ == "__main__":
    import sys, os
    # Add the parent directory to the Python path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    from EnvMgr import EnvManager

    env_obj = EnvManager(".env")
    llama = CAAFR_LLM(env_obj.get_env_key("LLM_API_KEY"))
    stats = {
        "azon" : [300, 150, 50],
        "fkart": [350, 200, 20]
    }
    res = llama.chat_caafr(stats, env_obj.get_env_key("LLM_MODEL"))
    print("---"*10)
    print(res)
    print("---"*10)

import openai

openai.api_key = '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'


def askOpenAI(promt: str):
    thePrompt = promt + '{}'
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=thePrompt,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["{}"],
    )
    return response

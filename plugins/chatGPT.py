# -*- coding: utf-8 -*-
import openai

# Set the API key for the openai module
openai.api_key = "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"
def GPT(stra):
    # Use the GPT-3 model to generate text
    print('已接受问题'+stra)
    prompt = stra
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        temperature=0.5,
    )

    # Print the generated text
    print(response["choices"][0]["text"])
    str1 = str(response["choices"][0]["text"])

    print('即将返回'+str1)
    return str1

if __name__ == '__main__':
    GPT('Alan Watts是谁')

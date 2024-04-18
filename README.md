# GPT-4 Wrapper

This repository contains a Python wrapper for GPT-4, providing an easy-to-use interface for the GPT 4 model on discord on a pay as you go basis compared to the subscription model.

## Description

The GPT-4 Wrapper in this repo simplifies the process of deploying and using the GPT-4 model. The wrapper handles the API calls and data processing, and returns the model's output in an easy-to-use format.

## Installation

1. Clone this repository
2. Set up your credentials in the `credentials.py` file. You will need your OpenAI API key and Discord secret keys.

## Use

1. Use the `/prompt` command in Discord.
2. Pass your prompt to the wrapper's `prompt` parameter.
3. It'll create a thread which will maintain context
4. The bot will return the generated text.

## Pricing

The usage of GPT-4 is subject to OpenAI's pricing. You can check [OpenAI's pricing page](https://openai.com/pricing) for more information.

## Contributions

Contributions are welcome! Feel free to submit pull requests or open issues if you have any suggestions or improvements.

## TODO

- [ ] Add a check for user/system message before giving a response. Relevant discussion is available [here](https://cdn.discordapp.com/attachments/1225906013723557989/1230631313514692628/image.png?ex=663405b9&is=662190b9&hm=118e811aff96bfbf36ad473920ea725fd02d540cfebe80185fd4f7bae65988f4&)

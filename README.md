# langchain-experiments

## Summary

Do you want to be able to summarize any PDF? 
Even by selecting exactly which pages you want?
With this small script, you will be able to do it.

You only need to follow these steps:

1. Create an .env file and add your OPENAI_API_KEY={} 
2. Set your Open AI Usage limits to a reasonable limit that you can afford, more info in FAQ
1. poetry install
2. poetry shell
3. python summary/summarize.py


### FAQS

1. Does this cost any money?
    - Yes, it would depend on how long your PDF is and how many tokens you use.
    - By default, this app uses the GPT-3.5 Turbo model. As of today (25-04-23), it costs 0.002 USD per 1k tokens.
    - To set your Usage limits you can go to: https://platform.openai.com/account/billing/limits
        - More information about pricing in: https://openai.com/pricing 
2. Where do I get my OPENAI_API_KEY:
    - Create an account in open ai and then go to your account -> manage account -> [Api Keys](https://platform.openai.com/account/api-keys)
3. I do not have poetry:
    - Install: https://python-poetry.org/docs/

### Disclaimer
Disclaimer This project, is an experimental software and is provided "as-is" without any warranty, express or implied. By using this software, you agree to assume all risks associated with its use, including but not limited to data loss, system failure, or any other issues that may arise.

The developers and contributors of this project do not accept any responsibility or liability for any losses, damages, or other consequences that may occur as a result of using this software. You are solely responsible for any decisions and actions taken based on the information provided by this experiment.

Please note that the use of the models in this case (chat-gpt-3.5-turbo) language model can be expensive due to its token usage. By utilizing this project, you acknowledge that you are responsible for monitoring and managing your own token usage and the associated costs. It is highly recommended to check your OpenAI API usage regularly and set up any necessary limits or alerts to prevent unexpected charges.

By using this software, you agree to indemnify, defend, and hold harmless the developers, contributors, and any affiliated parties from and against any and all claims, damages, losses, liabilities, costs, and expenses (including reasonable attorneys' fees) arising from your use of this software or your violation of these terms.





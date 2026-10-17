"""AI features for sales_toolkit (Part D of the lab).

Modules in this package:

    llm_client.py    Talks to a large language model (LLM) over HTTP.
                     Supports Google Gemini (free tier), Anthropic Claude
                     (paid), and two offline clients used for testing.
    catalogue.py     Loads the product catalogue (the list of things the
                     shop sells, with their prices).
    order_parser.py  Turns a customer's free-text order message into a
                     structured order. YOU build this in Step 21.
"""

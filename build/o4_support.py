# if LARGE_LANGUAGE_MODEL == 'o4-mini':
#         prompt['max_completion_tokens'] = PRODUCT_GENERATION_MAX_TOKENS
#     elif LARGE_LANGUAGE_MODEL == 'gtp-4o-mini':
#         prompt['max_tokens'] = PRODUCT_GENERATION_MAX_TOKENS * 4
#         prompt['temperature'] = PRODUCT_GENERATION_TEMPERATURE

# if LARGE_LANGUAGE_MODEL == 'gpt-4o-mini':
#     AZURE_LLM_URL = os.getenv('AZURE_GPT_4o_URL')
# elif LARGE_LANGUAGE_MODEL == 'o4-mini':
#     AZURE_LLM_URL = os.getenv('AZURE_o4_URL')
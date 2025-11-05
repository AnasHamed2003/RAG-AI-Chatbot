from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline

print("Testing GPT-Neo 125M model loading...")

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print("Embeddings loaded successfully")

# Initialize GPT-Neo 125M model
model_name = "EleutherAI/gpt-neo-125m"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Create text generation pipeline
text_generation_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=50,
    temperature=0.7,
    do_sample=True,
    pad_token_id=tokenizer.eos_token_id
)

# Create LangChain LLM wrapper
llm = HuggingFacePipeline(pipeline=text_generation_pipeline)
print("GPT-Neo model loaded successfully")

# Test a simple generation
result = llm.invoke("Hello, how are you?")
print(f"Test generation: {result}")
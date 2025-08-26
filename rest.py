# packages

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from pred_conv import predict_conversation

# Create the app
app = FastAPI()

# Creaate a pydantic model
class Prompt(BaseModel):
    prompt: str
    number_of_turns: int
    style_a: str
    style_b: str

# define the endpoint "debate"
@app.post("/debate")
def debate_endpoint(parameters: Prompt):
    prompt = parameters.prompt
    turns  = parameters.number_of_turns
    style_a = parameters.style_a
    style_b = parameters.style_b

    result = predict_conversation(user_prompt=prompt, number_of_turns=turns, style_a=style_a, style_b=style_b)
    return result

if __name__ == '__main__':
    uvicorn.run("rest:app", reload=True)


# to run in terminal, use python ./rest.py
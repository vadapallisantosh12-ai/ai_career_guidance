from cog import BasePredictor, Input 
 
class Predictor(BasePredictor): 
    def predict(self, question: str = Input(description="Career question")) -> str: 
        return f"Career Guidance for: {question}"

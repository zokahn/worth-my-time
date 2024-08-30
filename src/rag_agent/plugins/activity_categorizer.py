from src.rag_agent.plugins.base_plugin import BasePlugin
from src.rag_agent.utils.nlp import categorize_text

class ActivityCategorizerPlugin(BasePlugin):
    def initialize(self):
        pass

    def execute(self, window_title, categories):
        return categorize_text(window_title, categories)

    def cleanup(self):
        pass

def register_plugin():
    return ActivityCategorizerPlugin()

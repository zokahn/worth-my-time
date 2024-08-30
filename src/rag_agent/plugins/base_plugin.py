from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @abstractmethod
    def initialize(self):
        """Initialize the plugin"""
        pass

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Execute the main functionality of the plugin"""
        pass

    @abstractmethod
    def cleanup(self):
        """Cleanup any resources used by the plugin"""
        pass

def register_plugin():
    """Register the plugin class"""
    return BasePlugin
import importlib
import os

class PluginManager:
    def __init__(self):
        self.plugins = {}

    def load_plugins(self):
        plugin_dir = os.path.dirname(__file__)
        for filename in os.listdir(plugin_dir):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = f'src.rag_agent.plugins.{filename[:-3]}'
                module = importlib.import_module(module_name)
                if hasattr(module, 'register_plugin'):
                    plugin = module.register_plugin()
                    self.plugins[filename[:-3]] = plugin()

    def get_plugin(self, name):
        return self.plugins.get(name)

plugin_manager = PluginManager()

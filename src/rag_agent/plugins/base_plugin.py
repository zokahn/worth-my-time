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

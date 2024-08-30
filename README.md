# RAG Agent Development

## Current State of Things

- The RAG agent is up and running.
- The activity monitor script has been integrated into the main script.
- The activity monitor script is now tracking the active window title and categorizing activities.
- The activity monitor script is now associating activities with specific projects.
- The project structure has been updated to reflect the new plan.
- The high-level design, goals, and project structure documents have been updated with the new plan.
- The status has been updated.

## Goals

- Implement a cutting-edge Retrieval-Augmented Generation (RAG) agent.
- Track the activity of the workstation.
- Generate daily and weekly reports based on the tracked activities.
- Implement a modular architecture allowing for easy swapping of vector databases, embedding models, and language models.
- Use FAISS or Annoy for efficient similarity search.
- Implement data preprocessing pipeline with text cleaning, tokenization, and chunking.
- Use a lightweight local language model like GPT4All or LLaMA for the generation part.
- Implement a caching mechanism for generated responses to improve performance.
- Implement a feedback loop for self-analysis and improvement.
- Use the `evolution/` directory to store historical versions of key components.
- Implement `project_assistant.py` to analyze status files and provide insights.
- Collect metrics in the `metrics/` directory.
- Implement `visualize.py` to generate visual representations of project progress and health.
- Create an interactive dashboard (`dashboard.html`) using D3.js.
- Implement `code_reviewer.py` to perform AI-assisted code reviews and integrate it into the CI/CD pipeline.
- Design and implement a plugin system in the `plugins/` directory.
- Implement `nl_config.py` for natural language-based configuration of the RAG agent.

## Decisions Log

- Decided to implement the RAG agent in Python.
- Decided to use the subprocess module to start the activity monitor script in the background.

## Open Questions

- What is the best way to categorize activities as private or business-related?
- What is the best way to associate activities with specific projects?

## High-Level Design

[High-Level Design](status/hld.txt)

## Project Structure

[Project Structure](status/project_structure.txt)

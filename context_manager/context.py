def load_context(question):
    # Dummy context loader
    if "weather" in question:
        return {"status": "FOUND", "context": "Today's weather is sunny."}
    return {"status": "NOT_FOUND"}

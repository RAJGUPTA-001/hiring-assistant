
raw="""```json
[
  {
    "technology": "Python",
    "questions": [
      "Explain the difference between shallow and deep copies in Python, and provide code examples demonstrating when each should be used.",
      "Describe how the Global Interpreter Lock (GIL) affects multi-threaded performance in CPython and discuss alternative strategies to achieve concurrency.",
      "What are descriptor objects in Python? Explain how `__get__`, `__set__`, and `__delete__` methods work together, and give a practical use case.",
      "How does Python's `asyncio` event loop work? Compare `asyncio` coroutines with traditional threading and explain how to handle blocking I/O within an async context."
    ]
  }
]
```"""
import json
arr = json.loads(raw)
print(arr)
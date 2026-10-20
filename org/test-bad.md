# Test — bad content

This file contains a secret that should be caught:

api_key: sk_live_ABCDEFGHIJKLMNOP1234

And a code block that should fail:

```python
def hello():
    print("this is code, not knowledge")
```

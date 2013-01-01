
Retrieves full text from the current view:

```python
    import sublime
    
    def text_from(view):
      return view.substr(sublime.Region(0, min(view.size(), 2**14)))
```

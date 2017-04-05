## 0.0.3
* Plugins and libs have to use relative imports

* example:

    ```python
    from ..libs.screen import Screen
    from ..libs.text import Text

    class Plugin():
        def __init__(self, matrix=True, show=False, guishow=False):
            super(Plugin, self).__init__()
            self.name = "Example Plugin"
            self.version = "0.0.3"

            self.sample_text = Text('sample text')

            self.screen = Screen(matrix=matrix, show=show)
            self.screen.add(self.sample_text, refresh=False)

        def start(self):
            self.screen.refresh()
    ```

## 0.0.2
* The Plugin class is now required to launch the plugin

* example:

    ```python
    from libs.screen import Screen

    class Plugin():
        def __init__(self, matrix=True, show=False, guishow=False):
            super(Plugin, self).__init__()
            self.name = "Example Plugin"
            self.version = "0.0.2"
            self.screen = Screen(matrix=matrix, show=show)

        def start(self):
            self.screen.refresh()
    ```

## 0.0.1
* plugins are now in the *plugins* folder.
* each updated plugin must have a __self.version__ attribute set to the last version value.
* remove the standalone code of the plugin as it has to be launched from glm.py

* example:

    ```python
    from libs.screen import Screen

    class Plugin():
        def __init__(self, matrix=True, show=False, guishow=False):
            super(Plugin, self).__init__()
            self.version = "0.0.1"
            self.screen = Screen(matrix=matrix, show=show)

        def start(self):
            self.screen.refresh()
    ```

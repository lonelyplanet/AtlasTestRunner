## AtlasTestRunner

A plugin for Sublime Text 2 that executes three kinds of test:

* RSpec
* Cucumber
* Coffeescript Jasmine

Results are formatted and presented in a webbrowser.

Although written to support the LP SPP project, it should be configurable for others. Have a look at AtlasTestRunner.sublime-settings:
```
    jasmine_coffee_url:   A URL for your jasmine runner.

    jasmine_coffee_regex: These regexes match a path to your tests,
    cucumber_regex:       typically a path relative to the root of your project.
    rspec_regex:
```

To install (OS X or Linux), clone this repo into your Sublime Text 2 `Packages` directory:
```
    git clone https://github.com/lonelyplanet/AtlasTestRunner.git
```

* Run All Tests (OS X: `⌘-⌥-T`, Linux: `Ctrl-Alt-T`)
  Execute all tests in the current file.

* Run Single Test (OS X: `⌘-⌥-Shift-T`, Linux: `Ctrl-Alt-Shift-T`)
  Execute the test determined by the cursor.

## AtlasTestRunner

A test-runner plugin for Sublime Text 2 and Sublime Text 3.
The following test types are supported:

* RSpec
* Cucumber
* Coffeescript Jasmine

Results are formatted and presented in a browser.

Although written to support the LP SPP project, this should be configurable for other projects. Have a look at AtlasTestRunner.sublime-settings:
```
    jasmine_coffee_url:      A URL for your jasmine runner.

    jasmine_coffee_regex:    These regexes match a path to your tests,
    cucumber_regex:          typically a path relative to 
    rspec_regex:             the root of your project.
```

To install (OS X or Linux), clone this repo into your Sublime Text 2 `Packages` directory:
```
    git clone https://github.com/lonelyplanet/AtlasTestRunner.git
```

* Run All Tests (OS X: `⌘-⌥-T`, Linux: `Ctrl-Alt-T`)
  Execute all tests in the current file.

* Run Single Test (OS X: `⌘-⌥-Shift-T`, Linux: `Ctrl-Alt-Shift-T`)
  Execute the test determined by the cursor.

# UniUnitTests
Unit test code for CSCI-140/141. Java and Python.

# Python usage:
```py
def test(testFunc: Any, inputdir: str = '../input', outputdir: str = '../output', verbose: bool = False) -> int:
```
1. Import `tests` into your project:
>`from tests import test`
2. In your main guard, comment out the main function call, and replace it with the test function call.
Example:
```py
if __name__ == '__main__':
    #main()
    test(main, '../input', '../output')
```
## Note: 
* If all tests pass, the function returns 1, if not it returns 0
* `verbose` mode is not implemented
* Do *NOT* include parentheses when passing your main function into `test()`. If your main function requires arguments, testing will not work as expected

# Ethereum Contract Testing #

Testing framework for Ethereum contracts with examples that uses
`pyethereum`. Contains the class `TestContract` which is a subclass of
`unittest.TestCase`. The `TestContract` class contains a `setUp()`
function to create a fixture that creates the contracts whose
filenames are passed in.

See examples in the `tests` directory for usage. Only contracts
written in Serpent are supported at this time.

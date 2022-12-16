# format: <relative/path/to/solidity/file>:<contrac_name> --verify <contract_name>:<relative/path/to/spec/file>

SOLC_VERSION=0.7.0 certoraRun Bank.sol \
--verify Bank:Parametric.spec \
--rule validityOfTotalFunds \
--msg "$1"

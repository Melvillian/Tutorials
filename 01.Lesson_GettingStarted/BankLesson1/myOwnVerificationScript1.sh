# format: <relative/path/to/solidity/file>:<contrac_name> --verify <contract_name>:<relative/path/to/spec/file>

SOLC_VERSION=0.7.5 certoraRun Bank.sol \
--verify Bank:TotalGreaterThanUser.spec \
--msg "My first Certora shell script"
SOLC_VERSION=0.8.6 certoraRun ManagerBug1.sol:Manager --verify Manager:ManagerPartialSolution.spec \
--send_only \
--msg "$1"
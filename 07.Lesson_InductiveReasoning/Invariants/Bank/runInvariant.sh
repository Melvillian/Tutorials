SOLC_VERSION=0.7.6 certoraRun BankFixed.sol:Bank --verify Bank:invariant.spec \
--msg "$1"
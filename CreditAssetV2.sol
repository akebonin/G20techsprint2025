// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CreditAssetV2 {
    address public lender;
    address public borrower;
    uint256 public yieldThreshold;
    uint256 public totalFunded;
    uint256 public constant RELEASE_AMOUNT = 0.001 ether;
    uint256 public borrowerRegistrationTime; // Tracks registration time
    uint256 public constant TIMEOUT = 5 minutes; // 300 seconds

    event Funded(address indexed lender, uint256 amount);
    event FundsReleased(address indexed borrower, uint256 amount);
    event BorrowerRegistered(address indexed borrower);
    event BorrowerReset(address indexed oldBorrower, address indexed resetBy); // New event

    constructor(uint256 _yieldThreshold) payable {
        yieldThreshold = _yieldThreshold;
        lender = msg.sender;
        if (msg.value > 0) {
            totalFunded = msg.value;
            emit Funded(msg.sender, msg.value);
        }
    }

    modifier onlyBorrower() {
        require(msg.sender == borrower, "Not the registered borrower.");
        _;
    }

    function fundLoan() external payable {
        require(msg.value > 0, "Must send ETH to fund the loan");
        totalFunded += msg.value;
        lender = msg.sender;
        emit Funded(msg.sender, msg.value);
    }

    function registerAsBorrower() public {
        require(borrower == address(0), "A borrower is already active.");
        borrower = msg.sender;
        borrowerRegistrationTime = block.timestamp; // Start timeout
        emit BorrowerRegistered(msg.sender);
    }

    function releaseFunds(uint256 actualYield) public onlyBorrower {
        require(actualYield >= yieldThreshold, "Yield below required threshold.");
        require(totalFunded >= RELEASE_AMOUNT, "Insufficient contract balance.");
        require(address(this).balance >= RELEASE_AMOUNT, "Contract balance too low.");
        totalFunded -= RELEASE_AMOUNT;
        payable(borrower).transfer(RELEASE_AMOUNT);
        emit FundsReleased(borrower, RELEASE_AMOUNT);
        borrower = address(0); // Reset borrower
        borrowerRegistrationTime = 0; // Clear timeout
    }

    function resetBorrower() public {
        require(borrower != address(0), "No borrower to reset.");
        require(block.timestamp >= borrowerRegistrationTime + TIMEOUT, "Timeout not reached.");
        address oldBorrower = borrower;
        borrower = address(0);
        borrowerRegistrationTime = 0;
        emit BorrowerReset(oldBorrower, msg.sender);
    }

    function getStatus() public view returns (string memory) {
        if (borrower == address(0)) {
            return "Awaiting borrower registration";
        } else if (block.timestamp >= borrowerRegistrationTime + TIMEOUT) {
            return "Borrower timed out, can be reset";
        } else {
            return "Borrower registered, awaiting yield trigger";
        }
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    function getRemainingFunds() public view returns (uint256) {
        return totalFunded;
    }

    receive() external payable {
        totalFunded += msg.value;
        lender = msg.sender;
        emit Funded(msg.sender, msg.value);
    }
}

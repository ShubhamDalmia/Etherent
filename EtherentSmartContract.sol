// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

contract PropertyRent {
    address owner;

    constructor(){
        owner = msg.sender;
    }
    // Add Owner

    struct Owner{
        address payable walletAddress;
        string firstName;
        string lastName; 
        string phoneNumber;
        uint balance;
    }

    mapping(address => Owner) public owners;

    function addOwner(address payable walletAddress, string memory firstName, string memory lastName, string memory phoneNumber) public {
        uint balance = 0;
        owners[walletAddress] = Owner(walletAddress, firstName, lastName, phoneNumber, balance);
    }

    // Add Property
    struct Property{
        address payable walletAddress;
        uint propertyId;
        bool isCurrentlyRented;
        uint rent;
    }

    mapping(uint => Property) public properties;

    function addProperty(address payable walletAddress, uint propertyId,uint rent) public {
        bool isCurrentlyRented = false;
        properties[propertyId] = Property(walletAddress, propertyId,isCurrentlyRented,rent);
        ownerOfProperty[walletAddress].push(propertyId);
    }

    // Mapping to get list of propertyId's owned by an owner
    mapping(address => uint[]) public ownerOfProperty;

    //Add Tenant

     struct Tenant{
        address payable walletAddress;
        string firstName;
        string lastName; 
        string phoneNumber;
        uint rating;
        uint rentalPoints;
        bool canRent;
        uint lastRentPaid;
        uint dueAmount;
     }
     
     mapping(address => Tenant) public tenants;

    function addTenant(address payable walletAddress, string memory firstName, string memory lastName, string memory phoneNumber) public {
        uint rating = 0;
        uint rentalPoints = 0;
        bool canRent = true;
        uint lastRentPaid = 0;
        uint dueAmount = 0;
        tenants[walletAddress] = Tenant(walletAddress, firstName, lastName, phoneNumber, rating, rentalPoints ,canRent, lastRentPaid, dueAmount);
    }

    // Mapping to get the tenant of a property
    mapping(uint => address) propertyTenant;

    // Add Agreement
    struct PropertyAgreement{
        uint propertyId;
        uint start;
        uint end;
        address payable tenantAddress;
        address payable ownerAddress;
    }

    mapping(uint => PropertyAgreement)  public propertyAgreementByPropertyId;

    // Sign Agreement
    
    function signAgreement(uint propertyId, uint start, uint end, address payable ownerWalletAddress, address payable tenantWalletAddress) public{
        // require(owners[walletAddress].due == 0, 'You have pending balance.');
        // require(owners[walletAddress].canRent == true, 'You cannot rent.');
        propertyAgreementByPropertyId[propertyId] = PropertyAgreement(propertyId,start, end, ownerWalletAddress, tenantWalletAddress);
        tenants[tenantWalletAddress].canRent = false;
        tenants[tenantWalletAddress].lastRentPaid = block.timestamp;
        tenants[tenantWalletAddress].dueAmount = 0;
    }

    // End Agreement
    
    function endAgreement(uint propertyId, address payable tenantWalletAddress, uint cleanlinessRating, uint neighbourRating) public{
        // require(owners[walletAddress].due == 0, 'You have pending balance.');
        // require(owners[walletAddress].canRent == true, 'You cannot rent.');
        uint userRating = calculateRating(tenantWalletAddress, propertyId, cleanlinessRating, neighbourRating);
        tenants[tenantWalletAddress].rating = userRating;
        tenants[tenantWalletAddress].canRent = true;
        tenants[tenantWalletAddress].lastRentPaid = 0;
        tenants[tenantWalletAddress].dueAmount = 0;
        delete propertyAgreementByPropertyId[propertyId];
    }

    function calculateRating(address payable tenantWalletAddress,uint propertyId,uint cleanlinessRating ,uint neighbourRating) internal view returns(uint){
        uint cleanlinessPoints = 0;
        if(cleanlinessRating == 5)
            cleanlinessPoints = 15;
        else if(cleanlinessRating == 4)
            cleanlinessPoints = 12;
        else if(cleanlinessRating == 3)
            cleanlinessPoints = 9;
        else if(cleanlinessRating == 2)
            cleanlinessPoints = 6;
        else
            cleanlinessPoints = 3;

        uint neighbourPoints = 0;
        if(neighbourRating == 5)
            neighbourPoints = 15;
        else if(neighbourRating == 4)
            neighbourPoints = 12;
        else if(neighbourRating == 3)
            neighbourPoints = 9;
        else if(neighbourRating == 2)
            neighbourPoints = 6;
        else
            neighbourPoints = 3;

        
        uint rentalPoints = tenants[tenantWalletAddress].rentalPoints;
        uint agreementTerminationPoints = 0;
        uint validAgreementEnd = propertyAgreementByPropertyId[propertyId].end / 60; //In minutes
        uint agreementTerminationDate = block.timestamp / 60; //In minutes

        if(agreementTerminationDate > validAgreementEnd )
            agreementTerminationPoints = 30;
        else if (validAgreementEnd - agreementTerminationDate <= 2 && validAgreementEnd - agreementTerminationDate >= 1 )
            agreementTerminationPoints = 24;
        else if (validAgreementEnd - agreementTerminationDate == 3 )
            agreementTerminationPoints = 18;
        else if (validAgreementEnd - agreementTerminationDate <= 6 && validAgreementEnd - agreementTerminationDate >= 4 )
            agreementTerminationPoints = 12;
        else if (validAgreementEnd - agreementTerminationDate > 6)
            agreementTerminationPoints = 6;
        

        return cleanlinessRating + neighbourPoints + rentalPoints + agreementTerminationPoints;
    }

    function setRentalPoints(address tenantWalletAddress) internal {
        uint currentDate = block.timestamp;
        uint lastRentPaidDate = tenants[tenantWalletAddress].lastRentPaid;
        uint validDateForRentPayment = lastRentPaidDate + 2592000;
        uint delay = (currentDate - validDateForRentPayment) / 60;
        uint rentalPoints = 0;
        if(delay <= 0)
            rentalPoints = 40;
        else if(delay <= 1 && delay >= 3)
            rentalPoints = 35;
        else if(delay <= 7 && delay >= 4)
            rentalPoints = 30;
        else if(delay <= 14 && delay >= 8)
            rentalPoints = 20;
        else if(delay > 15)
            rentalPoints = 10;
        else
            rentalPoints = 5;

        tenants[tenantWalletAddress].rentalPoints = rentalPoints;
        tenants[tenantWalletAddress].lastRentPaid = validDateForRentPayment;
        tenants[tenantWalletAddress].dueAmount = 0;
    }

    // Make Payment
    function makePayment(address tenantWalletAddress, address ownerWalletAddress) public payable{
        setRentalPoints(tenantWalletAddress);
        owners[ownerWalletAddress].balance  +=  100;
    }
}
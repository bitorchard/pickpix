// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract TestemNFT is Ownable, ERC721 {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    uint256 public constant _maxSupply = 100000;
    uint8 public constant _maxMint = 100;
    uint256 public constant _tokenPrice = 0.1*(10**18);

    constructor() ERC721("TestemNFT", "TESTEM") {}

    //mapping(address=>tokenMetaData[]) public ownershipRecord;

    /*struct tokenMetaData {
        uint tokenId;
        uint timeStamp;
        string tokenURI;
    }*/

    function mintToken(address recipient)
        onlyOwner
        public
        returns (uint256)
    {
        //require(owner() != recipient, “Recipient cannot be the owner of the contract”);
        _tokenIds.increment();
        uint256 thisTokenId = _tokenIds.current();

        _mint(recipient, thisTokenId);
        return thisTokenId;
    }

    function mintTokens(uint8 numTokens)
        public
        payable
        returns (uint256[] memory)
    {
        require(numTokens <= _maxMint, "Exceeds mint limit");
        require(totalSupply() + numTokens <= _maxSupply, "Exceeds maximum supply");
        require(msg.value >= _tokenPrice * numTokens, "Not enough AVAX sent, check price");

        uint256[] memory tokenIds;
        for (uint256 i = 0; i < numTokens; i++) {
            _tokenIds.increment();
            uint256 thisTokenId = _tokenIds.current();
            _safeMint(msg.sender, thisTokenId);
            tokenIds[i] = thisTokenId;
        }
        return tokenIds;
    }

    function totalSupply()
        public
        view
        returns (uint256)
    {
        return _tokenIds.current();
    }

    function getCurrentPrice()
        public
        pure
        returns (uint256)
    {
        return _tokenPrice;
    }

    function magicNumber()
        public
        pure
        returns (uint256)
    {
        return uint256(666);
    }

    function decimals()
        public
        pure
        returns (uint8)
    {
        return uint8(0);
    }
}

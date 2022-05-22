//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;
pragma abicoder v2; // required to accept structs as function parameters

import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import "@openzeppelin/contracts/utils/cryptography/draft-EIP712.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/contracts/utils/math/SafeCast.sol";

contract Pixel is ERC721URIStorage, EIP712, AccessControl {
    uint24 lastPixel = 0;
    uint24 aBigPrime = 500000; // some big prime > 500000
    uint24 lcgCValue = 6666;
    using Counters for Counters.Counter;
    using SafeCast for uint256;
    Counters.Counter private _tokenIds;
    uint256 public constant _maxSupply = 100000;
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    string private constant SIGNING_DOMAIN = "Pixel-Voucher";
    string private constant SIGNATURE_VERSION = "1";

    mapping (address => uint256) pendingWithdrawals;
    mapping (uint32 => uint24) tokenIdToPixelId;

    constructor(address payable minter)
        ERC721("PixelNFT", "PXL")
        EIP712(SIGNING_DOMAIN, SIGNATURE_VERSION)
    {
        _setupRole(MINTER_ROLE, minter);
    }

    struct NFTVoucher {
        uint256 minPrice;
        string uri;
        bytes signature;
    }

    function decimals()
        public
        pure
        returns (uint8)
    {
        return uint8(0);
    }

    function totalSupply()
        public
        view
        returns (uint256)
    {
        return _tokenIds.current(); 
    }

    function getPixelIdFromTokenId(uint32 tokenId)
        public
        view
        returns (uint24)
    {
        return tokenIdToPixelId[tokenId]; 
    }

    function lastToken()
        public
        view
        returns (uint256)
    {
        return _tokenIds.current();
    }

    function _allocateFreePixel()
        internal
        returns (uint24)
    {
        uint24 freePixel = (lastPixel + lcgCValue) % aBigPrime;
        if (freePixel >= _maxSupply) {
            freePixel = (freePixel + lcgCValue) % aBigPrime;
        }
        lastPixel = freePixel;
        return freePixel;
    }

    /// @notice Redeems an NFTVoucher for an actual NFT, creating it in the process.
    /// @param redeemer The address of the account which will receive the NFT upon success.
    /// @param voucher A signed NFTVoucher that describes the NFT to be redeemed.
    function redeem(address redeemer, NFTVoucher calldata voucher)
        public
        payable
        returns (uint32)
    {
        address signer = _verify(voucher);

        require(hasRole(MINTER_ROLE, signer), "Shenanigans");
        require(msg.value >= voucher.minPrice, "Insufficient funds to redeem");
        require(totalSupply() <= _maxSupply, "Exceeds supply limit");

        _tokenIds.increment();
        uint32 mintedTokenId = _tokenIds.current().toUint32();
        uint24 mintedPixelId = _allocateFreePixel();

        // first assign the token to the signer, to establish provenance on-chain
        _mint(signer, mintedTokenId);
        _setTokenURI(mintedTokenId, voucher.uri);
        
        // transfer the token to the redeemer
        _transfer(signer, redeemer, mintedTokenId);

        // record payment to signer's withdrawal balance
        pendingWithdrawals[signer] += msg.value;
        tokenIdToPixelId[mintedTokenId] = mintedPixelId;

        return mintedTokenId;
    }

    /// @notice Transfers all pending withdrawal balance to the caller. Reverts if the caller is not an authorized minter.
    function withdraw()
        public
    {
        require(hasRole(MINTER_ROLE, msg.sender), "Only authorized minters can withdraw");
        
        // IMPORTANT: casting msg.sender to a payable address is only safe if ALL members of the minter role are payable addresses.
        address payable receiver = payable(msg.sender);

        uint amount = pendingWithdrawals[receiver];
        // zero account before transfer to prevent re-entrancy attack
        pendingWithdrawals[receiver] = 0;
        receiver.transfer(amount);
    }

    /// @notice Retuns the amount of Ether available to the caller to withdraw.
    function availableToWithdraw()
        public
        view
        returns (uint256)
    {
        return pendingWithdrawals[msg.sender];
    }

    /// @notice Returns a hash of the given NFTVoucher, prepared using EIP712 typed data hashing rules.
    /// @param voucher An NFTVoucher to hash.
    function _hash(NFTVoucher calldata voucher)
        internal
        view
        returns (bytes32)
    {
        return _hashTypedDataV4(keccak256(abi.encode(
            keccak256("NFTVoucher(uint256 minPrice,string uri)"),
            voucher.minPrice,
            keccak256(bytes(voucher.uri))
        )));
    }

    function getChainID()
        external
        view
        returns (uint256)
    {
        uint256 id;
        assembly {
            id := chainid()
        }
        return id;
    }

    /// @notice Verifies the signature for a given NFTVoucher, returning the address of the signer.
    /// @dev Will revert if the signature is invalid. Does not verify that the signer is authorized to mint NFTs.
    /// @param voucher An NFTVoucher describing an unminted NFT.
    function _verify(NFTVoucher calldata voucher)
        public
        view
        returns (address)
    {
        bytes32 digest = _hash(voucher);
        return ECDSA.recover(digest, voucher.signature);
    }

    function supportsInterface(bytes4 interfaceId) public view virtual override (AccessControl, ERC721) returns (bool) {
        return ERC721.supportsInterface(interfaceId) || AccessControl.supportsInterface(interfaceId);
    }
}

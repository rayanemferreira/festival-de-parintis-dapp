// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "hardhat/console.sol";

contract Marketplace {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

struct Product {
    uint256 id;
    uint256 price;
    address payable seller;
    address buyer;
    bool isSold;
    string ticketType;
    string ticketArea;
    string torcida; // novo campo
}


    uint public productCount;
    mapping(uint => Product) public products;

    event ProductAdded(uint id, uint price, address seller, string ticketType, string ticketArea, string torcida);
    event ProductPurchased(uint id, address buyer, string email);

    // ✅ Adiciona um novo produto
    function addProduct(
        uint _price,
        string memory _ticketType,
        string memory _ticketArea,
        string memory _torcida
    ) public {
        require(_price > 0, "O preco deve ser maior que zero");
        productCount++;


        products[productCount] = Product(
            productCount,
            _price,
            payable(msg.sender),
            address(0),
            false,
            _ticketType,
            _ticketArea,
            _torcida
        );

        emit ProductAdded(productCount, _price, msg.sender, _ticketType, _ticketArea, _torcida);
    }

    // 📦 Compra um produto
    function purchaseProduct(uint _id, string memory _email) public payable {
        Product storage product = products[_id];
        require(_id > 0 && _id <= productCount, "Produto invalido");
        require(!product.isSold, "Produto ja vendido");
        require(msg.value == product.price, "Valor incorreto");

        product.seller.transfer(msg.value);
        product.buyer = msg.sender;
        product.isSold = true;

        console.log("ID:", _id);
        console.log("Comprador:", msg.sender);

        emit ProductPurchased(_id, msg.sender, _email); 
    }

    // 📋 Lista todos os produtos
    function listProduct() public view returns (Product[] memory) {
        Product[] memory allProducts = new Product[](productCount);

        for (uint i = 1; i <= productCount; i++) {
            allProducts[i - 1] = products[i];
        }

        return allProducts;
    }
        // 🔍 Detalhes de um produto específico
    function getProduct(uint _id) public view returns ( uint, address, address, bool, string memory, string memory ,string memory ) {
        Product memory product = products[_id];
        return ( product.price, product.seller, product.buyer, product.isSold,product.ticketType,product.ticketArea,product.torcida);
    }

}


contract NameCoin {

    struct Item {
	address owner;
	uint value;
    }

    mapping (uint => Item) registry;

    function register(uint key) {
	if (registry[key].owner == 0) {
	    registry[key].owner = msg.sender;
	}
    }

    function transferOwnership(uint key, address newOwner) {
	if (registry[key].owner == msg.sender) {
	    registry[key].owner = newOwner;
	}
    }

    function setValue(uint key, uint newValue) {
	if (registry[key].owner == msg.sender) {
	    registry[key].value = newValue;
	}
    }

    function getValue(uint key) constant returns (uint value) {
	return registry[key].value;
    }

    function getOwner(uint key) constant returns (address owner) {
	return registry[key].owner;
    }
}

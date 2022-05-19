from pathlib import Path
from typing import List

from ape import Project
from ape.contracts import ContractInstance
from ape.types import AddressType
from ape.utils import ManagerAccessMixin

PROJECT = Project(Path(__file__).parent / "v2.json")

ADDRESS = {
    "ethereum": {
        "mainnet": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
        "rospten": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
        "rinkeby": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
        "kovan": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
        "goerli": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
    },
    "bsc": {
        "mainnet": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
    },
    "polygon": {
        "mainnet": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
        "mumbai": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
    },
    "fantom": {
        "opera": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
        "testnet": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
    },
}


class Factory(ManagerAccessMixin):
    @property
    def address(self) -> AddressType:
        ecosystem_name = self.provider.network.ecosystem.name
        network_name = self.provider.network.name
        return AddressType(ADDRESS[ecosystem_name][network_name])  # type: ignore

    @property
    def contract(self) -> ContractInstance:
        return PROJECT.UniswapV2Factory.at(self.address)  # type: ignore

    def get_pools(self, token: AddressType) -> List["Pool"]:
        addresses = (
            self.contract.PairCreated.query("pair", token0=token)
            or self.contract.PairCreated.query("pair", token1=token)
        )
        return [Pool(address) for address in addresses.pair]

    def get_all_pools(self) -> List["Pool"]:
        addresses = self.contract.PairCreated.query("pair")
        return [Pool(address) for address in addresses.pair]


class Pool:
    def __init__(self, address: AddressType):
        self.address = address

    @property
    def contract(self) -> ContractInstance:
        return PROJECT.UniswapV2Pair.at(self.address)  # type: ignore

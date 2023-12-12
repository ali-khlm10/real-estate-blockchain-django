import hashlib
from token_module.models import smartContractModel


def smart_contract_address(contract_name: str):
    contract: smartContractModel = smartContractModel.objects.filter(
        contract_name__iexact=contract_name).first()
    if contract is None:
        create_smart_contract_account_function(contract_name=contract_name)
    else:
        return contract.contract_address


def create_smart_contract_account_function(contract_name: str):
    new_contract: smartContractModel = smartContractModel.objects.create(
        contract_name=contract_name,
        contract_address=create_contract_address(
            contract_name=contract_name),
    )
    new_contract.save()
    return new_contract.contract_address


def create_contract_address(contract_name: str):
    sha512 = hashlib.sha512()
    sha512.update(contract_name.encode('utf-8'))
    sha512_digest = sha512.digest()
    contract_address = sha512_digest[-20:].hex()
    return f'0x{contract_address}'

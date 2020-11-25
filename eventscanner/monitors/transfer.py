from eventscanner.queue.pika_handler import send_to_backend
from mywish_models.models import Transfer, session
from scanner.events.block_event import BlockEvent
from settings.settings_local import NETWORKS


class TransferMonitor:
    network_type = []
    currency = None
    event_type = 'transferred'

    @classmethod
    def on_new_block_event(cls, block_event: BlockEvent):
        if block_event.network.type not in cls.network_type:
            return

        tx_hashes = set()
        for address_transactions in block_event.transactions_by_address.values():
            for transaction in address_transactions:
                tx_hashes.add(transaction.tx_hash)

        transfers = session \
            .query(Transfer) \
            .filter(Transfer.tx_hash.in_(tx_hashes), Transfer.currency == cls.currency) \
            .distinct(Transfer.tx_hash) \
            .all()
        for transfer in transfers:
            message = {
                'transactionHash': transfer.tx_hash,
                'transferId': transfer.id,
                'currency': cls.currency,
                'amount': int(transfer.amount),
                'success': True,
                'status': 'COMMITTED',
            }
            send_to_backend(cls.event_type, NETWORKS[block_event.network.type]['queue'], message)


class QurasTransferMonitor(TransferMonitor):
    network_type = ['QURAS_MAINNET']
    currency = 'XQC_NATIVE'


class EthTransferMonitor(TransferMonitor):
    network_type = ['ETHEREUM_MAINNET']
    currency = 'ETH'

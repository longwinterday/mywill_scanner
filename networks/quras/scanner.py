from collections import defaultdict

from eventscanner.queue.subscribers import pub

from scanner.events.block_event import BlockEvent
from scanner.services.scanner_polling import ScannerPolling


class QurasScanner(ScannerPolling):
    def process_block(self, block):
        print('{}: new block received {} ({})'.format(self.network.type, block.number, block.hash), flush=True)
        if not block.transactions:
            print('{}: no transactions in {} ({})'.format(self.network.type, block.number, block.hash), flush=True)
            return

        address_transactions = defaultdict(list)
        for transaction in block.transactions:
            for input in transaction.inputs:
                for inp in input:
                    address_transactions[inp.lower()].append(transaction)
            for output in transaction.outputs:
                    address_transactions[output.address].append(transaction)

        print('{}: transactions'.format(self.network.type), address_transactions, flush=True)
        block_event = BlockEvent(self.network, block, address_transactions)

        pub.sendMessage(self.network.type, block_event=block_event)

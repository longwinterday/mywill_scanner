from pubsub import pub

from eventscanner.monitors.payments import ERC20PaymentMonitor, EthPaymentMonitor, QurasPaymentMonitor
from eventscanner.monitors import transfer


pub.subscribe(ERC20PaymentMonitor.on_new_block_event, 'ETHEREUM_MAINNET')
pub.subscribe(EthPaymentMonitor.on_new_block_event, 'ETHEREUM_MAINNET')
pub.subscribe(QurasPaymentMonitor.on_new_block_event, 'QURAS_MAINNET')
pub.subscribe(transfer.QurasTransferMonitor.on_new_block_event, 'QURAS_MAINNET')
pub.subscribe(transfer.EthTransferMonitor.on_new_block_event, 'ETHEREUM_MAINNET')

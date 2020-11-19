import sys
import time

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback


from backend.blockchain.Block import Block

subscribe_key = 'sub-c-a8ba568a-1645-11eb-ae19-92aa6521e721'
publish_key = 'pub-c-6293fa95-3eb5-4b86-8111-2c125ff39a4d'


pnconfig = PNConfiguration()
pnconfig.subscribe_key = subscribe_key
pnconfig.publish_key =publish_key




CHANNELS = {
'TEST': 'TEST',
'BLOCK': 'BLOCK'
}

class Listener(SubscribeCallback):
    def __init__(self, blockchain):
        self.blockchain = blockchain


    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain  = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                print('\n -- Sucessfully replaced the local chain')
            except Exception as e:
                print(f'\n -- Did not replace chain: {e}')




class PubSub():
    """
    Handles the publish/subscribe layer of the application.
    Provides communication between the nodes of the blockchain network
    """
    def __init__(self, blockchain):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))

    def publish(self, channel, message):
        """ 
        Publish the mesage to the channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast block to all nodes
        """
        self.publish(CHANNELS['BLOCK'], block.to_json()) 

print("after listener")

def main():

    pubsub = PubSub()

    time.sleep(1)

    pubsub.publish(CHANNELS['TEST'], { 'foo': 'bar'} )
    print("after publish")

    try:
        sys.exit()
    except SystemExit :
        print("I will not exit this time")

if __name__ == '__main__':
    main()


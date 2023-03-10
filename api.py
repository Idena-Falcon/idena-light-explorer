import requests


class IdenaAPI:

    _host = "localhost"
    _port = "8100"
    _timeout = 3
    _api_key = None

    def __init__(self, host=_host, port=_port, timeout=_timeout, api_key=_api_key):
        self._host = host
        self._port = port
        self._timeout = timeout
        self._api_key = api_key
        self.url = f"http://{host}:{port}"

    def _request(self, url, payload):
        try:
            return requests.post(url, json=payload, timeout=self._timeout).json()
        except Exception as e:
            return {"error": {"message": str(e), "code": 0}}

    def identities(self, api_key=None):
        """ List all identities (not only validated ones) """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "dna_identities",
            "id": 1
        }
        return self._request(self.url, payload)

    def identity(self, address, api_key=None):
        """ Show info about identity for given address """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "dna_identity",
            "params": [address],
            "id": 1
        }
        return self._request(self.url, payload)

    def epoch(self, api_key=None):
        """ Details about the current epoch """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "dna_epoch",
            "id": 1
        }
        return self._request(self.url, payload)

    def ceremony_intervals(self, api_key=None):
        """ Show info about validation ceremony """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "dna_ceremonyIntervals",
            "id": 1
        }
        return self._request(self.url, payload)

    def address(self, api_key=None):
        """ Show address for current identity """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "dna_getCoinbaseAddr",
            "id": 1
        }
        return self._request(self.url, payload)

    def balance(self, address, api_key=None):
        """ Show DNA balance for address """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "dna_getBalance",
            "params": [address],
            "id": 1
        }
        return self._request(self.url, payload)

    def transaction(self, trx_hash, api_key=None):
        """ Details about a specific transaction """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "bcn_transaction",
            "params": [trx_hash],
            "id": 1
        }
        return self._request(self.url, payload)

    def transactions(self, address, count, api_key=None):
        """ List specific number of transactions for given address """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "bcn_transactions",
            "params": [{"address": f"{address}", "count": int(count)}],
            "id": 1
        }
        return self._request(self.url, payload)

    def pending_transactions(self, address, count, api_key=None):
        """ List specific number of pending transactions for given address """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "bcn_pendingTransactions",
            "params": [{"address": f"{address}", "count": int(count)}],
            "id": 1
        }
        return self._request(self.url, payload)

    def kill_identity(self, address, api_key=None):
        """ Kill your identity """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "dna_sendTransaction",
            "params": [{"type": 3, "from": f"{address}", "to": f"{address}"}],
            "id": 1
        }
        return self._request(self.url, payload)

    def go_online(self, api_key=None):
        """ Go online, serve as a valid node and start mining """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "dna_becomeOnline",
            "params": [{}],
            "id": 1
        }
        return self._request(self.url, payload)

    def go_offline(self, api_key=None):
        """ Go offline, do not serve as a node and stop mining """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "dna_becomeOffline",
            "params": [{}],
            "id": 1
        }
        return self._request(self.url, payload)

    # TODO: Untested!
    def send_invite(self, to_address, amount, api_key=None):
        """ Send invite code to given address """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "dna_sendInvite",
            "params": [{"to": to_address, "amount": amount}],
            "id": 1
        }
        return self._request(self.url, payload)

    # TODO: Untested!
    def activate_invite(self, to_address, key, api_key=None):
        """ Send invite code to given address """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "dna_activateInvite",
            "params": [{"to": to_address, "key": key}],
            "id": 1
        }
        return self._request(self.url, payload)

    # TODO: Untested!
    def fetch_flip_short_hashes(self, api_key=None):
        """ Get hashes for flips in short session """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "flip_shortHashes",
            "id": 1
        }
        return self._request(self.url, payload)

    # TODO: Untested!
    def fetch_flip_long_hashes(self, api_key=None):
        """ Get hashes for flips in long session """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "flip_longHashes",
            "id": 1
        }
        return self._request(self.url, payload)

    # TODO: Untested!
    def get_flip(self, flip_hash, api_key=None):
        """ Show info about flip by providing his hash """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "flip_get",
            "params": [flip_hash],
            "id": 1
        }
        return self._request(self.url, payload)

    # TODO: Untested!
    def submit_short_answers(self, answers, nonce, epoch, api_key=None):
        """ Show info about flip by providing his hash """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "flip_submitShortAnswers",
            "params": [{answers, nonce, epoch}],
            "id": 1
        }
        return self._request(self.url, payload)

    # TODO: Untested!
    def submit_long_answers(self, answers, nonce, epoch, api_key=None):
        """ Show info about flip by providing his hash """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "flip_submitLongAnswers",
            "params": [{answers, nonce, epoch}],
            "id": 1
        }
        return self._request(self.url, payload)

    # TODO: Untested!
    def submit_flip(self, flip_hex, pair_id, api_key=None):
        """  """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "flip_submit",
            "params": [{"hex": flip_hex, "pair": pair_id}],
            "id": 1
        }
        return self._request(self.url, payload)

    def send(self, from_address, to_address, amount, api_key=None):
        """ Send amount of DNA from address to address """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "dna_sendTransaction",
            "params": [{"from": from_address, "to": to_address, "amount": amount}],
            "id": 1
        }
        return self._request(self.url, payload)

    def sync_status(self, api_key=None):
        """ Show if node is synchronized """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "bcn_syncing",
            "id": 1
        }
        return self._request(self.url, payload)

    def node_version(self, api_key=None):
        """ Show node version """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "dna_version",
            "id": 1
        }
        return self._request(self.url, payload)

    def import_key(self, key, password, api_key=None):
        """ Import private key to manage specific identity """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "dna_importKey",
            "params": [{"key": key, "password": password}],
            "id": 1
        }
        return self._request(self.url, payload)

    def export_key(self, password, api_key=None):
        """ Export private key to backup your identity """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "dna_exportKey",
            "params": [password],
            "id": 1
        }
        return self._request(self.url, payload)

    def enode(self, api_key=None):
        """ Get info abut enode: ID, IP and Port """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "net_enode",
            "id": 1
        }
        return self._request(self.url, payload)
    # bcn_blockAt returns block at given height
    def block_at(self, height, api_key=None):
        """ Get block at given height """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "bcn_blockAt",
            "params": [height],
            "id": 1
        }
        return self._request(self.url, payload)
    # bcn_block returns block at given hash
    def block(self, block_hash, api_key=None):
        """ Get block by hash """
        payload = {
            "key": api_key if api_key else self._api_key,
            "method": "bcn_block",
            "params": [block_hash],
            "id": 1
        }
        return self._request(self.url, payload)
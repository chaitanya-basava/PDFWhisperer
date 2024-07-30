import time
import threading
import pickle
from collections.abc import MutableMapping
from typing import Any, Dict, Iterator

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory


class AutoExpireDict(MutableMapping):
    """
    A dictionary that automatically expires keys after a certain timeout.
    If the key isn't accessed or updated for the timeout period, it will be removed from the dictionary.

    :param _timeout: The timeout period in seconds
    :param _pickle_file: The file to save the dictionary to
    :param _convo_history_length: The length of the conversation history to store for each session
    """
    def __init__(self, _timeout: int, _pickle_file: str, _convo_history_length: int) -> None:
        self.timeout = _timeout
        self.pickle_file = _pickle_file
        self._chat_history_length = _convo_history_length * 2

        self.store: Dict[Any, Dict[str, Any]] = {}
        self.lock = threading.RLock()
        self.load_from_pickle()

        self.cleanup_thread = threading.Thread(target=self.cleanup_expired_keys, daemon=True)
        self.cleanup_thread.start()

        self.save_on_exit()

    def __setitem__(self, key: Any, value: Any) -> None:
        with self.lock:
            self.store[key] = {'value': value, 'timestamp': time.time()}

    def __getitem__(self, key: Any) -> Any:
        with self.lock:
            if key in self.store:
                self.store[key]['timestamp'] = time.time()
                return self.store[key]['value']
            raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        with self.lock:
            if key in self.store:
                del self.store[key]
            else:
                raise KeyError(key)

    def __iter__(self) -> Iterator[Any]:
        with self.lock:
            return iter(self.store)

    def __len__(self) -> int:
        with self.lock:
            return len(self.store)

    def cleanup_expired_keys(self) -> None:
        while True:
            time.sleep(self.timeout)
            with self.lock:
                current_time = time.time()
                keys_to_delete = [key for key, value in self.store.items() if
                                  current_time - value['timestamp'] > self.timeout]
                for key in keys_to_delete:
                    del self.store[key]

    def save_to_pickle(self) -> None:
        with open(self.pickle_file, 'wb') as f:
            pickle.dump(self.store, f)

    def load_from_pickle(self) -> None:
        try:
            with open(self.pickle_file, 'rb') as f:
                self.store.update(pickle.load(f))
        except FileNotFoundError:
            pass

    def save_on_exit(self) -> None:
        import atexit
        atexit.register(self.save_to_pickle)

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            new_chat = ChatMessageHistory()
            self.__setitem__(session_id, new_chat)
            return new_chat

        messages = self.__getitem__(session_id).messages
        new_chat = ChatMessageHistory(messages=messages[-self._chat_history_length:])
        self.__setitem__(session_id, new_chat)
        return new_chat


if __name__ == '__main__':
    timeout = 2  # seconds
    pickle_file = 'test_auto_expire_dict.pkl'
    d = AutoExpireDict(timeout, pickle_file)

    # Example operations
    d['a'] = 1
    d['b'] = 2

    print(d['a'])  # Accessing 'a'

    time.sleep(1)  # Wait for keys to expire

    try:
        print(d['a'])  # This should raise a KeyError
    except KeyError:
        print("Key 'a' has expired")

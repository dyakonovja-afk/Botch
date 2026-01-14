from collections import deque

queue = deque()
active_chats = {}

def add_to_queue(user_id: int):
    if user_id not in queue:
        queue.append(user_id)

def try_match():
    if len(queue) >= 2:
        a = queue.popleft()
        b = queue.popleft()
        active_chats[a] = b
        active_chats[b] = a
        return a, b
    return None, None

def end_chat(user_id: int):
    partner = active_chats.pop(user_id, None)
    if partner:
        active_chats.pop(partner, None)
    return partner

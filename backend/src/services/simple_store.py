from typing import Any, List, Optional
from chatkit.store import Store, NotFoundError
from chatkit.types import (
    Attachment,
    Page,
    ThreadItem,
    ThreadMetadata,
)

class SimpleMemoryStore(Store[Any]):
    def __init__(self):
        self.threads: dict[str, ThreadMetadata] = {}
        self.items: dict[str, List[ThreadItem]] = {}
        self.attachments: dict[str, Attachment] = {}

    async def load_thread(self, thread_id: str, context: Any) -> ThreadMetadata:
        if thread_id not in self.threads:
            raise NotFoundError(f"Thread {thread_id} not found")
        return self.threads[thread_id]

    async def save_thread(self, thread: ThreadMetadata, context: Any) -> None:
        self.threads[thread.id] = thread

    async def load_thread_items(
        self,
        thread_id: str,
        after: Optional[str],
        limit: int,
        order: str,
        context: Any,
    ) -> Page[ThreadItem]:
        items = self.items.get(thread_id, [])
        # Simple pagination: ignore 'after' for now, return all or slice
        # In real usage, 'after' is cursor.
        # Check order: 'asc' or 'desc'.
        sorted_items = sorted(items, key=lambda x: x.created_at, reverse=(order == 'desc'))
        
        # Determine start index
        start_index = 0
        if after:
            for i, item in enumerate(sorted_items):
                if item.id == after:
                    start_index = i + 1
                    break
        
        sliced_items = sorted_items[start_index : start_index + limit]
        has_next_page = (start_index + limit) < len(sorted_items)
        end_cursor = sliced_items[-1].id if sliced_items else None

        return Page(data=sliced_items, has_next_page=has_next_page, end_cursor=end_cursor)

    async def save_attachment(self, attachment: Attachment, context: Any) -> None:
        self.attachments[attachment.id] = attachment

    async def load_attachment(self, attachment_id: str, context: Any) -> Attachment:
        if attachment_id not in self.attachments:
            raise NotFoundError(f"Attachment {attachment_id} not found")
        return self.attachments[attachment_id]

    async def delete_attachment(self, attachment_id: str, context: Any) -> None:
        if attachment_id in self.attachments:
            del self.attachments[attachment_id]

    async def load_threads(
        self,
        limit: int,
        after: Optional[str],
        order: str,
        context: Any,
    ) -> Page[ThreadMetadata]:
        all_threads = list(self.threads.values())
        # Sort
        sorted_threads = sorted(all_threads, key=lambda x: x.created_at, reverse=(order == 'desc'))
        
        start_index = 0
        if after:
             for i, t in enumerate(sorted_threads):
                if t.id == after:
                    start_index = i + 1
                    break
        
        sliced = sorted_threads[start_index : start_index + limit]
        has_next = (start_index + limit) < len(sorted_threads)
        end_cursor = sliced[-1].id if sliced else None
        
        return Page(data=sliced, has_next_page=has_next, end_cursor=end_cursor)

    async def add_thread_item(self, thread_id: str, item: ThreadItem, context: Any) -> None:
        if thread_id not in self.items:
            self.items[thread_id] = []
        self.items[thread_id].append(item)

    async def save_item(self, thread_id: str, item: ThreadItem, context: Any) -> None:
        if thread_id not in self.items:
            # Should probably error if thread doesn't exist, but creating list is safer
             self.items[thread_id] = []
        
        # Update existing or append
        existing_index = next((i for i, x in enumerate(self.items[thread_id]) if x.id == item.id), -1)
        if existing_index >= 0:
            self.items[thread_id][existing_index] = item
        else:
            self.items[thread_id].append(item)

    async def load_item(self, thread_id: str, item_id: str, context: Any) -> ThreadItem:
        items = self.items.get(thread_id, [])
        for item in items:
            if item.id == item_id:
                return item
        raise NotFoundError(f"Item {item_id} in {thread_id} not found")

    async def delete_thread(self, thread_id: str, context: Any) -> None:
        if thread_id in self.threads:
            del self.threads[thread_id]
        if thread_id in self.items:
            del self.items[thread_id]

    async def delete_thread_item(self, thread_id: str, item_id: str, context: Any) -> None:
        if thread_id in self.items:
             self.items[thread_id] = [i for i in self.items[thread_id] if i.id != item_id]

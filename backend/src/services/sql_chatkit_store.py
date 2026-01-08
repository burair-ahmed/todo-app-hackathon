from typing import Any, List, Optional
from chatkit.store import Store, NotFoundError
from chatkit.types import (
    Attachment,
    Page,
    ThreadItem,
    ThreadMetadata,
    UserMessageItem,
    AssistantMessageItem,
    HiddenContextItem,
    UserMessageContent,
    UserMessageTextContent,
    AssistantMessageContent,
    InferenceOptions
)
from ..models.chatkit_models import ChatKitThread, ChatKitItem
from ..database.database import get_session
from sqlmodel import select
import json
from datetime import datetime

import logging

logger = logging.getLogger(__name__)

class SQLChatKitStore(Store[Any]):
    def __init__(self):
        # We assume transient session management via get_session()
        pass

    async def load_thread(self, thread_id: str, context: Any) -> ThreadMetadata:
        logger.info(f"Loading thread {thread_id}")
        with next(get_session()) as session:
            db_thread = session.exec(select(ChatKitThread).where(ChatKitThread.id == thread_id)).first()
            if not db_thread:
                logger.warning(f"Thread {thread_id} not found")
                raise NotFoundError(f"Thread {thread_id} not found")
            
            return ThreadMetadata(
                id=db_thread.id,
                created_at=db_thread.created_at,
                metadata=db_thread.metadata_json
            )

    async def save_thread(self, thread: ThreadMetadata, context: Any) -> None:
        logger.info(f"Saving thread {thread.id}")
        with next(get_session()) as session:
            db_thread = session.exec(select(ChatKitThread).where(ChatKitThread.id == thread.id)).first()
            if not db_thread:
                db_thread = ChatKitThread(
                    id=thread.id,
                    created_at=thread.created_at or datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    metadata_json=thread.metadata
                )
                session.add(db_thread)
            else:
                db_thread.updated_at = datetime.utcnow()
                db_thread.metadata_json = thread.metadata
                session.add(db_thread)
            session.commit()
            logger.info(f"Thread {thread.id} saved")

    async def load_thread_items(
        self,
        thread_id: str,
        after: Optional[str],
        limit: int,
        order: str,
        context: Any,
    ) -> Page[ThreadItem]:
        logger.info(f"Loading items for thread {thread_id}")
        with next(get_session()) as session:
            # Query items
            query = select(ChatKitItem).where(ChatKitItem.thread_id == thread_id)
            
            # Sort
            if order == 'desc':
                query = query.order_by(ChatKitItem.created_at.desc())
            else:
                query = query.order_by(ChatKitItem.created_at.asc())
            
            # TODO: Implement 'after' cursor logic efficiently for SQL
            # For now, fetch all and slice (not optimal for huge datasets but safe for MVP)
            # Or better: load a reasonable batch.
            # Since 'after' is an ID, and we don't have integer IDs guaranteed to be sequential for cursor pagination on ID easily without lookup
            all_items = session.exec(query).all()
            
            # Filter in Python for cursor if present
            start_index = 0
            if after:
                for i, item in enumerate(all_items):
                    if item.id == after:
                        start_index = i + 1
                        break
            
            sliced_db_items = all_items[start_index : start_index + limit]
            
            # Convert DB items to ChatKit Types
            result_items = []
            for db_item in sliced_db_items:
                item_obj = self._db_item_to_chatkit(db_item)
                if item_obj:
                    result_items.append(item_obj)
            
            has_next_page = (start_index + limit) < len(all_items)
            end_cursor = result_items[-1].id if result_items else None

            logger.info(f"Loaded {len(result_items)} items for thread {thread_id}")
            return Page(data=result_items, has_next_page=has_next_page, end_cursor=end_cursor)

    def _db_item_to_chatkit(self, db_item: ChatKitItem) -> ThreadItem:
        params = {
            "id": db_item.id,
            "thread_id": db_item.thread_id,
            "created_at": db_item.created_at
        }
        
        content_data = db_item.content
        
        if db_item.type == "user_message":
            # Reconstruct content list
            content_list = []
            for part in content_data.get("content", []):
                if part.get("type") == "text":
                    content_list.append(UserMessageTextContent(text=part.get("text")))
            return UserMessageItem(**params, content=content_list, inference_options=InferenceOptions())
            
        elif db_item.type == "assistant_message":
            content_list = []
            for part in content_data.get("content", []):
                if part.get("type") == "text":
                    # Reconstruction annotations if needed
                    content_list.append(AssistantMessageContent(text=part.get("text"), annotations=[]))
            return AssistantMessageItem(**params, content=content_list)
            
        elif db_item.type == "hidden_context_item":
             return HiddenContextItem(**params, content=content_data.get("content"))
             
        # Fallback
        return None

    def _chatkit_to_db_content(self, item: ThreadItem) -> dict:
        if isinstance(item, UserMessageItem):
            return {"content": [{"type": "text", "text": c.text} for c in item.content]}
        elif isinstance(item, AssistantMessageItem):
             return {"content": [{"type": "text", "text": c.text} for c in item.content]}
        elif isinstance(item, HiddenContextItem):
            return {"content": item.content}
        return {}

    async def save_item(self, thread_id: str, item: ThreadItem, context: Any) -> None:
        logger.info(f"Saving item {item.id} to thread {thread_id}")
        with next(get_session()) as session:
            # Check existence
            db_item = session.exec(select(ChatKitItem).where(ChatKitItem.id == item.id)).first()
            
            content_json = self._chatkit_to_db_content(item)
            item_type = ""
            if isinstance(item, UserMessageItem): item_type = "user_message"
            elif isinstance(item, AssistantMessageItem): item_type = "assistant_message"
            elif isinstance(item, HiddenContextItem): item_type = "hidden_context_item"
            
            if not db_item:
                db_item = ChatKitItem(
                    id=item.id,
                    thread_id=thread_id,
                    type=item_type,
                    created_at=item.created_at or datetime.utcnow(),
                    content=content_json
                )
                session.add(db_item)
            else:
                db_item.content = content_json
                session.add(db_item)
            
            session.commit()
            logger.info(f"Item {item.id} saved")

    async def add_thread_item(self, thread_id: str, item: ThreadItem, context: Any) -> None:
        await self.save_item(thread_id, item, context)

    # Attachments - Not used yet, implementing stubs
    async def save_attachment(self, attachment: Attachment, context: Any) -> None:
        pass
    async def load_attachment(self, attachment_id: str, context: Any) -> Attachment:
        raise NotFoundError("Attachment not found")
    async def delete_attachment(self, attachment_id: str, context: Any) -> None:
        pass

    async def load_threads(self, limit: int, after: Optional[str], order: str, context: Any) -> Page[ThreadMetadata]:
        logger.info(f"Loading threads with limit={limit}, after={after}, order={order}")
        with next(get_session()) as session:
            query = select(ChatKitThread)
            
            # Sort by updated_at desc usually
            if order == 'asc':
                 query = query.order_by(ChatKitThread.updated_at.asc())
            else:
                 query = query.order_by(ChatKitThread.updated_at.desc())

            all_threads = session.exec(query).all()
            
            # Simple pagination logic (same as load_thread_items)
            start_index = 0
            if after:
                for i, thread in enumerate(all_threads):
                    if thread.id == after:
                        start_index = i + 1
                        break
            
            sliced_threads = all_threads[start_index : start_index + limit]
            
            results = []
            for t in sliced_threads:
                results.append(ThreadMetadata(
                    id=t.id,
                    created_at=t.created_at,
                    metadata=t.metadata_json
                ))
                
            has_next_page = (start_index + limit) < len(all_threads)
            end_cursor = results[-1].id if results else None
            
            logger.info(f"Loaded {len(results)} threads")
            return Page(data=results, has_next_page=has_next_page, end_cursor=end_cursor)

    async def load_item(self, thread_id: str, item_id: str, context: Any) -> ThreadItem:
        with next(get_session()) as session:
            db_item = session.exec(select(ChatKitItem).where(ChatKitItem.id == item_id)).first()
            if not db_item:
                raise NotFoundError(f"Item {item_id} not found")
            return self._db_item_to_chatkit(db_item)

    async def delete_thread(self, thread_id: str, context: Any) -> None:
        with next(get_session()) as session:
            session.exec(select(ChatKitItem).where(ChatKitItem.thread_id == thread_id)).delete()
            session.exec(select(ChatKitThread).where(ChatKitThread.id == thread_id)).delete()
            session.commit()

    async def delete_thread_item(self, thread_id: str, item_id: str, context: Any) -> None:
         with next(get_session()) as session:
            db_item = session.exec(select(ChatKitItem).where(ChatKitItem.id == item_id)).first()
            if db_item:
                session.delete(db_item)
                session.commit()

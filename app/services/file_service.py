from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.file import File as FileModel
from app.models.document import Document
import uuid
from datetime import datetime
from typing import Optional, List

async def import_to_documents_service(db: AsyncSession, kb_id: str, last_update_time: Optional[datetime] = None, file_ids: Optional[List[int]] = None, batch_size: int = 1000):
    offset = 0
    total_imported = 0
    total_skipped = 0
    while True:
        query = select(FileModel)
        if file_ids:
            query = query.where(FileModel.id.in_(file_ids))
        elif last_update_time:
            query = query.where(FileModel.upload_time >= last_update_time)
        query = query.offset(offset).limit(batch_size)
        files_result = await db.execute(query)
        files = files_result.scalars().all()
        if not files:
            break
        batch_file_ids = [f.id for f in files]
        exist_docs_result = await db.execute(select(Document.file_id).where(Document.file_id.in_(batch_file_ids)))
        exist_ids = set([row[0] for row in exist_docs_result.all()])
        to_insert = []
        for f in files:
            if f.id in exist_ids:
                total_skipped += 1
                continue
            doc = Document(
                document_id=str(uuid.uuid4()),
                file_id=f.id,
                summary=None,  # 先空着
                source='upload',
                kb_id=kb_id
            )
            to_insert.append(doc)
        db.add_all(to_insert)
        await db.commit()
        total_imported += len(to_insert)
        offset += batch_size
        if file_ids:
            break
    return {"imported": total_imported, "skipped": total_skipped} 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.archive_file import ArchiveFile
from app.models.archive_record import ArchiveRecord
from app.models.document import Document
import uuid
from datetime import datetime
from typing import Optional, List

async def import_to_documents_service(db: AsyncSession, last_update_time: Optional[datetime] = None, efile_ids: Optional[List[int]] = None, batch_size: int = 1000):
    offset = 0
    total_imported = 0
    total_skipped = 0
    while True:
        # 1. 分批查找
        query = select(ArchiveFile)
        if efile_ids:
            query = query.where(ArchiveFile.efile_id.in_(efile_ids))
        elif last_update_time:
            query = query.where(ArchiveFile.last_update_time >= last_update_time)
        query = query.offset(offset).limit(batch_size)
        archive_files_result = await db.execute(query)
        archive_files = archive_files_result.scalars().all()
        if not archive_files:
            break
        # 2. 批量查找已存在file_id
        batch_efile_ids = [f.efile_id for f in archive_files]
        exist_docs_result = await db.execute(select(Document.file_id).where(Document.file_id.in_(batch_efile_ids)))
        exist_ids = set([row[0] for row in exist_docs_result.all()])
        # 3. 批量查找record_id对应的kb_id
        record_ids = list(set(f.record_id for f in archive_files if f.record_id))
        kb_map = {}
        if record_ids:
            records_result = await db.execute(
                select(ArchiveRecord.record_id, ArchiveRecord.kb_id)
                .where(ArchiveRecord.record_id.in_(record_ids))
            )
            kb_map = {row[0]: row[1] for row in records_result.all()}
        # 4. 构造待插入对象
        to_insert = []
        for f in archive_files:
            if f.efile_id in exist_ids:
                total_skipped += 1
                continue
            doc = Document(
                document_id=str(uuid.uuid4()),
                file_id=f.efile_id,
                summary=f.label,
                source='archive',
                kb_id=kb_map.get(f.record_id)
            )
            to_insert.append(doc)
        db.add_all(to_insert)
        await db.commit()
        total_imported += len(to_insert)
        offset += batch_size
        # 如果是efile_ids模式，导入一批后就break（不分页）
        if efile_ids:
            break
    return {"imported": total_imported, "skipped": total_skipped} 
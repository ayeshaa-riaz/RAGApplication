








def upsert_user_memory(
    user_id: str,
    memory_context: str,
    topics: list[str],
    books: list[str],
    declined: list[str],
    tone: str
):
    session = SessionLocal()
    try:
        existing = session.query(UserMemory).filter(UserMemory.user_id == user_id).first()
        if existing:
            existing.memory_context = memory_context
            existing.topics = topics
            existing.books_engaged = books
            existing.declined_questions = declined
            existing.tone_preference = tone
            existing.last_updated = datetime.utcnow()
        else:
            new_entry = UserMemory(
                user_id=user_id,
                memory_context=memory_context,
                topics=topics,
                books_engaged=books,
                declined_questions=declined,
                tone_preference=tone
            )
            session.add(new_entry)
        session.commit()
    finally:
        session.close()

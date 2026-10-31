from app.services.rag import index_document, retrieve_context, answer_question


def ask_agent(question):

    index_document()

    context, sources, distance = retrieve_context(question)

    result = answer_question(question, context, sources)

    not_found = "Informasi tidak ditemukan" in result

    if not context or not_found:
        confidence = "low"
        reason = "no_relevant_context"

    elif distance <= 0.45:
        confidence = "high"
        reason = "answered"

    else:
        confidence = "medium"
        reason = "answered"

    return {
        "answer": result,
        "confidence_label": confidence,
        "reason_code": reason
    }

from app.services.llamaindex import initialize_agent


def generate_response(question):
    agent = initialize_agent()

    result = agent.query(question)
    answer_text = result.response

    sources = []
    scores = []

    for node_score in result.source_nodes:
        node = node_score.node
        score = node_score.score
        scores.append(score)

        sources.append({
            "source": node.metadata.get("source"),
            "heading": node.metadata.get("heading_title"),
            "section": node.metadata.get("section_type"),
            "text": node.text[:300] + "...",
            "score": score
        })

    # compute confidence
    confidence = max(scores) if scores else None

    return {
        "answer": answer_text,
        "confidence": confidence,
        "sources": sources
    }

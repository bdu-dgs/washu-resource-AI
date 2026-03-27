from app.db import get_connection
import psycopg2.extras

def extract_keywords(question: str):
    stop_words = {
        "i", "want", "to", "find", "and", "the", "a", "an",
        "for", "of", "in", "on", "with", "is", "are", "my"
    }

    words = question.lower().replace(",", " ").replace(".", " ").split()
    keywords = [w for w in words if w not in stop_words and len(w) > 2]

    return keywords

def search_faculty(keywords):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT name, department, research_keywords, expertise, email, profile_url, search_text
        FROM faculty
        LIMIT 300
    """)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = []

    for row in rows:
        score = 0
        matched = []

        name_text = (row.get("name") or "").lower()
        dept_text = (row.get("department") or "").lower()
        keyword_text = (row.get("research_keywords") or "").lower()
        expertise_text = (row.get("expertise") or "").lower()
        search_text = (row.get("search_text") or "").lower()

        for kw in keywords:
            if kw in name_text:
                score += 3
                matched.append(kw)
            if kw in dept_text:
                score += 2
                matched.append(kw)
            if kw in keyword_text:
                score += 2
                matched.append(kw)
            if kw in expertise_text:
                score += 1
                matched.append(kw)
            if kw in search_text:
                score += 2
                matched.append(kw)

        if score > 0:
            results.append({
                "name": row.get("name", ""),
                "type": "faculty",
                "description": row.get("expertise", ""),
                "url": row.get("profile_url", ""),
                "score": score,
                "why_matched": f"Matched keywords: {', '.join(sorted(set(matched)))}"
            })

    return results


def search_additional_resources(keywords):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT title, category, subcategory, description, url, source, university, data_source_type, search_text
        FROM additional_resources
        LIMIT 300
    """)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = []

    for row in rows:
        score = 0
        matched = []

        title_text = (row.get("title") or "").lower()
        category_text = (row.get("category") or "").lower()
        subcategory_text = (row.get("subcategory") or "").lower()
        desc_text = (row.get("description") or "").lower()
        search_text = (row.get("search_text") or "").lower()

        for kw in keywords:
            if kw in title_text:
                score += 3
                matched.append(kw)
            if kw in category_text:
                score += 2
                matched.append(kw)
            if kw in subcategory_text:
                score += 2
                matched.append(kw)
            if kw in desc_text:
                score += 1
                matched.append(kw)
            if kw in search_text:
                score += 2
                matched.append(kw)

        if score > 0:
            results.append({
                "name": row.get("title", ""),
                "type": "additional_resource",
                "description": row.get("description", ""),
                "url": row.get("url", ""),
                "score": score,
                "why_matched": f"Matched keywords: {', '.join(sorted(set(matched)))}"
            })

    return results


def search_research_opportunities(keywords):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT title, faculty, description, skills, source_url, search_text
        FROM research_opportunities
        LIMIT 300
    """)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = []

    for row in rows:
        score = 0
        matched = []

        title_text = (row.get("title") or "").lower()
        faculty_text = (row.get("faculty") or "").lower()
        desc_text = (row.get("description") or "").lower()
        skills_text = (row.get("skills") or "").lower()
        search_text = (row.get("search_text") or "").lower()

        for kw in keywords:
            if kw in title_text:
                score += 3
                matched.append(kw)
            if kw in faculty_text:
                score += 2
                matched.append(kw)
            if kw in skills_text:
                score += 2
                matched.append(kw)
            if kw in desc_text:
                score += 1
                matched.append(kw)
            if kw in search_text:
                score += 2
                matched.append(kw)

        if score > 0:
            results.append({
                "name": row.get("title", ""),
                "type": "research_opportunity",
                "description": row.get("description", ""),
                "url": row.get("source_url", ""),
                "score": score,
                "why_matched": f"Matched keywords: {', '.join(sorted(set(matched)))}"
            })

    return results


def search_all_resources(question: str):
    keywords = extract_keywords(question)

    faculty_results = search_faculty(keywords)
    additional_results = search_additional_resources(keywords)
    research_results = search_research_opportunities(keywords)

    all_results = faculty_results + additional_results + research_results
    all_results.sort(key=lambda x: x["score"], reverse=True)

    return all_results[:10]
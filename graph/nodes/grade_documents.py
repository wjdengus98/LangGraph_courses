from typing import Any, Dict

from graph.chains.retrieval_grader import retrieval_grader
from graph.state import GraphState


def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]
    
    filtered_docs = [] # 관련 있는 문서만 담을 리스트
    web_search = False # 웹 검색 필요 여부 플래그(문서 관련 = False)
    for d in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": d.page_content} # LLM에게 관련성 물어보기
        )
        grade = score.binary_score # "yes" 또는 "no"
        if grade.lower() == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d) # 관련 있음 → 보관
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            web_search = True  # 관련 없음 → 웹 검색 필요
            continue # 다음 문서로 넘어감
    return {"documents": filtered_docs, "question": question, "web_search": web_search}
    
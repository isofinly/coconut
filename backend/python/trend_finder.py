from pytrends.request import TrendReq
from typing import Any, List
import json
import pytrends

pytrends = TrendReq()


def get_interest_over_time(query: List[str]) -> dict[str, Any]:
    """
    Get the interest over time for a given query and format it as JSON.

    Args:
        query (List[str]): A list of query terms.

    Returns:
        str: A JSON string containing the formatted interest over time data.
    """
    pytrends.build_payload(query, timeframe='today 1-m', geo='RU')
    interest_over_time = pytrends.interest_over_time()
    interest_for_query = interest_over_time[query[0]].to_dict()

    formatted_data = [
        {
            "id": idx + 1,
            "timestamp": str(timestamp).strip("Timestamp('").strip("')"),
            "interest": interest
        }
        for idx, (timestamp, interest) in enumerate(interest_for_query.items())
    ]

    return formatted_data


def get_related_topics(query: List[str]) -> str:
    """
    Get the related topics for a given query and format them as JSON.

    Args:
        query (List[str]): A list of query terms.

    Returns:
        str: A JSON string containing the formatted related topics data.
    """
    pytrends.build_payload(query, timeframe='today 1-m', geo='RU')
    interest_over_time = pytrends.related_topics()

    related_topics_data = interest_over_time[query[0]]['top']

    # Create a list of dictionaries in the desired format
    formatted_data = []
    for index, row in related_topics_data.iterrows():
        topic_dict = {
            "id": index,
            "title": row['topic_title'],
            "type": row['topic_type'],
            "interest": int(row['value'])
        }
        formatted_data.append(topic_dict)

    return formatted_data


def get_related_queries(query: List[str]) -> str:
    """
    Get related queries for a given query.

    Args:
        query (List[str]): A list of query strings.

    Returns:
        str: A formatted JSON string containing the related queries.
    """
    pytrends.build_payload(kw_list=query)

    related_queries = pytrends.related_queries()

    formatted_data = []
    for index, row in related_queries[query[0]]['top'].iterrows():
        query_dict = {
            "id": index,
            "query": row['query'],
            "interest": int(row['value'])
        }
        formatted_data.append(query_dict)
    return formatted_data

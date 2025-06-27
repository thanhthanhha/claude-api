
google_search_properties = {
    "query": {
        "type": "string",
        "description": "String to query from google"
    }
}

wiki_search_properties = {
    "query": {
        "type": "string",
        "description": "Query from Wiki database, query about people, places, phenomanon of science,... For example query need to be a specific name like \"france\" \"Butterfly Effect\""
    }
}

webpage_search_properties = {
    "query": {
          "type": "array",
          "items": {
            "type": "string"
          },
        "description": "URL list for URL need to be read"
    }
}
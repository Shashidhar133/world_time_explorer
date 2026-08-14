def is_valid_country(country, countries):
    return country in countries


def search_countries(query, countries, limit=8):
    query = query.strip().lower()

    if not query:
        return []

    return [
        country
        for country in countries
        if query in country.lower()
    ][:limit]
import requests
from typing import Optional
import time

def get_company_logo(company_name: str, size: int = 128) -> Optional[str]:
    """
    Try to fetch company logo from multiple sources.
    Returns the first working logo URL or None if none found.

    Args:
        company_name: Name of the company
        size: Size of the logo (for Google favicons)

    Returns:
        URL of the working logo or None
    """
    if not company_name:
        return None

    # Clean company name
    clean_name = company_name.strip().lower()

    # Try to extract domain-like name
    domain_candidates = [
        clean_name.replace(' ', '').replace('-', ''),  # "J.P. Morgan" -> "jpmorgan"
        clean_name.replace(' ', '-'),                   # "Stack Adapt" -> "stack-adapt"
        clean_name.split()[0],                          # "Toyota Material Handling" -> "toyota"
        clean_name.replace('.', '').replace(' ', ''),   # "J.P. Morgan" -> "jpmorgan"
    ]

    # Special cases for known companies
    domain_mapping = {
        'j.p. morgan': 'jpmorgan.com',
        'jp morgan': 'jpmorgan.com',
        'jpmorgan': 'jpmorgan.com',
        'stackadapt': 'stackadapt.com',
        'stack adapt': 'stackadapt.com',
        'toyota material handling': 'toyota.com',
        'cedars-sinai medical center': 'cedars-sinai.org',
        'cedars sinai medical center': 'cedars-sinai.org',
        'generation bio': 'generationbio.com',
        'astrazeneca': 'astrazeneca.com',
        'glovo': 'glovo.com',
        'eurofins': 'eurofins.com',
        'enedis': 'enedis.fr',
    }

    # Check if we have a special mapping
    if clean_name in domain_mapping:
        domain_candidates.insert(0, domain_mapping[clean_name].replace('.com', '').replace('.org', '').replace('.fr', ''))

    # Logo sources to try
    logo_sources = []

    for domain in domain_candidates:
        if not domain:
            continue

        # Add common domain extensions
        domain_variants = [
            f"{domain}.com",
            f"{domain}.org",
            f"{domain}.net",
            domain
        ]

        for full_domain in domain_variants:
            # Google favicons (high quality, reliable)
            logo_sources.append(f"https://www.google.com/s2/favicons?domain={full_domain}&sz={size}")

            # Clearbit (good for companies)
            logo_sources.append(f"https://logo.clearbit.com/{domain}")

            # Logo.dev
            logo_sources.append(f"https://img.logo.dev/{full_domain}?token=pk_X-1ZO13GSgeOoUrIuJ6GMQ")

    # Test each URL
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })

    for url in logo_sources:
        try:
            response = session.head(url, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                # Verify it's actually an image
                content_type = response.headers.get('content-type', '')
                if 'image' in content_type.lower():
                    return url
        except:
            continue

        # Small delay to be respectful to APIs
        time.sleep(0.1)

    return None

def test_logo_fetcher():
    """Test the logo fetcher with companies from the JSON"""
    test_companies = [
        "Glovo",
        "J.P. Morgan",
        "StackAdapt",
        "AstraZeneca",
        "Toyota Material Handling",
        "Generation Bio",
        "Cedars-Sinai Medical Center",
        "Eurofins",
        "Enedis"
    ]

    print("Testing logo fetcher...")
    for company in test_companies:
        logo_url = get_company_logo(company)
        print(f"{company:30} -> {logo_url or 'Not found'}")

if __name__ == "__main__":
    test_logo_fetcher()
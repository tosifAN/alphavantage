import csv
import os
from io import StringIO

import pytest

from alphavantage_mcp_server.api import fetch_earnings_calendar


@pytest.mark.asyncio
async def test_fetch_earnings_calendar():
    """Test fetching earnings calendar with real API call."""
    api_key = os.getenv('ALPHAVANTAGE_API_KEY')
    assert api_key, "ALPHAVANTAGE_API_KEY must be set in environment"

    result = await fetch_earnings_calendar(symbol="AAPL", horizon="3month")

    assert isinstance(result, str), "API should return CSV data as string"

    # Parse CSV data
    csv_reader = csv.DictReader(StringIO(result))
    rows = list(csv_reader)

    # Basic validation of structure
    assert len(rows) > 0, "CSV should contain at least one row"

    # Check required fields in first row
    first_row = rows[0]
    required_fields = ["symbol", "name", "reportDate"]
    for field in required_fields:
        assert field in first_row, f"Field '{field}' missing from CSV data"

    # Check if we found AAPL data
    apple_entries = [row for row in rows if row["symbol"] == "AAPL"]
    assert len(apple_entries) > 0, "Should find AAPL entries in the response"
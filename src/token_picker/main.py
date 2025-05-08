#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from token_picker.crew import TokenPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crypto token research crew.
    """
    inputs = {
        'sector': 'DeFi',  # Changed from Technology to DeFi as a crypto-specific sector
        "current_date": str(datetime.now())
    }

    # Create and run the crew
    result = TokenPicker().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL TOKEN DECISION ===\n\n")
    print(result.raw)


if __name__ == "__main__":
    run()
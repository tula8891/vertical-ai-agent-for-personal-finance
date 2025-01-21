"""Test TruLens imports"""

try:
    from trulens.core import TruSession

    print("✓ trulens.core.TruSession imported successfully")
except ImportError as e:
    print("✗ Failed to import trulens.core.TruSession:", str(e))

try:
    from trulens.connectors.snowflake import SnowflakeConnector

    print("✓ trulens.connectors.snowflake.SnowflakeConnector imported successfully")
except ImportError as e:
    print("✗ Failed to import trulens.connectors.snowflake.SnowflakeConnector:", str(e))

try:
    from trulens.apps.custom import TruCustomApp, instrument

    print("✓ trulens.apps.custom imports successful")
except ImportError as e:
    print("✗ Failed to import from trulens.apps.custom:", str(e))

try:
    from trulens.feedback import GroundTruthAgreement

    print("✓ trulens.feedback.GroundTruthAgreement imported successfully")
except ImportError as e:
    print("✗ Failed to import trulens.feedback.GroundTruthAgreement:", str(e))

try:
    from trulens.providers.cortex import Cortex

    print("✓ trulens.providers.cortex.Cortex imported successfully")
except ImportError as e:
    print("✗ Failed to import trulens.providers.cortex.Cortex:", str(e))

try:
    from trulens.core import Feedback, Select

    print("✓ trulens.core.Feedback and Select imported successfully")
except ImportError as e:
    print("✗ Failed to import trulens.core components:", str(e))

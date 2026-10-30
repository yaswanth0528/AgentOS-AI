
from app.tools.permissions import ToolPermissionManager


# Create permission manager
permissions = ToolPermissionManager()


# Test 1: Initially denied
print(
    "Initially allowed:",
    permissions.is_allowed("web_search")
)


# Test 2: Grant permission
permissions.grant_permission("web_search")

print(
    "After granting:",
    permissions.is_allowed("web_search")
)


# Test 3: Require permission
try:
    permissions.require_permission("web_search")
    print("Permission check: PASSED")

except PermissionError as error:
    print(error)


# Test 4: Revoke permission
permissions.revoke_permission("web_search")

print(
    "After revoking:",
    permissions.is_allowed("web_search")
)


# Test 5: List allowed tools
permissions.grant_permission("weather")

print(
    "Allowed tools:",
    permissions.list_allowed_tools()
)

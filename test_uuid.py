import uuid

# Create a UUID from a hex string
existing_uuid_str = "550e8400-e29b-41d4-a716-446655440000"
existing_uuid = uuid.UUID(existing_uuid_str)

print(f"Existing UUID: {existing_uuid}")
print(f"Variant: {existing_uuid.variant}")
print(f"Version: {existing_uuid.version}")
